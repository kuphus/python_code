import os
import math


array_of_arrays = [[1]]

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def get_input():
    number = input("Pick a number to be printed: ")
    return int(number) 


def add_right(current, length):
    for i in range(current+1, current+length+1):
        array_of_arrays[-1].append(i)


def add_left(current, length):
    for i in range(current+1, current+length+1):
        array_of_arrays[0].insert(0,i)


def add_down(current, length):
    array_index = 1
    current_available_height = len(array_of_arrays) - 1
    for i in range(current+1, current+length+1):
        if current_available_height == 0:  
            array_of_arrays.append([i])
        else:
            array_of_arrays[array_index].insert(0,i)           
            array_index += 1
            current_available_height -= 1


def add_up(current, length):  
    array_index =  -2 
    current_available_height = len(array_of_arrays) - 1
    for i in range(current+1, current+length+1):
        if current_available_height == 0:  
            array_of_arrays.insert(0,[i])
        else:
            array_of_arrays[array_index].append(i)   
            array_index -= 1
            current_available_height -= 1
                   

def add_empty_left(amount, max_number):
    for i in range(amount):
        if max_number < 10: 
            array_of_arrays[0].insert(0," ")
        elif max_number < 100:
            array_of_arrays[0].insert(0,"  ")
        elif max_number < 1000:
            array_of_arrays[0].insert(0,"   ")        


def add_empty_down(max_number):
    width = get_array_width()
    for array in array_of_arrays:
        if len(array) != width:
            if max_number < 10: 
                array.insert(0," ")
            elif max_number < 100:
                array.insert(0,"  ")
            elif max_number < 1000:
                array.insert(0,"  ")


def fill_array_of_arrays(max_number):
    length = 1
    current = 1
    while current < max_number:
        if current + length <= max_number:
            add_right(current, length)
            current += length
        elif current != max_number:
            new_length = max_number - current
            add_right(current, new_length)   
            current += new_length                
        if current + length <= max_number:
            add_up(current, length)        
            current += length
            if current == max_number:
                white = get_array_width()-1
                add_empty_left(white, max_number)
        elif current != max_number:
            new_length = max_number - current
            add_up(current, new_length)      
            current += new_length                    
        length += 1
        if current + length <= max_number:
            add_left(current, length)
            current += length
            if current == max_number:
                add_empty_down(max_number)    
        elif current != max_number:
            new_length = max_number - current
            add_left(current, new_length)    
            current += new_length                
            width = get_array_width()
            extra = width - (new_length + 1)
            add_empty_left(extra, max_number)
        if current + length <= max_number:
            add_down(current, length)
            current += length
        elif current != max_number:
            new_length = max_number - current
            add_down(current, new_length)       
            current += new_length   
            add_empty_down(max_number) 
        length += 1  
        


def get_array_width():
    width = 0
    for array in array_of_arrays:
        if len(array)>width:
            width = len(array)
    return width


def print_array(max_number):
    cls()
    width_max = get_array_width()
    for array in array_of_arrays:
        length = len(array)
        difference = width_max - length
        temp_string = ""
        for number in array:
            if isinstance(number, int):
                if number < 10 and 10 <= max_number < 100:
                    number = "0" + str(number)
                elif number < 10 and 100 <= max_number < 1000:        
                    number = "00" + str(number)            
                elif 10 <= number < 100 and  100 <= max_number < 1000:
                    number = "0" + str(number)
            temp_string = temp_string + " " + str(number)     
        print(temp_string)


def start():
    number = get_input()
    fill_array_of_arrays(number)
    print_array(number)



start()