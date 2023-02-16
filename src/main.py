from lib import Board, Player

def info(query: str, board: Board) -> str:
    return str(board.get_tile(query))

def main():
    board = Board()
    board.initialize_tiles()
    board.initialize_pieces()
    colors = Player.get_random_color()
    p1 = Player(1)
    p1.color = colors[0]
    p1.greet()
    p2 = Player(2)
    p2.color = colors[1]
    p2.greet()
    p1.pieces = board.get_pieces_for_player(p1.color)
    p2.pieces = board.get_pieces_for_player(p2.color)
    turn_count = 1
    players = [p1, p2]
    for player in players:
        if player.color == 1:
            white_player = player
        else:
            black_player = player
    while True:
        if turn_count % 2 == 1:
            current_player = white_player
            other_player = black_player
        else:
            current_player = black_player
            other_player = white_player
        print(f"\nYour turn, {current_player}\n")
        intent = current_player.get_intention()
        if intent == 0:
            while True:
                tile_select = input("Select a tile, or press '!' to switch back: ")
                if tile_select == '!':
                    break
                try:
                    print(str(board.get_tile(tile_select)))
                except ValueError:
                    print("Something went wrong with your selection, make sure it is in the format 'c4', 'D7', etc")
        
        current_tile = current_player.select_start(board)
        target_tile = current_player.select_target(board)
        active_piece = current_tile.piece
        if target_tile.occupied and active_piece.can_attack(target_tile, board):
            if target_tile.piece.is_king:
                print(f"You win, {current_player.name}!")
                break
            active_piece.attack(target_tile)
            
        elif active_piece.can_move(target_tile, board):
            active_piece.move(target_tile)
        for piece in other_player.pieces:
            if piece.is_king:
                king_location = piece.tile
        if current_player.is_check(king_location, board):
            print("\nCheck!\n")
        turn_count += 1
    
if __name__ == "__main__":
    main()
