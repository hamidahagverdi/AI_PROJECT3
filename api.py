import http.client
import ast

# API endpoint and authentication details
url = "/aip2pgaming/api/index.php"
id = '3679'
key = '3765d74d8c9c37475a69'

# HTTP headers for API requests
headers = {
  'userId': id,
  'x-api-key': key,
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'humans_21909=1'
}

def make_post_request(parameters: str) -> str:
    """
    Make a POST request to the API.
    
    Args:
        parameters: URL-encoded parameters string
        
    Returns:
        Dictionary containing the API response
    """
    conn = http.client.HTTPSConnection("www.notexponential.com")
    conn.request("POST", url, parameters, headers)
    response = conn.getresponse()
    data = response.read().decode()
    return ast.literal_eval(data)  # Convert JSON string to Python dictionary

def make_get_request(parameters: str) -> str:
    """
    Make a GET request to the API.
    
    Args:
        parameters: URL-encoded parameters string
        
    Returns:
        Dictionary containing the API response
    """
    conn = http.client.HTTPSConnection("www.notexponential.com")
    full_path = url + "?" + parameters
    conn.request("GET", full_path, None, headers)
    response = conn.getresponse()
    data = response.read().decode()
    return ast.literal_eval(data)  # Convert JSON string to Python dictionary


def create_team(tname: str) -> dict:
    """
    Create a new team.
    
    Args:
        tname: Team name
        
    Returns:
        Team ID if successful
    """
    payload = f"type=team&name={tname}"
    res = make_post_request(payload)
    print(res)
    assert res['code'] == 'OK', 'create_team'
    return res['teamId']
        

def add_team_member(teamId: str, userId: str)-> dict:
    """
    Add a member to a team.
    
    Args:
        teamId: Team ID
        userId: User ID to add
        
    Returns:
        API response
    """
    payload = f"type=member&userId={userId}&teamId={teamId}"
    res = make_post_request(payload)
    print(res)
    assert res['code'] == 'OK', 'add_team_member'
    return res


def remove_team_member(teamId: str, userId: str) -> dict:
    """
    Remove a member from a team.
    
    Args:
        teamId: Team ID
        userId: User ID to remove
        
    Returns:
        API response
    """
    payload = f"type=removeMember&userId={userId}&teamId={teamId}"
    res = make_post_request(payload)
    print(res)
    assert res['code'] == 'OK', 'remove_team_member'
    return res


def get_team_members(teamId: str) -> dict:
    """
    Get members of a team.
    
    Args:
        teamId: Team ID
        
    Returns:
        Team member information
    """
    payload = f"type=team&teamId={teamId}"
    res = make_get_request(payload)
    print(res)
    assert res['code'] == 'OK', 'get_team_members'
    return res


def get_my_team() -> dict:
    """
    Get teams that the authenticated user belongs to.
    
    Returns:
        User's team information
    """
    payload = f"type=myTeams"
    res = make_get_request(payload)
    print(res)
    assert res['code'] == 'OK', 'get_my_team'
    return res


def create_game(teamId1: str, teamId2: str, boardSize: int, target: int) -> str:
    """
    Create a new Tic-Tac-Toe game.
    
    Args:
        teamId1: Team ID of the first player
        teamId2: Team ID of the second player
        boardSize: Size of the game board
        target: Number of consecutive symbols needed to win
        
    Returns:
        Game ID if successful
    """
    payload = f"type=game&teamId1={teamId1}&teamId2={teamId2}&gameType=TTT&boardSize={boardSize}&target={target}"
    res = make_post_request(payload)
    print(res)
    assert res['code'] == 'OK', 'create_game'
    return res['gameId']

def get_my_games() -> dict:
    """
    Get all games for the authenticated user.
    
    Returns:
        User's game information
    """
    payload = f"type=myGames"
    res = make_get_request(payload)
    print(res)
    assert res['code'] == 'OK', 'get_my_games'
    return res

def get_my_open_games() -> dict:
    """
    Get open (not yet finished) games for the authenticated user.
    
    Returns:
        User's open game information
    """
    payload = f"type=myOpenGames"
    res = make_get_request(payload)
    print(res)
    assert res['code'] == 'OK', 'get_my_games'
    return res

def make_move(gameId: str, teamId: str, move: str) -> dict:
    """
    Make a move in a game.
    
    Args:
        gameId: Game ID
        teamId: Team ID making the move
        move: Move coordinates in format "row,col"
        
    Returns:
        Move ID if successful
    """
    payload = f"type=move&gameId={gameId}&teamId={teamId}&move={move}"
    res = make_post_request(payload)
    print(res)
    assert res['code'] == 'OK', 'make_move'
    return str(res['moveId'])

def get_moves(gameId: str, count: str) -> dict:
    """
    Get recent moves in a game.
    
    Args:
        gameId: Game ID
        count: Number of moves to retrieve
        
    Returns:
        Move information for the requested game
    """
    payload = f"type=moves&gameId={gameId}&count={count}"
    res = make_get_request(payload)
    print(res)
    assert res['code'] == 'OK', 'get_moves'
    return res['moves'][0]  # Return the most recent move

def get_game_details(gameId: str) -> dict:
    """
    Get details about a specific game.
    
    Args:
        gameId: Game ID
        
    Returns:
        Game details
    """
    payload = f"type=gameDetails&gameId={gameId}"
    res = make_get_request(payload)
    print(res)
    assert res['code'] == 'OK', 'get_game_details'
    return res

def get_board_string(gameId: str) -> dict:
    """
    Get the game board as a string representation.
    
    Args:
        gameId: Game ID
        
    Returns:
        Board represented as a string
    """
    payload = f"type=boardString&gameId={gameId}"
    res = make_post_request(payload)
    print(res)
    assert res['code'] == 'OK', 'get_board_string'
    return res

def get_board_map(gameId: str) -> dict:
    """
    Get the game board as a map representation.
    
    Args:
        gameId: Game ID
        
    Returns:
        Board represented as a map
    """
    payload = f"type=boardMap&gameId={gameId}"
    res = make_get_request(payload)
    print(res)
    assert res['code'] == 'OK', 'get_board_map'
    return res



