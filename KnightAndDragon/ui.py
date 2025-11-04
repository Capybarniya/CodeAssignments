from textual.app import App
from textual.containers import Horizontal, Vertical, Center
from textual.widgets import Footer, Header, RichLog, Select, Label, MaskedInput, Static, Button
from textual.screen import Screen

from content.text_variables import *
from game_logic import EventManager

class CluesScreen(Screen):

    BINDINGS = [("c", "app.pop_screen", "выйти")]
    CSS_PATH = 'content/clues screen.tcss'

    def compose(self):
        yield Header(icon = '🐲')
        yield Footer(show_command_palette = False)
        with Vertical():
            with Center():
                yield MaskedInput(template="AAAA;_", id='goal')
            with Horizontal():
                yield RichLog(id='l1')
                yield RichLog(id='l2')
                yield RichLog(id='l3')
                yield RichLog(id='l4')

    def on_mount(self):
        letter = self.query_one('#l1', RichLog)
        letter.border_subtitle = 'FIRST LETTER'
        letter = self.query_one('#l2', RichLog)
        letter.border_subtitle = 'SECOND LETTER'
        letter = self.query_one('#l3', RichLog)
        letter.border_subtitle = 'THIRD LETTER'
        letter = self.query_one('#l4', RichLog)
        letter.border_subtitle = 'FOURTH LETTER'

class MapLocation(Static):

    def __init__(self, content = "", *, expand = False, shrink = False, markup = True, name = None, id = None, classes = None, disabled = False):
        super().__init__(content, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)

    def on_enter(self, event):
        loc_name = self.parent.query_one("#word", Label)
        loc_name.content = self.content

    def on_leave(self, event):
        loc_name = self.parent.query_one("#word", Label)
        loc_name.content = self.parent.parent.parent.parent.gamemaster.curr_loc.loc_id

    def on_click(self, event):
        loc_name = self.parent.query_one("#word", Label)
        self.parent.parent.parent.parent.gamemaster.curr_loc = self.parent.parent.parent.parent.gamemaster.loc_from_id(self.content)
        loc_name.content = self.parent.parent.parent.parent.gamemaster.curr_loc.loc_id
        button = self.parent.parent.parent.parent.query_one('#next_btn', Button)
        ava = self.parent.parent.parent.parent.query_one('#avatar', Label)
        name = self.parent.parent.parent.parent.query_one('#name', Label)
        ava.content = self.parent.parent.parent.parent.gamemaster.curr_loc.encounter_avatar
        name.content = self.parent.parent.parent.parent.gamemaster.curr_loc.encounter_title
        log = self.parent.parent.parent.parent.query_one("#Log", RichLog)
        log.write('==================================================================================================\n')
        self.parent.parent.parent.parent.gamemaster.line_id = 0
        button.disabled = False
        button.action_press()

class GameApplication(App):

    CSS_PATH = "content/main screen.tcss"
    SCREENS = {"clues": CluesScreen}
    BINDINGS = [("c", "push_screen('clues')", "зацепки")]

    def __init__(self, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self.gamemaster = EventManager()

    def compose(self):
        yield Header(icon = '🐲')
        yield Footer(show_command_palette = False)
        with Horizontal():
            with Vertical(id='v1'):
                yield Label(encounter_dragon_gates, id='avatar')
                yield Label(encounter_title_dragon_gates, id='name')
            with Vertical(id='v2'):
                log = RichLog(highlight=False, markup=True, wrap=True, id='Log')
                log.write('> '+self.gamemaster.next_line()[0])
                self.gamemaster.line_id += 1
                yield log
                with Horizontal(id='inputs'):
                    yield Select.from_values(LINES, id='Select', prompt='-')
                    yield Button(label='->', id='next_btn', compact=True)
            with Vertical(id='v3'):
                yield Label(self.gamemaster.curr_loc.loc_id, id='word')
                yield Label(loc_map_string, id='locmap')
                yield MapLocation(id='gates_of_dragon', content='ВРАТА ДРАКОНА')
                yield MapLocation(id='treeheaded_giant', content='ТРЁХГЛАВЫЙ ГИГАНТ')
                yield MapLocation(id='interdimesinal_portal', content='МЕЖПРОСТРАНСТВЕННЫЙ ПОРТАЛ')
                yield MapLocation(id='suspicious_cat', content='ПОДОЗРИТЕЛЬНЫЙ КОТ')
                yield MapLocation(id='lamp_of_genie', content='ЛАМПА ДЖИНА')
                #yield Button(label='yo mama', id='yomama')

    def on_mount(self):
        self.title = "KNIGHT AND DRAGON"
        #self.sub_title = "Main Screen"
        self.theme = 'textual-light'
        text_log = self.query_one("#Log", RichLog)
        text_log.border_subtitle = 'TEXT LOG'
        text_log = self.query_one("#locmap", Label)
        text_log.border_subtitle = 'MAP'
        text_log = self.query_one("#avatar", Label)
        text_log.border_subtitle = 'ENCOUNTER'


    def on_ready(self):
        text_log = self.query_one("#Log", RichLog)

        text_log.write(text)

    def on_button_pressed(self, event):
       button_id = event.button.id
       button = self.query_one('#'+button_id, Button)
       select = self.query_one("#Select", Select)
       line, option_id = self.gamemaster.next_line()
       text_log = self.query_one("#Log", RichLog)
       text_log.write('> '+ line)
       self.gamemaster.line_id += 1

       if option_id in (1, 3, 4, 5):
           select.disabled = False
           select.set_options(self.gamemaster.curr_loc.options)
           button.disabled = True
           self.gamemaster.line_id = 0
           select.action_show_overlay()
           #text_log.write('> '+ 't')
           match option_id:
               case 3: self.gamemaster.curr_loc.right_flag = True
               case 4: self.gamemaster.curr_loc.left_flag = True
               case 5: self.gamemaster.curr_loc.center_flag = True

       if option_id == 2:
           button.disabled = True

    def on_select_changed(self, event):
        select = self.query_one("#Select", Select)
        choice = select.selection
        if choice != None:
            button = self.query_one('#next_btn', Button)
            text_log = self.query_one("#Log", RichLog)
            text_log.write('\n> ' + '[i]' + str(self.gamemaster.curr_loc.options[choice-1][0]) + '[/i]\n')
            button.disabled = False
            self.gamemaster.choice_next_branch(choice)
            button.action_press()
            select.disabled = True



