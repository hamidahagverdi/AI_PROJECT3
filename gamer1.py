from adverserial import GeneralizedTicTacToe

teamID = "1458"
teamID2 = "1449"


if __name__ == '__main__':
    teamID = "1458"
    teamID2 = "1449"
    game = GeneralizedTicTacToe(5, 4)
    game.play_computer_vs_online(teamID, teamID2)