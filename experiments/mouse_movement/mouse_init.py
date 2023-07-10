import autopy
import browser_setup
import logging


screen_res= {'width': 0, 'height': 0}

def get_screen_resolution():
    init_x = autopy.mouse.location()[0]
    init_y = autopy.mouse.location()[1]
    autopy.mouse.move(0, 0)
    final_x = 0
    final_y = 0

    for x in range(2100):
        y = 0
        try:
            autopy.mouse.move(x, y)
        except:
            final_x = x - 1
            break

    autopy.mouse.move(0, 0)

    for y in range(2100):
        x = 0
        try:
            autopy.mouse.move(x, y)
        except:
            final_y = y - 1
            break

    autopy.mouse.move(init_x, init_y)
    screen_res['width'] = final_x
    screen_res['height'] = final_y
    logging.info('  Desktop resolution is: width {} and height {}'.format(screen_res['width'], screen_res['height']))
    return screen_res

def get_resolution_difference_factor(driver):
    browser_resolution = browser_setup.get_browser_sizes(driver)
    height_factor = screen_res['height'] / browser_resolution['outer_height']
    width_factor = screen_res['width'] / browser_resolution['inner_width']
    factors= {
        'width_factor': width_factor,
        'height_factor': height_factor
    }
    logging.info('  Desktop/Browser difference factor is:: width factor {} and height factor {}'.format(factors['width_factor'], factors['height_factor']))
    return factors


def init_mouse_pos(x, y):
    autopy.mouse.move(x, y)