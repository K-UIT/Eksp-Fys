from abc import ABC, abstractmethod


class Sudoku(ABC):
    """Generic (abstract) representation of Sudoku board"""

    def __init__(self, initial_board: list[list[int]], box_width: int, box_height: int):
        # Setting up dimensions of everything
        self.board=initial_board
        self.b_width=box_width
        self.b_height=box_height
        self.dimension=box_width*box_height
        self.number_elements=sum(len(row) for row in initial_board)
        # Generating rows,boxes and columns as empty objects
        self.Rows = [Row(n, self.b_width) for n in range(0,self.dimension)] # Making row objects
        self.Cols = [Column(n, self.b_height) for n in range(0,self.dimension)] # Making column objects
        self.Boxes = [] # List of all the boxes
        
        for x in range(0,self.dimension//self.b_width): # Boxes take in coordinates
            for y in range(0,self.dimension//self.b_height):
                self.Boxes.append(Box(x,y, self.b_width))
        
        # Checking if dimension is valud
        if not self._validate_board_dimensions():
            raise ValueError("Board dimensions are invalid")
        
        # Setting up the board
        self._set_up_board()
            
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
        for row_id, row in enumerate(self.board):
            for col_id, value in enumerate(row):
                box_row=row_id//self.b_height
                box_col=col_id//self.b_width
                box_id=box_row*(self.dimension//self.b_width)+box_col
                
                square = Square(value, self.Rows[row_id], self.Cols[col_id], 
                                           self.Boxes[box_id], value!=0) # Current square
                self.board[row_id][col_id]= square     # Swapping ints with objects
                self.Rows[row_id]._add_square(square)  # Connecting rows
                self.Cols[col_id]._add_square(square)  # Connecting columns
                self.Boxes[box_id]._add_square(square) # Connecting boxes
                
    def _validate_board_values(self) -> bool:
        """Validate values of board (no repeated values within elements)"""
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
            
        return True # If nothing was catched then it must be valid
    
    
    def _filled_out(self) -> bool: # This just checks if the board is filled out
        for row in self.board:
            for sq in row:
                if sq.value==0:
                    return False
        return True
    
    
    def solve(self) -> bool:
        # Checking if we are done
        if self._filled_out():
            return self._validate_board_values()
    
        # Find first empty square
        for row in self.board:
            for sq in row:
                if sq.value == 0:
                    for val in sq.possible_values():
                        sq.value = val
                        if self._validate_board_values():
                            if self.solve():
                                return True
                        sq.value = 0  # backtrack
                    return False  # no valid value fits here
    
        return False
    @abstractmethod
    def __str__(self) -> str: # I wrote this code before I saw it was abstract, whoopsies
        """Neat looking readable sudoku board formatter"""
        
        board = ""
        for row_id, row in enumerate(self.Rows):
            board += str(row) + "\n"
            if (row_id+1)%self.b_height==0 and (row_id+1)!=self.dimension:
                for _ in range(int(self.dimension**0.5)):
                    board+="--"*self.b_width +"|-"
                board =board[:-2]+"\n" # Really messy way but works

        return board


# Subclass of Sudoku
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



# Subclass of Sudoku
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



# Subclass of Sudoku
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
    """A single square of a Sudoku board"""

    def __init__(self, value: int, row: "Row", column: "Column", box: "Box", locked: bool):
        self.value=value
        self.row=row
        self.column=column
        self.box=box
        self.locked = locked
    def possible_values(self) -> list[int]:
        possible = []
        for val in range(1,len(self.row.elements)+1):
            if val not in self.row.values() and val not in self.column.values() and val not in self.box.values():
                possible.append(val)
            
        return possible



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
    def __init__(self, row_id, length):
        super().__init__()
        self.id=row_id
        self.length=length

    def __str__(self): # Prints out a row
        output=""
        for sq_id, square in enumerate(self.elements):
            output += str(square.value) +" "
            if (sq_id+1)%self.length==0 and (sq_id+1)!=len(self.elements):
                output += "| "
        return output


# Subclass of Element
# Should implement __str__ to print as a vertical column
class Column(Element):
    def __init__(self, col_id, height):
        super().__init__()
        self.id=col_id
        self.height=height
    def __str__(self): # Prints out a column
        output=""
        for sq_id, square in enumerate(self.elements):
            output += str(square.value) +"\n"
            if (sq_id+1)%self.height==0 and (sq_id+1)!=len(self.elements):
                output += "-\n"
        return output


# Subclass of Element
# Should implement __str__ to print as a box
class Box(Element):
    def __init__(self, x_id, y_id, width):
        super().__init__()
        self.x_id=x_id
        self.y_id=y_id
        self.width=width
        
    def __str__(self): # Prints out a box
        output=""
        for sq_id, square in enumerate(self.elements):
            output+=str(square.value)
            if (sq_id+1)%self.width==0 and (sq_id+1)!=len(self.elements):
                output+= "\n"
        output += "\n"
        return output


def clean(brett:str)-> list[list[int]]: # This method won't work for boards >9 but that's okay
    """Some prelogic to set up the board as a list of lists from a string"""
    
    brett=list(map(int,brett.replace(".","0").replace("\n",""))) # Making the str into a list of ints
    dim = int(len(brett)**0.5) # as the board is nxn we can do this to find the dimension
    
    if dim**2 != len(brett): # Checking if the board is square
        raise ValueError("Not square board")
    clean_brett=[]
    
    for i in range(0,dim**2,dim): # Splitting every column into it's own list
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

    
    
    
