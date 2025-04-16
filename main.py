from adverserial import GeneralizedTicTacToe


if __name__ == '__main__':
    size, win_length = map(int, input("Enter size and win length: ").split())
    game = GeneralizedTicTacToe(size, win_length)
    game.play_human_vs_computer()
