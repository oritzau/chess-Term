from lib import *

if __name__ == "__main__":
    board = Board()
    board.initialize_tiles()
    board.initialize_pieces()
    board.represent()
    p1 = Player(1, 0, board)
    p1.greet()
    p2 = Player(2, 1, board)
    p2.greet()

    turn_count = 0
    while True:
        if turn_count % 2 == 0:
            current_player = p2
        else:
            current_player = p1
        current_tile = current_player.select_start(board)
        target_tile = current_player.select_target(board)
        active_piece = current_tile.piece
        if target_tile.occupied and active_piece.can_attack(target_tile, board):
            if target_tile.piece.is_king:
                print(f"You win, {current_player.name}!")
                break
            active_piece.attack(target_tile)
            turn_count += 1
        elif active_piece.can_move(target_tile, board):
            active_piece.move(target_tile)
            turn_count += 1
        board.represent()