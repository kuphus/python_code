from tkinter import Button, Label
import random
import settings

class Cell:
    
    all = []
    mines = []
    cell_count = settings.board_columns*settings.board_rows
    mine_count = settings.mines_count
    cell_count_label_object=None
    mine_count_label_object=None
    
    
    def __init__(self, x, y, is_mine=False):
        self.x = x
        self.y = y
        self.is_mine = is_mine
        self.is_opened = False
        self.is_marked = False
        self.button_gui = None
        Cell.all.append(self)
    
    
    def create_button_gui(self, location):
        btn_gui = Button(
            location,
            width=2,
            height=1,
            bg="white",
        )
        btn_gui.bind('<Button-1>', self.open_cell)
        btn_gui.bind('<Button-3>', self.mark_cell)
        self.button_gui = btn_gui
        
        
    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg="black",
            fg="white",
            text="Cells left: {}".format(Cell.cell_count)
        )
        Cell.cell_count_label_object = lbl
    
    
    @staticmethod
    def create_mine_count_label(location):
        lbl = Label(
            location,
            bg="black",
            fg="white",
            text="Mines left: {}".format(Cell.mine_count)
        )
        Cell.mine_count_label_object = lbl
    
    
    @staticmethod
    def create_lost_game_label(location):
        lbl = Label(
            location,
            bg="black",
            fg="white",
            text="You Lost the Game!!!"
        )
        
        
    def open_cell(self, event):
        if not self.is_marked:
            if self.is_mine:
                self.show_mines()
            else:
                if self.get_surrounding_mines == 0:
                    for cell in self.get_surrounded_cells:
                        cell.show_cell()
                        self.show_cell()
                else:
                    self.show_cell()
            self.button_gui.unbind('<Button-1>')
            self.button_gui.unbind('<Button-3>')
            #TODO: win message if it's the last not mine cell (open cells equal to amount of mines)
        
    
    def mark_cell(self, event):
        if not self.is_opened:
            if not self.is_marked:
                self.button_gui.configure(
                    bg="yellow"
                )
                Cell.mine_count -= 1
                if Cell.mine_count_label_object:
                    Cell.mine_count_label_object.configure(text="Mines left: {}".format(Cell.mine_count))
                self.is_marked = True
            else:
                self.button_gui.configure(
                    bg="white"
                )
                Cell.mine_count += 1
                if Cell.mine_count_label_object:
                    Cell.mine_count_label_object.configure(text="Mines left: {}".format(Cell.mine_count))
                self.is_marked = False
                
    
    def show_mines(self):
        #TODO:interrupt the game, show all mines, display message.
        self.button_gui.configure(
            bg="red",
            text="*"
        )
        for mine in Cell.mines:
            mine.button_gui.configure(
                bg="red",
                text="*"
            )
        Cell.create_mine_count_label()
      
      
    def get_cell_by_coordinates(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
        
    
    @property
    def get_surrounded_cells(self):
        surrounding_cells = [
            self.get_cell_by_coordinates(self.x - 1, self.y - 1),
            self.get_cell_by_coordinates(self.x - 1, self.y),
            self.get_cell_by_coordinates(self.x - 1, self.y + 1),
            self.get_cell_by_coordinates(self.x, self.y - 1),
            self.get_cell_by_coordinates(self.x, self.y + 1),
            self.get_cell_by_coordinates(self.x + 1, self.y - 1),
            self.get_cell_by_coordinates(self.x + 1, self.y),
            self.get_cell_by_coordinates(self.x + 1, self.y + 1)
        ]
        surrounding_cells = [cell for cell in surrounding_cells if cell is not None]
        return surrounding_cells
    
    
    @property
    def get_surrounding_mines(self):
        surrounding_mines = 0
        for cell in self.get_surrounded_cells:
            if cell.is_mine:
                surrounding_mines += 1  
        return surrounding_mines
    
    
    def show_cell(self):
        if not self.is_opened:
            self.button_gui.configure(
                text = self.get_surrounding_mines 
            )
            Cell.cell_count -= 1
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text="Cells left: {}".format(Cell.cell_count))
            self.is_opened = True
        
        
    @staticmethod
    def randomize_mines(amount_mines):
        mines = random.sample(Cell.all, amount_mines)
        for mine in mines:
            mine.is_mine = True
            Cell.mines.append(mine)
            
    
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
        
        
class Board:
    
    def __init__(self, location, columns, rows, mines):
        self.columns = columns
        self.rows = rows
        for x in range(columns):
            for y in range(rows):
                cell = Cell(x, y)
                cell.create_button_gui(location)
                cell.button_gui.grid(
                    column=x, row=y
                )
        Cell.randomize_mines(mines)
