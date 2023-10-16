## Welcome to chessTerm! 
A lightweight, terminal based chess application which allows you to play 
against a local opponent or face off against yourself. 

chess-Term is best enjoyed with a friend as the game does not currently support 
online or AI opponents. When prompted, enter a name for each player and you 
will receive a color at random. 
## How to play:
chess-Term follows the modal style of editors like Vim, with players 
starting every turn in info mode. In info mode, board tiles can be freely
queried for piece information.

Use **!** to switch to play mode, where moves are made by selecting a start
and destination tile. Moves will be validated before they are allowed to 
be played. 

## Important Notes
- Checks will be announced but do not strictly **have** to be blocked, moved 
out of, etc. One player wins by capturing the enemy king.
- Castling is currently unsupported but I am planning on implementing it soon
