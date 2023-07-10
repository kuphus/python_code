from tkinter import *
from cell import Cell, Board
import settings
import utility

root = Tk()
# Window configurations
root.geometry("{}x{}".format(settings.window_width, settings.window_height))
root.title("MaainSwiepur")
root.resizable(False, False)
root.configure(bg="black")

top_frame = Frame(
    root,
    bg="black",
    width=settings.window_width,
    height=utility.calc_perc(settings.window_height, 15)
)
top_frame.place(x=0, y=0)

left_frame = Frame(
    root,
    bg="black",
    width=utility.calc_perc(settings.window_width, 20),
    height=utility.calc_perc(settings.window_height, 85)
)
left_frame.place(x=0, y=utility.calc_perc(settings.window_height, 15))

center_frame = Frame(
    root,
    bg="black",
    width=utility.calc_perc(settings.window_width, 80),
    height=utility.calc_perc(settings.window_height, 85)
)
center_frame.place(x=utility.calc_perc(settings.window_width, 20), y=utility.calc_perc(settings.window_height, 15))

game_title = Label(
    top_frame,
    bg="black",
    fg="white",
    text="Maainsweepur",
    font=("", 40)
)
game_title.place(
    x=utility.calc_perc(settings.window_width, 15),
    y=5
)

board = Board(center_frame, settings.board_columns, settings.board_rows, settings.mines_count)

Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x=10, y= 40)

Cell.create_mine_count_label(left_frame)
Cell.mine_count_label_object.place(x=10, y= 60)

# Run the window
root.mainloop()