# TIC-TAC-TOE GAME

Evaluation Function
Our evaluation function operates on two levels to assess board positions:
Terminal Position Evaluation:
Winning positions are assigned extreme values (±1,000,000,000 * (search_depth - current_depth))
The depth factor rewards quicker wins and delays losses
Draws are valued at 0
Non-Terminal Position Evaluation:
For positions at maximum search depth, we evaluate using a pattern-based heuristic
We analyze all possible winning patterns (horizontal, vertical, diagonal lines of length win_length)
Each pattern is scored based on symbol distribution:
Mixed patterns (containing both X and O) score 0 (no potential)
Player patterns score 10^n where n is the number of player symbols
Computer patterns score -10^n where n is the number of computer symbols
This exponential scoring heavily prioritizes nearly-complete lines
The final score is the sum of all pattern scores
This approach ensures that the algorithm recognizes immediate threats and opportunities while providing meaningful guidance in non-terminal positions.
Minimax Implementation with Alpha-Beta Pruning
Our implementation uses a standard minimax algorithm with alpha-beta pruning to search the game tree:
Alpha-Beta Framework:
Max depth of 4 moves into the future (configurable via search_depth)
Player maximizes score (prefers higher values)
Computer minimizes score (prefers lower values)
Alpha-beta pruning significantly reduces the search space
Key Implementation Features:
The search immediately returns when terminal states are detected
Victory checking focuses only on the last move made, avoiding redundant checks
Depth is factored into scoring to prefer immediate advantages over distant ones
The algorithm always checks neighboring positions first, prioritizing relevant moves
Move Generation Strategy:
Instead of exploring the entire board, we focus on cells adjacent to existing moves
This proximity-based approach dramatically reduces the branching factor
Only when no nearby positions exist do we fall back to checking all empty cells
Performance Optimizations
We implemented several techniques to improve search performance:
Proximity-Based Move Generation:
The get_nearby_positions() method only considers cells within a configurable radius of existing moves
This heuristic reduces the branching factor from O(n²) to a much smaller constant
The radius is adjustable via the proximity parameter (default: 1)
Fast Victory Checking:
Victory checks only examine lines passing through the most recent move
For each direction (horizontal, vertical, diagonal), we count consecutive symbols in both directions
This avoids redundant checks of the entire board after each move
Parallel Processing:
We leverage multiprocessing to evaluate different moves concurrently
The computer_move_parallel() function distributes calculations across available CPU cores
Each position evaluation is handled by a separate worker in the process pool
This parallelization provides nearly linear speedup on multi-core systems
Optimized Data Structures:
Player and computer moves are tracked in efficient sets for O(1) lookups
Pattern evaluation is structured to avoid redundant calculations
Memory usage is optimized by storing only the necessary state information
These optimizations allow our implementation to handle larger board sizes and longer winning conditions while maintaining responsive performance.
