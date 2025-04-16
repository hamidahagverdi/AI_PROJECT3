# TIC-TAC-TOE GAME

Winning positions: ±1,000,000,000 * (search_depth - current_depth)
Draws: 0

Non-Terminal Position Evaluation:

Pattern-based heuristic analyzing all potential winning lines
Pattern scoring: Player patterns = 10^n, Computer patterns = -10^n, Mixed patterns = 0
Final score is sum of all pattern evaluations

Minimax with Alpha-Beta Pruning

Search depth: 4 moves (configurable)
Player maximizes score, Computer minimizes
Early termination for detected wins/losses
Victory checking focused on last move only
Depth-factored scoring prioritizes immediate advantages
Move generation focused on cells adjacent to existing moves

Performance Optimizations
Proximity-Based Move Generation:

Only considers cells within configurable radius of existing moves
Reduces branching factor from O(n²) to smaller constant

Fast Victory Checking:

Only examines lines through most recent move
Counts consecutive symbols in both directions

Parallel Processing:

Distributes move evaluation across available CPU cores
Nearly linear speedup on multi-core systems

Optimized Data Structures:

Sets for O(1) move lookups
Efficient pattern evaluation
Minimal state storage
