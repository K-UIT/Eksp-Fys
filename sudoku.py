from abc import ABC, abstractmethod


class Sudoku(ABC):
    """Generic (abstract) representation of Sudoku board"""

    def __init__(self, initial_board: list[list[int]], box_width: int, box_height: int):
        self.board=initial_board
        self.b_width=box_width
        self.b_height=box_height
        self.dimension=box_width*box_height
        
        if not self._validate_board_dimensions: # Checking if dimensions are valid
            raise ValueError("Board dimensions are invalid")

    def _validate_board_dimensions(self) -> bool:
        """Validate dimensions of initial board
        Board should be square and compatible with box width and height.
        """
        if int(self.number_elements**0.5)!=self.dimension:
            return False # Checking if the number of elements is correct
        
        root=int(self.dimension**0.5)
        if root**2==self.dimension: # Checking if we are dealing with square boxes
            height=length=root
        else:
            for i in range(1,root+1): # Trying to find the largest box combo
                if self.dimension%i==0:
                    length, height = self.dimension//i, i
        
        if height!=self.b_height or length!=self.b_width:
            return False # If height and length wrong return false
        return True




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
        """Neat looking readable sudoku board formatter"""
        board = ""
        for row_id, row in enumerate(self.board):
            for square_id, square in enumerate(row):
                board += str(square) + " "
                if (square_id + 1) % self.b_width == 0 and square_id != self.dimension - 1:
                    board += "| "
                elif square_id == self.dimension - 1:
                    board += "\n"
    
            if (row_id + 1) % self.b_height == 0 and row_id != self.dimension - 1:
                for box_id in range(0, self.dimension // self.b_width):
                    board += "--" * self.b_width
                    if box_id < self.dimension // self.b_width - 1:
                        board += "|-"
                    if box_id == self.dimension // self.b_width - 1:
                        board += "\n"
    
        return board


# Subclass of Sudoku
class Sudoku_4x4(Sudoku):
    def __init__(self, board: list[list[int]]): # Initiating the board
        super().__init__(board, box_width = 2, box_height= 2)

    def __str__(self) -> str: # Printing out a general board
        return super().__str__()



# Subclass of Sudoku
class Sudoku_6x6(Sudoku):
    def __init__(self, board: list[list[int]]): # Initiating the board
        super().__init__(board, box_width = 3, box_height= 2)
    
    def __str__(self) -> str: # Printing out a general board
        return super().__str__()


# Subclass of Sudoku
class Sudoku_9x9(Sudoku):
    def __init__(self, board: list[list[int]]): # Initiating the board
        super().__init__(board, box_width = 3, box_height= 3)
    
    
    def __str__(self) -> str: # Printing out a general board
        return super().__str__()


class Square:
    """A single square of a Sudoku board"""

    def __init__(self, value: int, row: "Row", column: "Column", box: "Box"):
        self.value=value
        self.row=row
        self.column=column
        self.box=box
        self.possible = []
    def possible_values(self) -> list[int]:
        for val in range(1,Sudoku.dimension):
            if val not in self.possible:
                self.possible.append(val)
        return self.possible







class Element(ABC):
    """Generic Sudoku element containing a collection of squares"""

    def __init__(self):
        self.elements=[]

    def _add_square(self, square: Square) -> None:
        if square not in self.elements:
            self.elements.append(square)

    def values(self) -> list[int]:
        """Return values of squares that have been filled in"""
        
        return [square.value for square in self.elements if square.value>0]

    @abstractmethod  # This method must be implemented by subclasses
    def __str__(self) -> str:
        """Return string representation of the element"""
        pass


# Subclass of Element
# Should implement __str__ to print as a horizontal row
class Row(Element):
    pass


# Subclass of Element
# Should implement __str__ to print as a vertical column
class Column(Element):
    pass


# Subclass of Element
# Should implement __str__ to print as a box
class Box(Element):
    pass


# Some prelogic to set up the board as a list of lists
def clean(brett): # This method won't work for boards >9 but that's okay 
    brett=list(map(int,brett.replace(".","0").replace("\n",""))) # Making the str into a list of ints
    dim = int(len(brett)**0.5) # as the board is nxn we can do this to find the dimension
    if dim**2 != len(brett):
        raise ValueError("Not square board")
    clean_brett=[]
    for i in range(0,dim**2,dim): # Splitting every column into it's own list
        clean_brett.append(brett[i:i+dim])
    return clean_brett



if __name__=="__main__":
    brett = input("Give a board: ")
    clean_brett = clean(brett)
