from content.text_variables import * 

class EventManager():

    def __init__(self):
        self.dragongates = DragonGates()
        self.giant = Giant()
        self.wormhole = Wormhole()
        self.suscat = SusCat()
        self.genielamp = GenieLamp()
        self.curr_loc = self.dragongates
        self.id_dict = {'ВРАТА ДРАКОНА': self.dragongates, 'МЕЖПРОСТРАНСТВЕННЫЙ ПОРТАЛ': self.wormhole, 'ТРЁХГЛАВЫЙ ГИГАНТ': self.giant, 'ПОДОЗРИТЕЛЬНЫЙ КОТ': self.suscat, 'ЛАМПА ДЖИНА': self.genielamp}
        self.line_id = 0
        self.is_map_accessable = False
        self.is_intro_ended = False

    def loc_from_id(self, id: str) -> GameLocation:
        return self.id_dict[id]
    
    def next_line(self):
        return self.curr_loc.dialog_branch[self.line_id]
    
    def choice_next_branch(self, choice):
        if self.curr_loc.loc_id == 'ТРЁХГЛАВЫЙ ГИГАНТ' and self.curr_loc.right_flag and self.curr_loc.left_flag and self.curr_loc.center_flag:
            self.curr_loc.options = None
            self.curr_loc.dialog_branch = g_branch_intro_end
            self.curr_loc.next_branches = None
            self.line_id = 0
            print(self.curr_loc.dialog_branch)
        else:
            self.curr_loc.options = self.curr_loc.next_branches[choice][1]
            self.curr_loc.dialog_branch = self.curr_loc.next_branches[choice][0]
            if self.curr_loc.next_branches[choice][2] != 'self':
                self.curr_loc.next_branches = self.curr_loc.next_branches[choice][2]
            self.line_id = 0

    
class GameLocation():

    def __init__(self):
        self.loc_flag = False
        self.dialog_flag = False
        self.encounter_avatar = encounter_ph
        self.encounter_title = 'ИМЯ'
        self.loc_id = 'ЛОКАЦИЯ'
        self.dialog_branch = branch_ph
        self.options = None
        self.next_branches = None

    def on_entry(self):
        pass

class DragonGates(GameLocation):

    def __init__(self):
        super().__init__()
        self.encounter_avatar = encounter_dragon_gates
        self.encounter_title = encounter_title_dragon_gates
        self.loc_id = 'ВРАТА ДРАКОНА'
        self.dialog_branch = dg_branch_intro_1
        self.options = dg_options_intro
        self.next_branches = dg_next_branches_intro
        self.riddles_id = 0
        self.riddles_answers = [['прах']]

class Giant(GameLocation):

    def __init__(self):
        super().__init__()
        self.encounter_avatar = encounter_giant
        self.encounter_title = encounter_title_giant
        self.loc_id = 'ТРЁХГЛАВЫЙ ГИГАНТ'
        self.dialog_branch = g_branch_intro_1
        self.options = g_options_intro
        self.next_branches = g_next_branches_intro
        self.right_flag = False
        self.left_flag = False
        self.center_flag = False

class Wormhole(GameLocation):

        def __init__(self):
            super().__init__()
            self.encounter_avatar = encounter_wormhole
            self.encounter_title = encounter_title_wormhole
            self.loc_id = 'МЕЖПРОСТРАНСТВЕННЫЙ ПОРТАЛ'
            self.dialog_branch = wh_branch_intro_1
            self.options = wh_options_intro_1
            self.next_branches = wh_next_branches_intro_1

class SusCat(GameLocation):

        def __init__(self):
            super().__init__()
            self.encounter_avatar = encounter_suscat
            self.encounter_title = encounter_title_suscat
            self.loc_id = 'МЕЖПРОСТРАНСТВЕННЫЙ ПОРТАЛ'
            self.dialog_branch = sc_branch_1
            self.options = sc_options_1
            self.next_branches = sc_next_branches_1
            self.riddles_id = 0
            self.riddles_answers = [['эхо'], ['мягкий знак', 'мягким знаком', 'ь'], ['сон']]

class GenieLamp(GameLocation):

    pass