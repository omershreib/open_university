from runner import ReversiGameRunner
from agents import RandomAgent, AlphaBetaAgent

if __name__ == "__main__":
    game = ReversiGameRunner(board_size=8, max_agent=RandomAgent(85), min_agent=AlphaBetaAgent(), verbose=True)
    game.play()
