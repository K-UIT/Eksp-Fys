from abc import ABC, abstractmethod


class Sudoku(ABC):
    """
    Generic (abstract) representation of Sudoku board
    """

    def __init__(self, initial_board: list[list[int]], box_width: int, box_height: int):
        # Setting up dimensions of everything
        self.board=initial_board
        self.b_width=box_width
        self.b_height=box_height
        self.dimension=box_width*box_height
        self.number_elements=sum(len(row) for row in initial_board)
        
        # Generating rows,boxes and columns as empty objects I can link to later
        self.Rows  = [Row(n,    self.b_width)  for n in range(0,self.dimension)]
        self.Cols  = [Column(n, self.b_height) for n in range(0,self.dimension)]
        self.Boxes = [Box(n,    self.b_width)  for n in range(0,self.dimension)]
        
        # Checking if dimension is valid before moving forward
        if not self._validate_board_dimensions():
            raise ValueError("Board dimensions are invalid")
        
        # Setting up the board
        self._set_up_board()
            
    def _validate_board_dimensions(self) -> bool:
        """Validate dimensions of initial board
        Board should be square and compatible with box width and height.
        """
        # Checking if the number of elements is correct
        if int(self.number_elements**0.5)!=self.dimension:
            return False
        
        # Checking if we are dealing with square boxes
        root=int(self.dimension**0.5)
        if root**2==self.dimension:
            height=length=root
        
        # If not square, then we are dealing with nx(n+1) boxes
        else:
            for i in range(1,root+1): # Trying to find the largest box combo
                if self.dimension%i==0:
                    length, height = self.dimension//i, i
        
        # Just checking if we ended up with the same value we fed into the code
        if height!=self.b_height or length!=self.b_width:
            return False
        return True

    def _set_up_board(self) -> None:
        """
        Initialize squares and elements (rows, columns, boxes) of the board
        """
        # We need the coordinates of all rows, columns and boxes
        for row_id, row in enumerate(self.board):
            for col_id, value in enumerate(row):
                # Flattening the current box coordinates so it can go in our 1d list
                box_id=(row_id//self.b_height)*(self.dimension//self.b_width)\
                        +col_id//self.b_width
                
                # Using the coordinates to generate square objects
                square = Square(value, self.Rows[row_id], self.Cols[col_id], self.Boxes[box_id], value!=0) 
                
                # Connecting everything together
                self.board[row_id][col_id]= square     # Swapping ints with objects
                self.Rows[row_id]._add_square(square)  # Connecting rows
                self.Cols[col_id]._add_square(square)  # Connecting columns
                self.Boxes[box_id]._add_square(square) # Connecting boxes
                
    def _validate_board_values(self) -> bool:
        """
        Validate values of board (no repeated values within elements)
        """
        for row in self.Rows: # Checking rows for uniqueness
            vals = row.values()
            if len(vals) != len(set(vals)):
                return False

        for col in self.Cols: # Checking columns for uniqueness
            vals = col.values()
            if len(vals) != len(set(vals)):
                return False
        
        for box in self.Boxes: # Checking boxes for uniqueness
            vals = box.values()
            if len(vals) != len(set(vals)):
                return False
            
        return True # If nothing was catched then it must be a valid boardstate
    
    
    def _filled_out(self) -> bool:
        """
        Check if the board has any empty spaces in it
        """
        # Goes through every square looking for any zeros
        for row in self.board:
            for sq in row:
                if sq.value==0:
                    return False
        return True # If there are no zeros in the board it must be filled
    
    
    def solve(self) -> bool:
        """
        Generic recursive solving algorithm (for any board size)
        """
        
        # Checking if we are done
        if self._filled_out():
            return self._validate_board_values()
    
        # Find first empty square
        for row in self.board:
            for sq in row:
                if sq.value == 0:
                    
                    # Set found zero to be possible values
                    for val in sq.possible_values(): 
                        sq.value = val
                        
                        # If it's valid then preform recursive step
                        if self._validate_board_values(): 
                            if self.solve():
                                return True
                        
                        # If nothing is valid here, backtrack
                        sq.value = 0
                    return False  # no valid value fits here
    @abstractmethod
    def __str__(self) -> str: # I wrote this code before I saw it was abstract, whoopsies
        """
        Neat looking readable sudoku board formatter
        """
        
        board = "" # Staring board is empty
        
        # Adds row objects 
        for row_id, row in enumerate(self.Rows):
            board += str(row) + "\n"
            
            # If we have passed the end of a box add some horisontal lines
            if (row_id+1)%self.b_height==0 and (row_id+1)!=self.dimension:
                for _ in range(int(self.dimension**0.5)): # This won't work for n>9
                    board+="--"*self.b_width +"|-"

                board =board[:-2]+"\n" # Really messy way but works

        return board


# Subclass of Sudoku representing a 4x4 board
class Sudoku_4x4(Sudoku):
    def __init__(self, board: list[list[int]]): # Initiating the board
        super().__init__(board, box_width = 2, box_height= 2)
        
    def solver(self):
        print("Solving 4x4 board\n Starting board:")
        print(self) # Printing at the start
        self.solve()
        print("Done!")
        print(self) # Printing at the end 
    
    def __str__(self) -> str: # Printing out a general board
        return super().__str__()


# Subclass of Sudoku representing a 6x6 board
class Sudoku_6x6(Sudoku):
    def __init__(self, board: list[list[int]]): # Initiating the board
        super().__init__(board, box_width = 3, box_height= 2)
    
    def solver(self):
        print("Solving 6x6 board\n Starting board:")
        print(self) # Printing at the start
        self.solve()
        print("Done!")
        print(self) # Printing at the end 
    
    def __str__(self) -> str: # Printing out a general board
        return super().__str__()


# Subclass of Sudoku representing a 9x9 board
class Sudoku_9x9(Sudoku):
    def __init__(self, board: list[list[int]]): # Initiating the board
        super().__init__(board, box_width = 3, box_height= 3)
    
    def solver(self):
        print("Solving 9x9 board\n Starting board:")
        print(self) # Printing at the start
        self.solve()
        print("Done!")
        print(self) # Printing at the end 
            
    
    def __str__(self) -> str: # Printing out a general board
        return super().__str__()


class Square:
    """
    A single square of a Sudoku board
    """

    def __init__(self, value: int, row: "Row", column: "Column", box: "Box", locked: bool):
        # Every square knows this
        self.value=value      # The squares value        (0->n)
        self.row=row          # The squares row index    (0->n-1)
        self.column=column    # The squares column index (0->n-1)
        self.box=box          # The squares box index    (0->n-1)
        self.locked = locked  # If the square had a value when setting up the board
        
    def possible_values(self) -> list[int]:
        """
        All possible values the square can be
        """
        possible = []
        
        # Checks if any of the values from 1-n are already in the squares row, column or box
        for val in range(1,len(self.row.elements)+1):
            if val not in self.row.values() and val not in self.column.values() and val not in self.box.values():
                possible.append(val)
            
        return possible


class Element(ABC):
    """
    Generic Sudoku element (Abstract) containing a collection of squares
    """

    def __init__(self):
        self.elements=[] # All the elements squares

    def _add_square(self, square: Square) -> None:
        """
        Adds a square object to the elements if it's not there already
        """
        if square not in self.elements:
            self.elements.append(square)

    def values(self) -> list[int]:
        """
        Return values of squares that have been filled in
        """
        return [square.value for square in self.elements if square.value>0]

    @abstractmethod  # This method must be implemented by subclasses
    def __str__(self) -> str:
        """
        Return string representation of the element
        """
        pass


# Subclass of Element representing a single row
# Should implement __str__ to print as a horizontal row
class Row(Element):
    def __init__(self, row_id, length):
        super().__init__()  # Calling for elements
        self.id=row_id      # Defining its row id
        self.length=length  # Defining how long a box should be

    def __str__(self):
        """
        Prints out an entire row with seperators between boxes
        """
        output="" # Starting row string is empty
        
        # Adds every square in a row element to the string
        for sq_id, square in enumerate(self.elements):
            output += str(square.value) +" "
            
            # Seperates row "chunks" in different boxes 
            if (sq_id+1)%self.length==0 and (sq_id+1)!=len(self.elements):
                output += "| "
        return output


# Subclass of Element representing a single column
# Should implement __str__ to print as a vertical column
class Column(Element):
    def __init__(self, col_id, height):
        super().__init__()  # Calling for elements
        self.id=col_id      # Defining its row id
        self.height=height  # Defining how long a box should be
        
    def __str__(self):
        """
        Prints out an entire row with seperators between boxes
        """
        output="" # Starting column string is empty
        
        # Adds every square in a column element to the string
        for sq_id, square in enumerate(self.elements):
            output += str(square.value) +"\n"
            
            # Seperate columns "chunks" if different boxes 
            if (sq_id+1)%self.height==0 and (sq_id+1)!=len(self.elements):
                output += "-\n"
        return output


# Subclass of Element representing a single box
# Should implement __str__ to print as a box
class Box(Element):
    def __init__(self, box_id, width):
        super().__init__()  # Calling for elements
        self.box_id=box_id  # Defining its box id
        self.width=width    # How wide the box is
        
    def __str__(self):
        """
        Prints out an entire box
        """
        output="" # Starting box string is empty
        
        # Adding every square on the box to the string
        for sq_id, square in enumerate(self.elements):
            output+=str(square.value)
            
            # Going to a new line if we are at the end of the box
            if (sq_id+1)%self.width==0 and (sq_id+1)!=len(self.elements):
                output+= "\n"
        output += "\n"
        return output


def clean(brett:str)-> list[list[int]]: # This method won't work for boards >9 but that's okay
    """
    Some prelogic to set up the board as a list of lists from a string
    """
    # Making the string into a list of intigers
    brett=list(map(int,brett.replace(".","0").replace("\n","")))
    
    # As the board is nxn, taking the root gives the dimension
    dim = int(len(brett)**0.5)
    
    # Checking if the board is square
    if dim**2 != len(brett):
        raise ValueError("Not square board")
    clean_brett=[]
    
    # Splitting every row into it's own list
    for i in range(0,dim**2,dim):
        clean_brett.append(brett[i:i+dim])
    
    return clean_brett # Returning a list of lists


if __name__=="__main__":
    # Cleaning up some boards
    b4 = clean(".423.31..13.3...")
    b6 = clean("..3.41.145..14..2...2.6.6354.24..6..")
    b9 = clean("67.5.32......6.....53.....1436..5....2....3..5.1.........4.9.76....7.5.2..4...9..")

    # 4x4
    S4=Sudoku_4x4(b4)
    S4.solver()
    
    # 6x6
    S6=Sudoku_6x6(b6)
    S6.solver()
    
    # 9x9
    S9=Sudoku_9x9(b9)
    S9.solver()
