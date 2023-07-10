import math
import random
import autopy
import logging



def getBezierX(t, startX, ctrl_point1X, ctrl_point2X, endX):
    '''
    Based on the X coordinates of the starting point, the first control point, the second control point,
    and the end point, this function will return the X coordinate of the curve on moment t
    '''
    x = math.pow(1-t,3) * startX + 3 * t * math.pow(1 - t, 2) * ctrl_point1X + 3 * t * t * (1 - t) * ctrl_point2X + t * t * t * endX
    logging.debug('  Input: t {}, startX {}, ctrlp1_X {}, ctrlp2_X {}, endX {}'.format(t,startX,ctrl_point1X,ctrl_point2X,endX))
    logging.debug('  Bezier X-coordinate is {}'.format(x))
    return x


def getBezierY(t, startY, ctrl_point1Y, ctrl_point2Y, endY):
    '''
    Based on the Y coordinates of the starting point, the first control point, the second control point,
    and the end point, this function will return the Y coordinate of the curve on moment t
    '''
    y = math.pow(1-t,3) * startY + 3 * t * math.pow(1 - t, 2) * ctrl_point1Y + 3 * t * t * (1 - t) * ctrl_point2Y + t * t * t * endY
    logging.debug('  Input: t {}, startY {}, ctrlp1_Y {}, ctrlp2_Y {}, endY {}'.format(t, startY, ctrl_point1Y, ctrl_point2Y, endY))
    logging.debug('  Bezier Y-coordinate is {}'.format(y))
    return y


def getBezierXandY(t, startX, startY, ctrl_point1X, ctrl_point1Y, ctrl_point2X, ctrl_point2Y, endX, endY):
    '''
    Based on the X and Y coordinates of the starting point, the first control point, the second control point,
    and the end point, this function will return the X and Y coordinates of the curve on moment t as a dictionary
    '''
    coordinate= {
        'x': getBezierX(t, startX, ctrl_point1X, ctrl_point2X, endX),
        'y': getBezierY(t, startY, ctrl_point1Y, ctrl_point2Y, endY)
    }
    return coordinate


def create_control_point(startX, startY, endX, endY, percentage=0.3):
    '''
    out_of_bound is a value for how far beyond the straight line between start and finish the value might be extended.
    Generates a random X and Y coordinate between the start and end point + out_of_bound and returns these values in a dictionary.
    The percentage parameter should be a float between 0 and 1.
    '''
    if(percentage > 0 and percentage <= 1):
        extra_X = (abs(startX - endX)) * percentage
        side_X = extra_X / 2
        if(endX > startX):
            endX = endX + side_X
            startX = startX - side_X
        else:
            endX = endX - side_X
            startX = startX + side_X
        extra_Y = (abs(startY - endY)) * percentage
        side_Y = extra_Y / 2
        if(endY > startY):
            endY = endY + side_Y
            startY = startY - side_Y
        else:
            endY = endY - side_Y
            startY = startY + side_Y

    coordinate= {
        'x': random.uniform(startX, endX),
        'y': random.uniform(startY, endY)
    }
    logging.info('  Control point created at: x {} and y {}'.format(coordinate['x'], coordinate['y']))
    return coordinate


def get_length(startX, startY, endX, endY):
    '''
    Calculates the length of a line based on the difference in X coordinates and Y coordinates according to
    Pythagorean theorem
    '''
    length = math.sqrt(math.pow(abs(startX - endX),2) + math.pow(abs(startY - endY), 2))
    logging.info('  Line length is {}'.format(length))
    return length


def array_with_equal_distance(start, finish, steps):
    steps_array = [float(start)]
    distance = abs(finish - start)
    step_value = distance / steps
    travelled = start
    for step in range(0, steps):
        travelled = travelled + step_value
        steps_array.append(travelled)
    return steps_array


def create_variable_speed_array(speed):
    '''
    Speed up to half the difference, then slow down the second half, using steps as the first step
    '''
    steps = []
    a = (speed/2) / -0.25
    b = -a
    loop_steps = array_with_equal_distance(0 , int(speed/2), int(speed/2))
    for y in loop_steps:
        c = -y          # since c = 0, every increase in y is the same decrease in c
        x_plus = (-b + (math.sqrt((b * b) - 4 * (a * c) ))) / (2 * a)
        x_min = (-b - (math.sqrt((b * b) - 4 * (a * c) ))) / (2 * a)
        steps.append(abs(x_plus))
    # now mirror the values
    max_index = len(steps) - 1
    for index in range(max_index, 0, -1):
        if(index>0):
            difference = steps[index] - steps[index-1]
            new_value = steps[len(steps)-1] + abs(difference)
            steps.append(new_value)
        else:
            steps.append(0.0)
    steps.append(1)
    return steps

def move_mouse_to(startX, startY, endX, endY, percentage):
    '''
    Moves the mouse from start coordinate to end coordinate with a bezier curve.
    percentage is the percentage amount the two control points may be outside the straight line.
    '''
    logging.info('  Moving mouse to {}, {}'.format(endX, endY))
    length = get_length(startX, startY, endX, endY)
    steps = create_variable_speed_array(int(length)/2)    # the speed of the movement
    logging.debug('  Steps / speed array '.format(steps))
    control_point1 = create_control_point(startX, startY, endX, endY, percentage)
    control_point2 = create_control_point(startX, startY, endX, endY, percentage)
    logging.debug('  Mouse steps:')
    for step in steps:
        coordinate_at_t = getBezierXandY(step, startX, startY, control_point1['x'], control_point1['y'], control_point2['x'], control_point2['y'], endX, endY)
        logging.debug('  Moving mouse to {}, {}'.format(coordinate_at_t['x'], coordinate_at_t['y']))
        autopy.mouse.smooth_move(coordinate_at_t['x'], coordinate_at_t['y'])
