import random

BLACK = 0
WHITE = 1

def smart_range(start: int, stop: int) -> range:
    #excludes start, includes stop, adjusts for lower stop than start
    if start == stop:
        return None
    if start > stop:
        return range(start - 1, stop - 1, -1)
    return range(start + 1, stop + 1)
 

class Board:
    def __init__(self) -> None:
        self.__tiles = []
        self.__pieces = []

    def setup(self):
        self.initialize_tiles()
        self.initialize_pieces()

    def initialize_tiles(self) -> None:
        for i in range(1, 9):
            for j in range(1, 9):
                #covers issue of rows going BWBWBWBWBW and then the subsequent row starting with W and so on 
                if i % 2 == 0:
                    temp_tile = Tile(i, j, j % 2)
                else:
                    temp_tile = Tile(i, j, (j + 1) % 2)
                self.__tiles.append(temp_tile)

    def get_pieces_for_player(self, color: int) -> list:
        return_list = []
        for piece in self.__pieces:
            if piece.color == color:
                return_list.append(piece)
        return return_list

    def initialize_pieces(self) -> None:
        
        #White Pawns
        pawn_row = 2
        for j in range(1, 9):
            self.__pieces.append(Pawn(self.get_tile_by_index(pawn_row, j), WHITE))
        
        #Black Pawns
        pawn_row = 7
        for j in range(1, 9):
            self.__pieces.append(Pawn(self.get_tile_by_index(pawn_row, j), BLACK))

        #White Rooks
        self.__pieces.append(Rook(self.get_tile_by_index(1, 1), WHITE))
        self.__pieces.append(Rook(self.get_tile_by_index(1, 8), WHITE))
        
        #Black Rooks
        self.__pieces.append(Rook(self.get_tile_by_index(8, 1), BLACK))
        self.__pieces.append(Rook(self.get_tile_by_index(8, 8), BLACK))
        
        #White Knights
        self.__pieces.append(Knight(self.get_tile_by_index(1, 2), WHITE))
        self.__pieces.append(Knight(self.get_tile_by_index(1, 7), WHITE))
        
        #Black Knights
        self.__pieces.append(Knight(self.get_tile_by_index(8, 2), BLACK))
        self.__pieces.append(Knight(self.get_tile_by_index(8, 7), BLACK))
        
        #White Bishops
        self.__pieces.append(Bishop(self.get_tile_by_index(1, 3), WHITE))
        self.__pieces.append(Bishop(self.get_tile_by_index(1, 6), WHITE))
        
        #Black Bishops
        self.__pieces.append(Bishop(self.get_tile_by_index(8, 3), BLACK))
        self.__pieces.append(Bishop(self.get_tile_by_index(8, 6), BLACK))
        
        #Queens
        self.__pieces.append(Queen(self.get_tile_by_index(1, 4), WHITE))
        self.__pieces.append(Queen(self.get_tile_by_index(8, 4), BLACK))
        
        #Kings
        self.__pieces.append(King(self.get_tile_by_index(1, 5), WHITE))
        self.__pieces.append(King(self.get_tile_by_index(8, 5), BLACK))

    def get_tile_by_index(self, row: int, column: int) -> 'Tile':
        try:    
            return self.__tiles[(row - 1)* 8 + (column - 1)]
        except IndexError:
            return None

    # tiles are stored in self.__tiles starting at A1 going to H8
    # this method converts that upside down so that the bottom left is A1 when printing
    def print_game_state(self):
        piece_dict = {
            "pawn": "P",
            "knight": "K",
            "bishop": "T",
            "rook": "R",
            "queen": "Q",
            "king": "K",
        }
        board_state = ""
        length = len(self.__tiles)
        for i in range(1, 9):
            start_pos = length - (i * 8)
            for j in range(start_pos, start_pos + 8):
                tile = self.__tiles[j]
                if tile.occupied:
                    piece_name = str(tile.piece).split(" ")[1].lower()
                    board_state += "{:<3}".format(piece_dict[piece_name])
                else:
                    board_state += "{:<3}".format("_")
            board_state += "\n"
        print(board_state)

    def get_tile(self, query: str) -> 'Tile':
        letters = "abcdefgh"
        column_letter: str = query[0].lower()
        row: int = int(query[1]) - 1
        column: int = letters.index(column_letter)
        return self.__tiles[row * 8 + column]

    

class Player:
    def __init__(self, number: int) -> None:
        self.name = input(f"What would you like to be called, Player {number}: ")
        self.pieces = []
        self.in_check = False

    def create_two_players():
        colors = Player.get_random_color()
        p1 = Player(1)
        p1.color = colors[0]
        p1.greet()
        p2 = Player(2)
        p2.color = colors[1]
        p2.greet()
        return p1, p2


    def get_random_color() -> tuple:
        colors = [BLACK, WHITE]
        random.shuffle(colors)
        return colors

    def greet(self) -> None:
        colors = ["black", "white"]
        print(f"\nGreetings, {self.name}! You will be playing {colors[self.color]}.\n")
    
    # todo! 
    def castle(self):
        pass

    def get_intention(self) -> int:
        while True:
            intent = input("Press '?' to enter info mode, '!' to enter play mode: ")
            if intent.lower() == '?': #help
                return 0
            elif intent.lower() == '!': #play
                return 1
    def __str__(self) -> str:
        return self.name

    def select_start(self, board: Board) -> 'Tile':
        while True:
            selection = input(f"Select tile, {self.name} : ")
            try:
                selected_tile = board.get_tile(selection)
                if selected_tile.piece.color == self.color:
                    break
                else:
                    print("That tile controlled by your opponent's piece")
            except AttributeError or ValueError:
                print("That tile is empty or does not exist")
                pass
        return selected_tile
    
    def has_check(self, king_location: 'Tile', board: Board) -> bool:
        for piece in self.pieces:
            if piece.can_attack(king_location, board):
                return True
        return False
    
    def select_target(self, board: Board) -> 'Tile':
        while True:
            selection = input("Select target tile: ")
            try:
                selected_tile = board.get_tile(selection)
                if selected_tile.occupied == False or selected_tile.piece.color != self.color:
                    break
                else:
                    print("That tile is controlled by one of your pieces")
            except AttributeError or ValueError:
                print("Something went wrong, double check your selection")
                pass
        return selected_tile

    

class Tile:
    #black = 0, white = 1
    def __init__(self, row: int, column: int, color: int) -> None:
        self.__row = row
        self.__column = column
        self.__color = color
        self.occupied = False
        self.piece = None
    
    def get_row(self) -> int:
        return self.__row
    
    def get_column(self) -> int:
        return self.__column
    
    #Ex: "C2", "H1", "A5", etc.
    def __str__(self) -> str:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        if self.occupied:
            return f"{letters[self.__column - 1]}{self.__row}, Piece: {str(self.piece)}"
        else:
            return f"{letters[self.__column - 1]}{self.__row}, empty"
        
    def show_less(self) -> str:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        return f"{letters[self.__column - 1]}{self.__row}"

class Piece:
    def __init__(self, start_tile: Tile, color: int) -> None:
        self.tile = start_tile
        self.tile.piece = self
        self.tile.occupied = True
        self.color = color
        self.has_moved = False
        self.is_king = False

    def __str__(self) -> str:
        colors = ["Black", "White"]
        return f"{colors[self.color]}"
    
    def move(self, other: Tile):
        self.tile.occupied = False
        self.tile = other
        other.occupied = True
        other.piece = self
        if self.has_moved == False:
            self.has_moved = True
        print(f"{str(self)} to {self.tile.show_less()}")

    def attack(self, other: Tile):
        self.tile.occupied = False
        self.tile = other
        other.piece = self

class Pawn(Piece):
    def __init__(self, start_tile: Tile, color: int) -> None:
        super().__init__(start_tile, color)

    def __str__(self) -> str:
        return super().__str__() + " Pawn"

    def can_move(self, other: Tile, board: Board) -> bool:
        valid_row = False
        valid_column = False
        current_row, target_row = self.tile.get_row(), other.get_row()
        current_column, target_column = self.tile.get_column(), other.get_column()
        if self.has_moved == False:
            if self.color == 1: #white
                if target_row == current_row + 2 and board.get_tile_by_index(current_row + 2, current_column).occupied == False:
                    valid_row = True
            else: #black
                if target_row == current_row - 2 and board.get_tile_by_index(current_row - 2, current_column).occupied == False:
                    valid_row = True
        if self.color == 1: #white
            if target_row == current_row + 1:
                valid_row = True
        else: #black
            if target_row == current_row - 1:
                valid_row = True
        if current_column == target_column:
            valid_column = True
        if valid_column and valid_row and other.occupied == False:
            return True
        return False

    def can_attack(self, other: Tile, board: Board) -> bool:
        valid_row = False
        valid_column = False
        valid_square = False
        current_row, target_row = self.tile.get_row(), other.get_row()
        current_column, target_column = self.tile.get_column(), other.get_column()
        if other.occupied and other.piece.color != self.color:
            valid_square = True
        if self.color == 1: #white
            if target_row == current_row + 1:
                valid_row = True
        else: #black
            if target_row == current_row - 1:
                valid_row = True
        if current_column + 1 == target_column or current_column - 1 == target_column:
            valid_column = True
        if valid_column and valid_row and valid_square:
            return True
        return False
        
    def transform(self):
        pass

class Knight(Piece):
    def __init__(self, start_tile: Tile, color: int) -> None:
        super().__init__(start_tile, color)

    def __str__(self) -> str:
        return super().__str__() + " Knight"
    
    def can_move(self, other: Tile, board: Board) -> bool:
        current_row, target_row = self.tile.get_row(), other.get_row()
        current_column, target_column = self.tile.get_column(), other.get_column()
        l_shape = False
        if current_row == target_row - 2 or current_row == target_row + 2:
            if current_column == target_column - 1 or current_column == target_column + 1: #checking L shape
                l_shape = True
        if current_row == target_row - 1 or current_row == target_row + 1:
            if current_column == target_column - 2 or current_column == target_column + 2: #checking ___| shape
                l_shape = True
        if other.occupied == False and l_shape:
            return True
        return False

    def can_attack(self, other: Tile, board: Board) -> bool:
        current_row, target_row = self.tile.get_row(), other.get_row()
        current_column, target_column = self.tile.get_column(), other.get_column()
        l_shape = False
        if current_row == target_row - 2 or current_row == target_row + 2:
            if current_column == target_column - 1 or current_column == target_column + 1: #checking L shape
                l_shape = True
        if current_row == target_row - 1 or current_row == target_row + 1:
            if current_column == target_column - 2 or current_column == target_column + 2: #checking ___| shape
                l_shape = True
        if other.occupied == True and other.piece.color != self.color and l_shape:
            return True
        return False

class Bishop(Piece):
    def __init__(self, start_tile: Tile, color: int) -> None:
        super().__init__(start_tile, color)
    
    def __str__(self) -> str:
        return super().__str__() + " Bishop"
    
    def can_move(self, other: Tile, board: Board) -> bool:
        #checks if all tiles on path are unoccupied and if path is diagonal
        if other == self.tile:
            return False
        tiles_traveled = []
        current_row, target_row = self.tile.get_row(), other.get_row()
        current_column, target_column = self.tile.get_column(), other.get_column()
        # is_diagonal = False
        if abs(current_row - target_row) == abs(current_column - target_column):
            is_diagonal = True
        else:
            return False
        #Ex (2, 3) C2 to (4, 5) E4
        row_list = list(smart_range(current_row, target_row))
        column_list = list(smart_range(current_column, target_column))
        for i in range(len(row_list)):
            tiles_traveled.append(board.get_tile_by_index(row_list[i], column_list[i]))
        if all(tile.occupied == False for tile in tiles_traveled) and is_diagonal:
            return True
        return False

    def can_attack(self, other: Tile, board: Board) -> bool:
        #checks if all EXCEPT last tile are unoccupied, last tile contains opposite color, and path is diagonal
        if other == self.tile:
            return False
        tiles_traveled = []
        current_row, target_row = self.tile.get_row(), other.get_row()
        current_column, target_column = self.tile.get_column(), other.get_column()
        # is_diagonal = False
        if abs(current_row - target_row) == abs(current_column - target_column):
            is_diagonal = True
        else:
            return False
        row_list = list(smart_range(current_row, target_row))
        column_list = list(smart_range(current_column, target_column))
        for i in range(len(row_list)):
            tiles_traveled.append(board.get_tile_by_index(row_list[i], column_list[i]))
        if all(tile.occupied == False for tile in tiles_traveled[:-1]) and is_diagonal and other.piece.color != self.color:
            return True
        return False

class Rook(Piece):
    def __init__(self, start_tile: Tile, color: int) -> None:
        super().__init__(start_tile, color)

    def __str__(self) -> str:
        return super().__str__() + " Rook"

    def can_move(self, other: Tile, board: Board) -> bool:
        current_row, target_row = self.tile.get_row(), other.get_row()
        current_column, target_column = self.tile.get_column(), other.get_column()
        tiles_traveled = []
        is_straight = False
        if current_row == target_row and current_column != target_column:
            for i in smart_range(current_column, target_column):
                tiles_traveled.append(board.get_tile_by_index(current_row, i))
            is_straight = True
        elif current_column == target_column and current_row != target_row:
            for i in smart_range(current_row, target_row):
                tiles_traveled.append(board.get_tile_by_index(i, current_column))
            is_straight = True
        else:
            return False
        if is_straight and all(tile.occupied == False for tile in tiles_traveled):
            return True
        return False
    
    def can_attack(self, other: Tile, board: Board) -> bool:
        current_row, target_row = self.tile.get_row(), other.get_row()
        current_column, target_column = self.tile.get_column(), other.get_column()
        tiles_traveled = []
        is_straight = False
        if current_row == target_row and current_column != target_column:
            for i in smart_range(current_column, target_column):
                tiles_traveled.append(board.get_tile_by_index(current_row, i))
            is_straight = True
        elif current_column == target_column and current_row != target_row:
            for i in smart_range(current_row, target_row):
                tiles_traveled.append(board.get_tile_by_index(i, current_column))
            is_straight = True
        else:
            return False
        if is_straight and all(tile.occupied == False for tile in tiles_traveled[:-1]) and other.piece.color != self.color:
            return True
        return False

class Queen(Piece):
    def __init__(self, start_tile: Tile, color: int) -> None:
        super().__init__(start_tile, color)
    
    def __str__(self) -> str:
        return super().__str__() + " Queen"

    def can_move(self, other: Tile, board: Board) -> bool:
        valid_move = False
        temp_bishop = Bishop(self.tile, self.color)
        if temp_bishop.can_move(other, board):
            valid_move = True
        temp_rook = Rook(self.tile, self.color)
        if temp_rook.can_move(other, board):
            valid_move = True
        Queen(self.tile, self.color)
        return valid_move
    
    def can_attack(self, other: Tile, board) -> bool:
        valid_attack = False
        temp_bishop = Bishop(self.tile, self.color)
        if temp_bishop.can_attack(other, board):
            valid_attack = True
        temp_rook = Rook(self.tile, self.color)
        if temp_rook.can_attack(other, board):
            valid_attack = True
        Queen(self.tile, self.color)
        return valid_attack

class King(Piece):
    def __init__(self, start_tile: Tile, color: int) -> None:
        super().__init__(start_tile, color)
        self.is_king = True
    
    def __str__(self) -> str:
        return super().__str__() + " King"

    def can_move(self, other: Tile, board: Board) -> bool:
        current_row, target_row = self.tile.get_row(), other.get_row()
        current_column, target_column = self.tile.get_column(), other.get_column()
        is_1_square = False
        no_surrounding_king = False
        if abs(target_column - current_column) == 1 and abs(target_row - current_row) == 1:
            is_1_square = True
        if abs(target_column - current_column) == 1 and abs(target_row - current_row) == 0:
            is_1_square = True
        if abs(target_column - current_column) == 0 and abs(target_row - current_row) == 1:
            is_1_square = True
        #checking if king within 1 tile or target tile (other)
        surrounding_tiles = []
        surrounding_tiles.append(board.get_tile_by_index(target_row - 1, target_column - 1))
        surrounding_tiles.append(board.get_tile_by_index(target_row - 1, target_column + 1))
        surrounding_tiles.append(board.get_tile_by_index(target_row + 1, target_column + 1))
        surrounding_tiles.append(board.get_tile_by_index(target_row + 1, target_column - 1))
        surrounding_tiles.append(board.get_tile_by_index(target_row, target_column - 1))
        surrounding_tiles.append(board.get_tile_by_index(target_row, target_column + 1))
        surrounding_tiles.append(board.get_tile_by_index(target_row - 1, target_column))
        surrounding_tiles.append(board.get_tile_by_index(target_row + 1, target_column))
        
        surrounding_tiles = [i for i in surrounding_tiles if i is not None] #dropping None values

        if self.color == 0: #black
            if all(str(tile.piece) != "White King" for tile in surrounding_tiles) and is_1_square:
                no_surrounding_king = True
        
        elif self.color == 1: #white
            if all(str(tile.piece) != "Black King" for tile in surrounding_tiles) and is_1_square:
                no_surrounding_king = True
        if is_1_square and no_surrounding_king and other.occupied == False:
            return True
        return False

    def can_attack(self, other: Tile, board: Board) -> bool:
        current_row, target_row = self.tile.get_row(), other.get_row()
        current_column, target_column = self.tile.get_column(), other.get_column()
        is_1_square = False
        no_surrounding_king = False
        if abs(target_column - current_column) == 1 and abs(target_row - current_row) == 1:
            is_1_square = True
        if abs(target_column - current_column) == 1 and abs(target_row - current_row) == 0:
            is_1_square = True
        if abs(target_column - current_column) == 0 and abs(target_row - current_row) == 1:
            is_1_square = True
        #checking if king within 1 tile or target tile (other)
        surrounding_tiles = []
        surrounding_tiles.append(board.get_tile_by_index(target_row - 1, target_column - 1))
        surrounding_tiles.append(board.get_tile_by_index(target_row - 1, target_column + 1))
        surrounding_tiles.append(board.get_tile_by_index(target_row + 1, target_column + 1))
        surrounding_tiles.append(board.get_tile_by_index(target_row + 1, target_column - 1))
        surrounding_tiles.append(board.get_tile_by_index(target_row, target_column - 1))
        surrounding_tiles.append(board.get_tile_by_index(target_row, target_column + 1))
        surrounding_tiles.append(board.get_tile_by_index(target_row - 1, target_column))
        surrounding_tiles.append(board.get_tile_by_index(target_row + 1, target_column))
        
        surrounding_tiles = [i for i in surrounding_tiles if i is not None] #dropping None values

        if self.color == 0: #black
            if all(str(tile.piece) != "White King" for tile in surrounding_tiles) and is_1_square:
                no_surrounding_king = True
        
        elif self.color == 1: #white
            if all(str(tile.piece) != "Black King" for tile in surrounding_tiles) and is_1_square:
                no_surrounding_king = True
        if is_1_square and no_surrounding_king and other.occupied == True and other.piece.color != self.color:
            return True
        return False
