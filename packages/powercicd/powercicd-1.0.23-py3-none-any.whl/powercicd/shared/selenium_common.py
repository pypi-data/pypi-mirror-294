import logging
import os
import socket

from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium import webdriver

log = logging.getLogger(__name__)


def find_free_port(start_port=20000, end_port=30000):
    """Finds a free port number in the specified range."""
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))  # Try to bind to the port
                return port  # If successful, return the port
            except OSError:
                pass  # If the port is in use, continue to the next one
    raise ValueError(f"No free port found in the specified range ({start_port}-{end_port}).")


def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def configure_selenium_logger(tmp_dir: str):
    from selenium.webdriver.remote.remote_connection import LOGGER
    LOGGER.propagate = False
    
    selenium_log_path = os.path.normpath(os.path.abspath(fr"{tmp_dir}\selenium.log"))
    log_dir = os.path.dirname(selenium_log_path)
    log.debug(f"Ensuring the log directory exists: '{log_dir}'")
    os.makedirs(log_dir, exist_ok=True)
    selenium_handler = logging.FileHandler(selenium_log_path)
    selenium_handler.setLevel(logging.INFO)
    selenium_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    LOGGER.addHandler(selenium_handler)
    log.debug(f"Configured the Selenium logger to write to '{selenium_log_path}'")
    

def new_browser(tenant: str, headless: bool, selenium_user_dir: str) -> ChromiumDriver:
    os.makedirs(selenium_user_dir, exist_ok=True)
    debugging_port = find_free_port()
    log.debug(f"Opening new browser: {selenium_user_dir=}, {tenant=}, {debugging_port=}, {headless=}")

    abs_selenium_user_dir = os.path.normpath(os.path.abspath(selenium_user_dir))
    
    options = webdriver.EdgeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--start-maximized")
    options.add_argument(f'user-data-dir={abs_selenium_user_dir}')
    options.add_argument(f"--remote-debugging-port={debugging_port}")
    options.add_argument(f"profile-directory={tenant}")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    options.add_experimental_option("detach", True)
    
    if headless:
        options.add_argument("--headless")
                    
    return webdriver.Edge(options=options)
