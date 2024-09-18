# main.py
import farmgamegui


def main():
    """
    The main entry point for the Farm Game application.
    This function initializes the FarmGameGUI and starts the main event loop,
    allowing the application to run and respond to user interactions.
    """

    fg = farmgamegui.FarmGameGUI()
    fg.mainloop()


if __name__ == "__main__":
    main()
