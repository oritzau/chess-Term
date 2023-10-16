from lib import Board, Player, BLACK, WHITE

def info(query: str, board: Board) -> str:
    return str(board.get_tile(query))

def main():
    board = Board()
    board.setup()
    p1, p2 = Player.create_two_players()
    p1.pieces = board.get_pieces_for_player(p1.color)
    p2.pieces = board.get_pieces_for_player(p2.color)
    turn_count = 1
    winner = False
    players = [p1, p2]
    for player in players:
        if player.color == WHITE:
            white_player = player
        else:
            black_player = player
    while winner == False:
        board.print_game_state()
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
                    print("\nThe tile you entered does not exist\n")
        while True:
            current_tile = current_player.select_start(board)
            target_tile = current_player.select_target(board)
            active_piece = current_tile.piece
            moving_into_check = False
            if active_piece.is_king:
                if other_player.has_check(target_tile, board):
                    print("\nCannot move into check!\n")
                    moving_into_check = True
            if target_tile.occupied and active_piece.can_attack(target_tile, board) and not moving_into_check:
                if target_tile.piece.is_king:
                    print(f"You win, {current_player.name}!")
                    winner = True
                    break
                active_piece.attack(target_tile)
                break
                
            elif active_piece.can_move(target_tile, board) and not moving_into_check:
                active_piece.move(target_tile)
                break

        for piece in other_player.pieces:
            if piece.is_king:
                king_location = piece.tile
        if current_player.has_check(king_location, board):
            print("\nCheck!")
        turn_count += 1
    
if __name__ == "__main__":
    main()
