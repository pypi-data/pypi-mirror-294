from platform import system
from shutil import which
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.edge.service import Service as EdgeService

def set_browser() -> webdriver:
    # Detect the operating system
    os_name = system().lower()
    
    # Initialize a list to check available browsers in priority order
    available_browsers = []

    # Check for Firefox
    if which("firefox"):
        available_browsers.append('firefox')
    
    # Check for Chrome/Chromium
    if which("chrome") or which("chromium"):
        available_browsers.append('chrome')
    
    # Check for Safari (only available on macOS)
    if os_name == "darwin" and which("safaridriver"):
        available_browsers.append('safari')
    
    # Check for Microsoft Edge (only available on Windows)
    if os_name == "windows" and which("msedge"):
        available_browsers.append('edge')

    # Initialize WebDriver in priority order: Firefox > Chrome > Safari > Edge
    if 'firefox' in available_browsers:
        return webdriver.Firefox(service=FirefoxService())
    elif 'chrome' in available_browsers:
        return webdriver.Chrome(service=ChromeService())
    elif 'safari' in available_browsers:
        return webdriver.Safari(service=SafariService())
    elif 'edge' in available_browsers:
        return webdriver.Edge(service=EdgeService())
    else:
        raise EnvironmentError("No supported browsers found on the system. Please install Firefox, Chrome, Safari, or Edge.")

