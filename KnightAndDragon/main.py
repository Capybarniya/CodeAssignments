#from textual.widgets import Button

from ui import GameApplication

if __name__ == "__main__":
    app = GameApplication()

    app.run()

    #GameApplication().query_one('#next_btn', Button).action_press()