from lib import Tile, Board, Piece, Pawn

def info(query: str, board: Board) -> str:
    return str(board.get_tile(query))

def main():
    board = Board()
    board.initialize_tiles()
    board.initialize_pieces()
    
if __name__ == "__main__":
    main()
