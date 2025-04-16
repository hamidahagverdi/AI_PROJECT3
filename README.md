# TIC-TAC-TOE GAME

Generalized Tic-Tac-Toe Implementation
How Our AI Thinks (Evaluation Function)
Our AI evaluates the game board in two ways:
When the game can end:

If AI can win: Very high positive score
If player can win: Very high negative score
If it's a draw: Score of 0
Faster wins are worth more than slower wins

During regular gameplay:

The AI looks at all possible winning lines on the board
Lines with only AI pieces get positive scores
Lines with only player pieces get negative scores
Mixed lines (with both AI and player pieces) are worth nothing
More pieces in a line = exponentially higher score
Example: A line with 3 AI pieces is much stronger than 3 separate lines with 1 AI piece each

How Our AI Decides Moves (Minimax Algorithm)

The AI thinks ahead 4 moves (like a chess player)
It assumes the player will make the best possible move
It uses "alpha-beta pruning" to avoid analyzing obviously bad moves
The AI immediately recognizes winning or losing positions
It first checks spaces next to existing pieces (most promising moves)

How We Made It Fast
Smart Move Selection:

The AI only considers moves near existing pieces
This makes the game much faster on large boards

Efficient Win Detection:

Only checks if the most recent move created a winning line
Doesn't waste time checking the entire board after each move

Parallel Processing:

Uses multiple CPU cores to evaluate different moves at the same time
Like having multiple AIs thinking about different possibilities simultaneously

Memory Optimization:

Uses efficient data structures to track moves and patterns
Stores only what's necessary to make decisions

This implementation can play on larger boards (beyond 3x3) and with different winning conditions (beyond 3-in-a-row) while still making smart moves quickly.
