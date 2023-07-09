from colorama import Fore, Back, Style, init
import random
import os
import time

color_array = []

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def get_random_number():
    random_number = random.randint(1,4)    
    return random_number

def print_color(number):
    cls()
    match number:
        case 1:
            print(Fore.RED + 'Red')
        case 2:
            print(Fore.BLUE + 'Blue')
        case 3:
            print(Fore.GREEN + 'Green')
        case 4:   
            print(Fore.YELLOW + 'Yellow')

def print_pause():
    cls()
    print(Fore.WHITE + '-------')

def play_array():
    for x in color_array:
        print_color(x)
        time.sleep(2)
        print_pause()
        time.sleep(2)      

def user_input():
    var = 0
    while var != '1' and var != '2' and var != '3' and var != '4' and var != 'q' and var != 'Q':    
        print(Fore.RED + 'Press 1 for Red')
        print(Fore.BLUE + 'Press 2 for Blue')
        print(Fore.GREEN + 'Press 3 for Green')
        print(Fore.YELLOW + 'Press 4 for Yellow')
        print(Fore.WHITE + 'Press Q to quit')
        var = input()
        if var=='q' or var=='Q':
            exit()
    return var          

def check_array():
    i = 1
    for x in color_array:
        cls()
        print(Fore.WHITE + 'What was color number ',i,'?') 
        color = user_input()
        i += 1
        if x != int(color):
            #print("DEBUG: guessed wrong color, 1 returned from check_array method")
            return 1
        else:
            print("That's correct!")
            time.sleep(2) 

def end_game():
    play_again = 0
    print("Better luck next time!")
    while play_again != 'y' and play_again != 'Y' and play_again != 'n' and play_again != 'N':
        print("Do you want to play again? Y or N?")
        play_again = input()
    if  play_again == 'y' or play_again == 'Y':
        color_array.clear()
        start()
    else:
        exit()

def start():
    succes = 0
    while succes != 1:
        number = get_random_number()
        color_array.append(number)
        play_array()   
        succes = check_array()
        #print("DEBUG: the value of succes is ", succes)
        if succes == 1:
            #print("DEBUG: succes is 1, the end_game method is called")
            end_game()
        


init()
start()