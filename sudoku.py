from abc import ABC, abstractmethod


class Sudoku(ABC):
    """Generic (abstract) representation of Sudoku board"""

    def __init__(self, initial_board: list[list[int]], box_width: int, box_height: int):
        self.board=initial_board
        self.b_width=box_width
        self.b_height=box_height
        self.dimension=box_width*box_height
    def _validate_board_dimensions(self):
        """Validate dimensions of initial board

        Board should be square and compatible with box width and height.
        """
        pass

    def _set_up_board(self):
        """Initialize squares and elements (rows, columns, boxes) of the board"""
        pass

    def _validate_board_values(self):
        """Validate values of board (no repeated values within elements)"""
        pass

    @abstractmethod  # This method must be implemented by subclasses
    def solve(self) -> list[list[int]]:
        """Solve Sudoku and return board with all values filled in"""
        pass

    @abstractmethod  # This method must be implemented by subclasses
    def __str__(self) -> str:
        board = ""
        for row_id, row in enumerate(self.board): # Going through every row
            for square_id, square in enumerate(row):
                board += str(square) + " "
                if (square_id + 1) % self.b_width == 0 and square_id != self.dimension - 1:
                    board += "| "
                elif square_id == self.dimension - 1:
                    board += "\n"
            if (row_id + 1) % self.b_height == 0 and row_id != self.dimension - 1:
                for box_id in range(0, self.dimension // self.b_width):
                    board += "--" * self.b_width
                    if box_id % (self.b_width + 1) == 0 and box_id != self.dimension - 1:
                        board += "|"
                    elif box_id == self.dimension // self.b_width - 1:
                        board += "\n"
        return board


# Subclass of Sudoku
class Sudoku_4x4:
    pass


# Subclass of Sudoku
class Sudoku_6x6:
    pass


# Subclass of Sudoku
class Sudoku_9x9:
    pass


class Square:
    """A single square of a Sudoku board"""

    def __init__(self, value: int, row: "Row", column: "Column", box: "Box"):
        self.value=value
        self.row=row
        self.column=column
        self.box=box
        self.sees=row+column+box

    def possible_values(self) -> list[int]:
        possible = []
        for val in range(1,10):
            if val not in self.sees:
                possible.append(val)
        return possible


class Element(ABC):
    """Generic Sudoku element containing a collection of squares"""

    def __init__(self):
        pass

    def _add_square(self, square: Square) -> None:
        pass

    def values(self) -> list[int]:
        """Return values of squares that have been filled in"""
        return []  # Placeholder

    @abstractmethod  # This method must be implemented by subclasses
    def __str__(self) -> str:
        """Return string representation of the element"""
        pass


# Subclass of Element
# Should implement __str__ to print as a horizontal row
class Row:
    pass


# Subclass of Element
# Should implement __str__ to print as a vertical column
class Column:
    pass


# Subclass of Element
# Should implement __str__ to print as a box
class Box:
    pass


# Some prelogic to set up the board as a list of lists
def clean(brett): # This method won't work for boards >9 but that's okay 
    brett=list(map(int,brett.replace(".","0").replace("\n",""))) # Making the str into a list of ints
    dim = int(len(brett)**0.5) # as the board is nxn we can do this to find the dimension
    if dim**2 != len(brett):
        raise ValueError("Non-square board")
    clean_brett=[]
    for i in range(0,dim**2,dim): # Splitting every column into it's own list
        clean_brett.append(brett[i:i+dim])
    return dim, clean_brett

# Prelogic finding the mxn box sizes for non square boxes
def size(dim):
    root=int(dim**0.5)
    if root**2==dim: # Checking if we are dealing with square boxes
        height=length=root
    else:
        for i in range(1,root+1): # Trying to find the largest box combo
            if dim%i==0:
                length, height = dim//i, i    
    return length, height


if __name__=="__main__":
    brett = input("Give a board: ")
    dim, clean_brett = clean(brett)
    length, height = size(dim)
    print(height)
    print(length)
    print(clean_brett)
    
    test = Sudoku(clean_brett, length, height)    
    print(test)



