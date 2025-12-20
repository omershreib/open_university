from runner import ReversiGameRunner
from agents import RandomAgent

if __name__ == "__main__":
    game = ReversiGameRunner(
        board_size=8,
        red_agent=RandomAgent(1),
        white_agent=RandomAgent(2),
        verbose=True,
        use_gui=True,
        gui_delay=0.1
    )
    game.play()
