from typing import List, Tuple, Set
from multiprocessing import Process, Pool, cpu_count
import api

class GeneralizedTicTacToe():
    """
    A generalized version of Tic-Tac-Toe that can be played on boards of various sizes
    with customizable winning conditions. Includes AI using alpha-beta pruning.
    """

    # Constants used in the evaluation process
    CONTINUE = 0x4D4D4D4D  # Special value indicating that the game should continue
    MAX_VALUE = 1000000000  # Large value used for win/loss scoring

    def __init__(self, size: int, win_length: int):
        """
        Initialize the game with a specified board size and winning condition length.
        
        Args:
            size: The dimension of the square board (size x size)
            win_length: Number of consecutive symbols needed to win
        """
        self.COMPUTER = 'O'      # Symbol for computer player
        self.PLAYER = 'X'        # Symbol for human player
        self.win_length = win_length  # Number of consecutive symbols needed to win
        self.search_depth = 4    # Maximum depth for alpha-beta search
        self.proximity = 1       # Radius around existing moves to consider for next moves
        self.size = size         # Board dimension
        self.grid = self.initialize_grid(self.size)  # Initialize empty board
        self.player_moves = set()    # Track player move coordinates
        self.computer_moves = set()  # Track computer move coordinates

    
    def initialize_grid(self, size: int) -> List[List[str]]:
        """
        Create an empty game board.
        
        Args:
            size: The dimension of the square board
        
        Returns:
            A 2D list representing the empty board with '-' in each cell
        """
        grid = [['-' for _ in range(size)] for _ in range(size)]
        return grid


    def is_valid_position(self, row: int, col: int) -> bool:
        """
        Check if a position is valid for making a move.
        
        Args:
            row: Row index
            col: Column index
        
        Returns:
            True if the position is within bounds and empty, False otherwise
        """
        if row >= self.size or row < 0:
            return False
        if col >= self.size or col < 0:
            return False
        return self.grid[row][col] == '-'
    

    def display_grid(self):
        """
        Print the current state of the game board to the console.
        """
        for i in range(self.size):
            for j in range(self.size):
                print(self.grid[i][j], end=" ")
            print()
        return
    
    
    def get_empty_positions(self) -> List[Tuple]:
        """
        Get all empty positions on the board.
        
        Returns:
            List of (row, col) tuples representing empty positions
        """
        positions = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == '-':
                    positions.append((i, j))
        return positions
    

    def get_nearby_positions(self) -> List[Tuple]:
        """
        Get empty positions that are within the proximity radius of existing moves.
        This optimizes move generation by focusing on relevant areas of the board.
        
        Returns:
            List of (row, col) tuples for empty positions near existing moves,
            or all empty positions if no nearby positions found
        """
        radius = self.proximity
        positions = []
        
        # Check positions near player moves
        for move in self.player_moves:
            start_row = max(move[0] - radius, 0) 
            end_row = min(move[0] + radius, self.size - 1)  
            start_col = max(move[1] - radius, 0) 
            end_col = min(move[1] + radius, self.size - 1)
            for i in range(start_row, end_row + 1):
                for j in range(start_col, end_col + 1):
                    if self.grid[i][j] == '-' and (i, j) not in positions:
                        positions.append((i, j))
        
        # Check positions near computer moves
        for move in self.computer_moves:
            start_row = max(move[0] - radius, 0) 
            end_row = min(move[0] + radius, self.size - 1)  
            start_col = max(move[1] - radius, 0) 
            end_col = min(move[1] + radius, self.size - 1)
            for i in range(start_row, end_row + 1):
                for j in range(start_col, end_col + 1):
                    if self.grid[i][j] == '-' and (i, j) not in positions:
                        positions.append((i, j))

        # If no nearby positions found, return all empty positions
        if not positions:
            return self.get_empty_positions()
        return positions
        
    
    def player_turn(self) -> Tuple[int, int]:
        """
        Handle player's turn by getting input and updating the game state.
        
        Returns:
            Tuple of (row, col) representing the player's move
        """
        while True:
            row, col = map(int, input("Enter row, col coordinates:").split())
            if self.is_valid_position(row, col):
                break
        
        self.place_symbol(self.PLAYER, (row, col), self.player_moves)
        return (row, col)
    

    def place_symbol(self, symbol: str, position: Tuple, move_set: Set[Tuple]):
        """
        Place a symbol on the board and update the corresponding move set.
        
        Args:
            symbol: The symbol to place ('X' or 'O')
            position: (row, col) tuple where to place the symbol
            move_set: Set of moves to update (player_moves or computer_moves)
        """
        if position == (-1, -1):
            print("ERROR: INVALID POSITION DETECTED")
            exit(1)
        move_set.add((position[0], position[1]))
        self.grid[position[0]][position[1]] = symbol

    
    def remove_symbol(self, position: Tuple, move_set: Set[Tuple]):
        """
        Remove a symbol from the board (used during search).
        
        Args:
            position: (row, col) tuple to remove the symbol from
            move_set: Set of moves to update (player_moves or computer_moves)
        """
        move_set.remove((position[0], position[1]))
        self.grid[position[0]][position[1]] = '-'
    
    
    def computer_turn(self) -> Tuple[int, int]:
        """
        Determine the best move for the computer using alpha-beta pruning.
        
        Returns:
            Tuple of (row, col) representing the computer's move
        """
        best_position = (-1, -1)
        best_score = GeneralizedTicTacToe.MAX_VALUE ** 2  # Initialize with a very high score (worse for computer)
        positions = self.get_nearby_positions()
        for position in positions:
            self.place_symbol(self.COMPUTER, position, self.computer_moves)
            # Get score from alpha-beta search (lower is better for computer)
            score = self.alpha_beta(True, 1, -GeneralizedTicTacToe.MAX_VALUE, GeneralizedTicTacToe.MAX_VALUE, position)
            self.remove_symbol(position, self.computer_moves)
            print(score)
            if score <= best_score:  # Computer is minimizing, so lower scores are better
                best_score = score
                best_position = (position[0], position[1])

        self.place_symbol(self.COMPUTER, best_position, self.computer_moves)
        return best_position    


    def alpha_beta(self, is_maximizing: bool, depth: int, alpha: int, beta: int, last_move: Tuple) -> int:
        """
        Alpha-beta pruning algorithm to evaluate the best move.
        
        Args:
            is_maximizing: True if maximizing player's turn (player), False if minimizing (computer)
            depth: Current search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            last_move: Last move made (used for victory checking)
            
        Returns:
            Evaluation score of the position
        """
        # First check if the position is terminal (win/loss/draw) or max depth reached
        evaluation = self.evaluate_position(depth, is_maximizing, last_move)
        if evaluation != GeneralizedTicTacToe.CONTINUE:
            return evaluation
        
        if is_maximizing == True:
            return self.maximize(depth, last_move, alpha, beta)
        
        return self.minimize(depth, last_move, alpha, beta)
    

    def maximize(self, depth: int, last_move: Tuple, alpha: int, beta: int):
        """
        Maximizing part of alpha-beta pruning (player's turn in search).
        
        Args:
            depth: Current search depth
            last_move: Last move made
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            
        Returns:
            Best score for maximizing player
        """
        best_val = -GeneralizedTicTacToe.MAX_VALUE
        for position in self.get_nearby_positions():
            self.place_symbol(self.PLAYER, position, self.player_moves)
            val = self.alpha_beta(False, depth + 1, alpha, beta, position)
            self.remove_symbol(position, self.player_moves)

            best_val = max(best_val, val)
            alpha = max(alpha, val)
            if alpha >= beta:  # Beta cutoff
                break
        
        return best_val
    
    def minimize(self, depth: int, last_move: Tuple, alpha: int, beta: int):
        """
        Minimizing part of alpha-beta pruning (computer's turn in search).
        
        Args:
            depth: Current search depth
            last_move: Last move made
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            
        Returns:
            Best score for minimizing player
        """
        best_val = GeneralizedTicTacToe.MAX_VALUE
        for position in self.get_nearby_positions():
            self.place_symbol(self.COMPUTER, position, self.computer_moves)
            val = self.alpha_beta(True, depth + 1, alpha, beta, position)
            self.remove_symbol(position, self.computer_moves)

            best_val = min(best_val, val)
            beta = min(beta, val)
            if alpha >= beta:  # Alpha cutoff
                break
        
        return best_val

    def evaluate_position(self, depth: int, is_maximizing: bool, last_move: Tuple):
        """
        Evaluate the current board position.
        
        Args:
            depth: Current search depth
            is_maximizing: True if maximizing player's turn, False otherwise
            last_move: Last move made (used for victory checking)
            
        Returns:
            Evaluation score or CONTINUE flag if search should continue
        """
        # Check if someone won with the last move
        if is_maximizing == True and self.check_victory(self.computer_moves, last_move):
            return -1 * GeneralizedTicTacToe.MAX_VALUE * (self.search_depth - depth)  # Computer wins
        if is_maximizing == False and self.check_victory(self.player_moves, last_move):
            return 1 * GeneralizedTicTacToe.MAX_VALUE * (self.search_depth - depth)   # Player wins
        if len(self.get_empty_positions()) == 0:
            return 0  # Draw
        if depth == self.search_depth:
            result = self.position_score(depth)  # Heuristic evaluation at max depth
            return result
        return GeneralizedTicTacToe.CONTINUE  # Continue search


    def position_score(self, depth: int):
        """
        Calculate a heuristic score for a non-terminal position.
        
        Args:
            depth: Current search depth
            
        Returns:
            A score estimating the value of the current position
        """
        total_score = 0
        
        # Find all possible winning patterns on the board
        patterns = self.find_all_patterns(self.grid, self.win_length)
        
        # Evaluate each pattern and sum up the scores
        for pattern in patterns:
            total_score += self.evaluate_pattern(pattern, depth)

        return total_score
            

    def find_all_patterns(self, grid, win_length):
        """
        Find all possible winning line patterns on the board.
        
        Args:
            grid: Current game grid
            win_length: Number of consecutive symbols needed to win
            
        Returns:
            List of all possible line patterns (horizontal, vertical, diagonal)
        """
        size = self.size
        patterns = []

        if win_length > size:
            return patterns

        # Horizontal patterns
        for i in range(size):
            for j in range(size - win_length + 1):
                patterns.append([grid[i][j + k] for k in range(win_length)])

        # Vertical patterns
        for j in range(size):
            for i in range(size - win_length + 1):
                patterns.append([grid[i + k][j] for k in range(win_length)])

        # Diagonal patterns (top-left to bottom-right)
        for i in range(size - win_length + 1):
            for j in range(size - win_length + 1):
                patterns.append([grid[i + k][j + k] for k in range(win_length)])

        # Diagonal patterns (top-right to bottom-left)
        for i in range(size - win_length + 1):
            for j in range(win_length - 1, size):
                patterns.append([grid[i + k][j - k] for k in range(win_length)])

        return patterns

    
    def evaluate_pattern(self, pattern, depth):
        """
        Evaluate a single pattern for its potential value.
        
        Args:
            pattern: List of symbols to evaluate
            depth: Current search depth
            
        Returns:
            Score for this pattern
        """
        symbol_count = self.count_symbols(pattern)
        computer_count = symbol_count.get(self.COMPUTER, 0)
        player_count = symbol_count.get(self.PLAYER, 0)

        # Check for winning patterns
        if computer_count == self.win_length:
            return -GeneralizedTicTacToe.MAX_VALUE * (self.search_depth - depth)  # Computer wins
        
        if player_count == self.win_length:
            return GeneralizedTicTacToe.MAX_VALUE * (self.search_depth - depth)   # Player wins

        # Evaluate pattern potential
        if computer_count > 0 and player_count > 0:
            return 0  # Mixed symbols, no potential
        elif player_count > 0:
            return 10 ** player_count  # Player potential (exponential scoring)
        elif computer_count > 0:
            return -1 * (10 ** computer_count)  # Computer potential (negative)
        return 0  # Empty pattern



    def count_symbols(self, pattern):
        """
        Count occurrences of each symbol in a pattern.
        
        Args:
            pattern: List of symbols
            
        Returns:
            Dictionary with count of each symbol
        """
        counts = {}
        for symbol in pattern:
            if symbol in counts:
                counts[symbol] += 1
            else:
                counts[symbol] = 1
        return counts
    

    
    def check_victory(self, moves: Set[Tuple], last_move: Tuple) -> bool:
        """
        Check if the last move created a winning line.
        
        Args:
            moves: Set of moves to check within
            last_move: Last move made
            
        Returns:
            True if the last move created a winning line, False otherwise
        """
        if last_move == (-1, -1):
            return False

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertical, diagonal down, diagonal up

        for (dr, dc) in directions:
            count = 1  # Start with 1 for the last move
            # Check forward direction
            for step in range(1, self.win_length):
                new_row = last_move[0] + step * dr
                new_col = last_move[1] + step * dc
                if (new_row, new_col) not in moves:
                    break
                count += 1
            
            # Check backward direction
            for step in range(1, self.win_length):
                new_row = last_move[0] - step * dr
                new_col = last_move[1] - step * dc
                if (new_row, new_col) not in moves:
                    break
                count += 1

            if count >= self.win_length:
                return True

        return False
    
    
  
    
    def play_human_vs_computer(self):
        """
        Play a game between a human player and the computer AI.
        """
        while True:
            self.display_grid()
            move = self.player_turn()
            if self.check_victory(self.player_moves, move):
                print('Player wins!')
                break
            
            if len(self.get_empty_positions()) == 0:
                print('Game ends in a draw')
                break

            move = computer_move_parallel(self)  # Use parallel processing to improve AI performance
            if self.check_victory(self.computer_moves, move):
                print('Computer wins!')
                break
            if len(self.get_empty_positions()) == 0:
                print('Game ends in a draw')
                break

        print("Computer moves:", self.computer_moves)
        print("Player moves:", self.player_moves)
        self.display_grid()

        return
    

    def play_computer_vs_online(self, team_id1, team_id2):
        """
        Play a game where this computer AI plays against an online opponent.
        
        Args:
            team_id1: This computer's team ID
            team_id2: Opponent's team ID
        """
        # Create a new game and make the first move
        game_id = api.create_game(team_id1, team_id2, self.size, self.win_length)
        
        self.place_symbol(self.COMPUTER, (self.size // 2, self.size // 2), self.computer_moves)
        move_id = api.make_move(game_id, team_id1, f"{self.size // 2},{self.size // 2}")

        while True:
            self.display_grid()
            # Wait for opponent's move
            while True:
                response = api.get_moves(game_id, "1") 
                if response['moveId'] != move_id:
                    row, col = map(int, response['move'].split(','))
                    move = (row, col)
                    self.place_symbol(self.PLAYER, move, self.player_moves)
                    break
            
            if self.check_victory(self.player_moves, move):
                print('Opponent wins!')
                break

            if len(self.get_empty_positions()) == 0:
                print('Game ends in a draw')
                break
            
            # Make computer's move
            self.display_grid()
            move = self.computer_turn()
            move_id = api.make_move(game_id, team_id1, f"{move[0]},{move[1]}")

            if self.check_victory(self.computer_moves, move):
                print('You win!')
                break

            if len(self.get_empty_positions()) == 0:
                print('Game ends in a draw')
                break

        
        print("Computer moves:", self.computer_moves)
        print("Player moves:", self.player_moves)
        self.display_grid()

        return
        

    
    def play_online_vs_computer(self, team_id, game_id):
        """
        Play a game where this computer AI responds to an online opponent who started the game.
        
        Args:
            team_id: This computer's team ID
            game_id: Existing game ID to join
        """
        # Get opponent's first move
        response = api.get_moves(game_id, "1")
        row, col = map(int, response['move'].split(','))
        move = (row, col)
        self.place_symbol(self.PLAYER, move, self.player_moves)
                     
        while True:
            self.display_grid()
            # Make computer's move
            move = self.computer_turn()
            move_id = api.make_move(game_id, team_id, f"{move[0]},{move[1]}")

            if self.check_victory(self.computer_moves, move):
                print('Computer wins!')
                break

            if len(self.get_empty_positions()) == 0:
                print('Game ends in a draw')
                break

            # Wait for opponent's move
            self.display_grid()
            while True:
                response = api.get_moves(game_id, "1") 
                if response['moveId'] != move_id:
                    row, col = map(int, response['move'].split(','))
                    move = (row, col)
                    self.place_symbol(self.PLAYER, move, self.player_moves)
                    break
            
            if self.check_victory(self.player_moves, move):
                print('Opponent wins!')
                break

            if len(self.get_empty_positions()) == 0:
                print('Game ends in a draw')
                break
        
        print("Computer moves:", self.computer_moves)
        print("Player moves:", self.player_moves)
        self.display_grid()

        
        
def computer_move_worker(args):
    """
    Worker function for parallel processing of computer moves.
    
    Args:
        args: Tuple containing (game, position)
        
    Returns:
        Tuple of (score, position)
    """
    game: GeneralizedTicTacToe = args[0]
    position = args[1]
    game.place_symbol(game.COMPUTER, position, game.computer_moves)
    score = game.alpha_beta(True, 1, -GeneralizedTicTacToe.MAX_VALUE, GeneralizedTicTacToe.MAX_VALUE, position)
    game.remove_symbol(position, game.computer_moves)
    return (score, position)


def computer_move_parallel(game: GeneralizedTicTacToe):
    """
    Use parallel processing to evaluate all possible computer moves.
    
    Args:
        game: Current game instance
        
    Returns:
        Best move position as (row, col) tuple
    """
    positions = game.get_nearby_positions()
    
    # Create a process pool to evaluate positions in parallel
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(computer_move_worker, [(game, position) for position in positions])

    # Find the best move (lowest score for computer)
    best_position = (-1, -1)
    best_score = GeneralizedTicTacToe.MAX_VALUE ** 2
    for result in results:
        score, position = result
        if score <= best_score:
            best_score = score
            best_position = (position[0], position[1])
    game.place_symbol(game.COMPUTER, best_position, game.computer_moves)
    return best_position
