import browser_setup
import mouse_init
import mouse_movement
import autopy
import time
from datetime import datetime
import random
import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By




class Web_handler:

    # Variables
    driver = None
    factor = None
    panel_height = 59
    file = None
    frame = []
    minimum_wait = 0.5


    # Constructor
    def __init__(self):
        logging.basicConfig(filename='test.log', filemode='w', level=logging.INFO)
        logging.info('                                                                                                 ')
        logging.info('-------------New Run @ {} --------------------'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        self.file = open("element_info.txt", "w")
        self.driver = browser_setup.setUp()
        screen_res = mouse_init.get_screen_resolution()
        self.factor = (1 / autopy.screen.scale())
        self.panel_height = (browser_setup.get_browser_panel_height(self.driver) * 0.8) * self.factor
        logging.info('  Panel height (factored) is {}'.format(self.panel_height))
        logging.info('  Screen scale factor is {}'.format(self.factor))
        mouse_init.init_mouse_pos((screen_res['width'] / 2), (screen_res['height'] / 2))
        logging.info('-------------Initialization Finished--------------')


    # Functions
    def get(self,url):
        try:
            self.driver.get(url)
        except:
            logging.critical('  Cannot navigate to URL "{}" '.format(url))


    def print_to_file(self, var):
        self.file = open("element_info.txt", "a")
        self.file.write(str(var)+ '\n')
        self.file.close()


    def get_element_by_xpath(self, xpath, timeout=2):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            logging.critical('  Element with xpath {} not found'.format(xpath))
            element = None
        return element


    def get_element_by_id(self, id, timeout=2):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.ID, id)))
        except TimeoutException:
            logging.critical('  Element with id {} not found'.format(id))
            element = None
        return element


    def get_element_by_class(self, class_value, timeout=2):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, class_value)))
        except TimeoutException:
            logging.critical('  Element with class {} not found'.format(class_value))
            element = None
        return element


    def get_element_by_link_text(self, link_text, timeout=2):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.LINK_TEXT, link_text)))
        except TimeoutException:
            logging.critical('  Element with link text {} not found'.format(link_text))
            element = None
        return element


    def visible_in_viewport(self, element):
        check_in_view_script = """var elem = arguments[0];
                                    var bounding = elem.getBoundingClientRect();
                                    return (
                                        bounding.top >= 0 &&
                                        bounding.left >= 0 &&
                                        bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                                        bounding.right <= (window.innerWidth || document.documentElement.clientWidth)
                                    );"""
        is_in_viewport = self.driver.execute_script(check_in_view_script, element)
        logging.info('  Is element {} in viewport?  {}'.format(element, is_in_viewport))
        return is_in_viewport


    def scroll_to_element(self, element, timeout=2):
        logging.info('-------------Scrolling to element {}'.format(element))
        ### The below javascript code scrolls the element in center of screen
        scroll_element_into_center = """var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);""" \
                                     """var elementTop = arguments[0].getBoundingClientRect().top;""" \
                                     """window.scrollBy(0, elementTop-(viewPortHeight/2));"""
        in_view = False
        while not in_view:
            self.driver.execute_script("""document.documentElement.style.scrollBehavior="smooth";""", element)
            self.driver.execute_script(scroll_element_into_center, element)
            in_view = self.visible_in_viewport(element)


    def get_coordinates_and_size_of_element(self, element, record=True):
        script = """var rect = arguments[0].getBoundingClientRect(); return rect;"""
        rect = self.driver.execute_script(script, element)
        if record:
            self.print_to_file(rect)
        logging.info('  Element info:    x {}. y {}, width {}, height {}'.format(rect['x'], rect['y'],rect['width'], rect['height']))
        return rect


    def create_random_coordinate_in_box(self, box):
        x = box['x']
        y = box['y']
        width = (box['width'] * self.factor)
        height = (box['height'] * self.factor)
        startX = x + (width/4)
        endX = x + 3 * (width/4)
        startY = y + (height/4)
        endY = y + 3 * (height/4)
        coordinate= {
            'x': random.uniform(startX, endX),
            'y': random.uniform(startY, endY)
        }
        logging.info('  Random coordinate in Element box: width {} and height {}'.format(coordinate['x'], coordinate['y']))
        return coordinate


    def move_to_id(self, id, record=True, sleep=True):
        if record:
            self.print_to_file(id)
        logging.info('-------------{}--------------'.format(id))
        if sleep:
            time.sleep(random.uniform(self.minimum_wait,2.0))
        element = self.get_element_by_id(id)
        element_rect = self.get_coordinates_and_size_of_element(element)
        coordinate = self.create_random_coordinate_in_box(element_rect)
        mouse_movement.move_mouse_to(autopy.mouse.location()[0], autopy.mouse.location()[1], (coordinate['x'] * self.factor), ((coordinate['y'] * self.factor) + self.panel_height), round(random.uniform(0.1, 1.0), 10))


    def move_to_xpath(self, xpath, record=True, sleep=True):
        if record:
            self.print_to_file(xpath)
        logging.info('-------------{}--------------'.format(xpath))
        if sleep:
            time.sleep(random.uniform(self.minimum_wait,2.0))
        element = self.get_element_by_xpath(xpath)
        element_rect = self.get_coordinates_and_size_of_element(element)
        coordinate = self.create_random_coordinate_in_box(element_rect)
        mouse_movement.move_mouse_to(autopy.mouse.location()[0], autopy.mouse.location()[1], (coordinate['x'] * self.factor), ((coordinate['y'] * self.factor) + self.panel_height), round(random.uniform(0.1, 1.0), 10))


    def move_to_xpath_within_frame(self, xpath, record=True, sleep=True):
        if record:
            self.print_to_file(xpath)
        logging.info('-------------{}--------------'.format(xpath))
        if sleep:
            time.sleep(random.uniform(self.minimum_wait, 2.0))
        element = self.get_element_by_xpath(xpath)
        element_rect = self.get_coordinates_and_size_of_element(element)
        coordinate = self.create_random_coordinate_in_box(element_rect)
        x = 0
        y = 0
        for frame in self.frame:
            x = x + frame['x']
            y = y + frame['y']
        mouse_movement.move_mouse_to(autopy.mouse.location()[0], autopy.mouse.location()[1],
                                     ((coordinate['x'] + x) * self.factor),
                                     (((coordinate['y'] + y) * self.factor) + self.panel_height),
                                     round(random.uniform(0.1, 1.0), 10))

    def click(self):
        autopy.mouse.click()
        logging.info('-------------#CLICK#-----------------------')


    def switch_to_frame(self, xpath, timeout, record=True):
        if record:
            self.print_to_file(xpath)
        frame = self.get_element_by_xpath(xpath, timeout)
        self.scroll_to_element(frame)
        self.move_to_xpath(xpath)
        frame_info = self.get_coordinates_and_size_of_element(frame)
        self.frame.append(frame_info)
        self.driver.switch_to.frame(frame)


    def switch_from_frame(self):
        self.driver.switch_to.parent_frame()
        self.frame.pop()


    def type(self, word):
        autopy.mouse.click()
        logging.info('-------------Typing {}-----------------------'.format(word))
        for letter in word:
            time.sleep(random.uniform(0.1, 0.1))
            autopy.key.type_string(letter)


    def click_and_move_to_xpath(self,xpath):
        self.click()
        self.move_to_xpath(xpath, sleep=False)


    def stop(self):
        self.driver.quit()