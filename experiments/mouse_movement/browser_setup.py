from selenium import webdriver
import logging


# Setup settings
def setUp():
    profile = setUpProfile()  # for setup profiles
    options = setUpOptions()  # options for running gecko
    capabilities = setUpCapabilities()  # enable some abilities like marionette
    #capabilities = setUpProxy(capabilities)  # setup proxy if you get ban
    driver = webdriver.Firefox(options=options, capabilities=capabilities, firefox_profile=profile)  # initialize web driver
    driver.maximize_window()
    return driver


def setUpProfile():
    profile = webdriver.FirefoxProfile()
    #profile.add_extension("buster_captcha_solver_for_humans-0.6.0.xpi")  # add buster extension path
    profile.set_preference("security.fileuri.strict_origin_policy", False)  # disable Strict Origin Policy
    profile.update_preferences()  # Update profile with new configs
    return profile


def setUpOptions():
    options = webdriver.FirefoxOptions()
    #options.headless = True
    return options


# Enable Marionette, An automation driver for Mozilla's Gecko engine
def setUpCapabilities():
    capabilities = webdriver.DesiredCapabilities.FIREFOX
    capabilities['marionette'] = True
    return capabilities


# Setup proxy
def setUpProxy(capabilities):
    PROXY = '1.1.1.1:70'
    capabilities['proxy'] = {"proxyType": "MANUAL", "httpProxy": PROXY, "ftpProxy": PROXY, "sslProxy": PROXY}
    return capabilities


def get_browser_panel_height(driver):
    panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
    logging.info('  Panel height is: {}'.format(panel_height))
    return panel_height


def get_browser_sizes(driver):
    inner_height = driver.execute_script('return window.innerHeight;')
    inner_width = driver.execute_script('return window.innerWidth;')
    browser = driver.get_window_size()
    browser_data= {
        'inner_height': inner_height,
        'inner_width': inner_width,
        'outer_height': browser['height'],
        'outer_width': browser['width']
    }
    logging.info('  Browser sizes are: outer width {} and  outer height {},  inner width {} and inner height {}'.format(browser['width'], browser['height'], inner_width, inner_height))
    return browser_data


def get_pixel_ratio(driver):
    ratio = driver.execute_script('return window.devicePixelRatio;')
    logging.info('  Device pixel ratio is {}'.format(ratio))
    return ratio


def get_screen(driver):
    screen_width = driver.execute_script('return screen.width;')
    screen_height = driver.execute_script('return screen.height;')
    screen= {
        'width': screen_width,
        'height': screen_height
    }
    return screen