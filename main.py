from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables.datatables import MDDataTable
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivymd.uix.label.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
import random
from kivymd.uix.card import MDCard

# from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

from datetime import datetime
import uuid

from database import Database
# Initialize db instance
db = Database()

# Window.size = (1080, 2400)


class MainScreen(Screen):
    
    pass

class DrillsScreen(Screen):
    pass

class TwoByFourScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_scores = []
        self.entry_dialog = None
        self.data_table = None
        self.data_table_row_num = 0
        self.history_table = None
    
    def show_dialog(self, **kwargs):
        if not self.entry_dialog:
            self.entry_dialog = MDDialog(
                title="Enter Score",
                type="custom",
                content_cls=TwoByFourDialog(),
            )
        self.entry_dialog.open()
        pass 

    def close_dialog(self, *args):
        self.entry_dialog.dismiss()

    def on_pre_enter(self, *args):
        self.data_table_row_num = 0
        app.current_drill = "twobyfours"
        app.update_session_id()
        # self.add_history()
        
        if not self.data_table:
            self.data_table = MDDataTable(
                pos_hint={"center_y": 0.5, "center_x": 0.5},
                use_pagination=False,
                rows_num=20,
                column_data=[
                    ("Station", dp(20)),
                    ("Target", dp(15)),
                    ("Score", dp(15)),
                    ("Notes", dp(50)),
                ],
                row_data=[],
            )
            self.ids.twobyfour_current_container.add_widget(self.data_table)
        
        #clear row_data when screen loads
        self.data_table.row_data = []

    def add_score(self, drill, session_id, score, distance, club, lie, other=None):
        if type(club) is not str:
            club = club.text
        if type(lie) is not str:
            lie = lie.text
        
        db.submit_score(drill, session_id, int(score.value), int(distance.value), club, lie, other)
        # self.close_dialog()
        notes = f"{club} | {lie} | {int(distance.value)}ft"
        self.data_table.add_row((str(self.data_table_row_num + 1), "4", score.value, notes))
        self.data_table_row_num += 1
        pass 

    def submit_session(self, **kwargs):
        print("Session submitted")
        pass 
    
    def pull_current_scores(self):
        session_id = app.session_id
        self.current_scores = db.get_session_scores('twobyfours', session_id)

    def add_history(self):

        if not self.history_table:
            self.history_table = MDDataTable(
                    use_pagination=False,
                    column_data=[
                        ("Date", dp(30)),
                        ("# of Stations", dp(30)),
                        ("Average Score", dp(30)),
                    ],
                    row_data=[],
                )
            self.ids.twobyfour_history_container.add_widget(self.history_table)

        else:
            #clear_history
            self.history_table.row_data = []
        
        #update current history data
        row_data = []
        rows = db.get_historical_scores('twobyfours', app.session_id, limit = 5)
        for row in rows:
            row_data.append([row[1].strftime("%m/%d"), row[2], round(row[3],1)])
        
        self.history_table.row_data = row_data

    pass

class TwoByFourDialog(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE INPUT FROM THE USER"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def close_dialog(self):
        self.dismiss()

class StarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_scores = []
        self.entry_dialog = None
        self.data_table = None
        self.data_table_row_num = 0
        self.history_table = None

    def on_pre_enter(self, *args):
        self.data_table_row_num = 0
        app.current_drill = "star"
        app.update_session_id()
        
        if not self.data_table:
            self.data_table = MDDataTable(
                pos_hint={"center_y": 0.5, "center_x": 0.5},
                use_pagination=False,
                rows_num=20,
                column_data=[
                    ("Station", dp(20)),
                    ("Target", dp(15)),
                    ("Score", dp(15)),
                    ("Notes", dp(50)),
                ],
                row_data=[],
            )
            self.ids.star_current_container.add_widget(self.data_table)
        
        #clear row_data when screen loads
        self.data_table.row_data = []

    def add_score(self, drill, session_id, score, distance,other=None):
        
        db.submit_score(drill, session_id, int(score.value), int(distance.value), None, None, other)
        # self.close_dialog()
        notes = f"{int(distance.value)}ft"
        self.data_table.add_row((str(self.data_table_row_num + 1), "tbd", str(score.value), notes))
        self.data_table_row_num += 1
        pass 

    def submit_session(self, **kwargs):
        print("Session submitted")
        pass 
    
    def pull_current_scores(self):
        session_id = app.session_id
        self.current_scores = db.get_session_scores('star', session_id)

    pass

class RouletteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_scores = []
        self.data_table = None
        self.data_table_row_num = 0
        self.history_table = None
        self.clubs = ['GW', '52', '56', '60']
        self.surfaces = ['Tight', 'Lt Rough', 'Hvy Rough',  'Sand']
        self.distances = ["10ft", "20ft", "30ft", "40ft"]
        self.carrys = ["0%","25%", "50%", "75%"]
        self.stances = ["Flat", "Uphill", "Downhill"]
        self.breaks = ["Flat", "Uphill", "Downhill"]
        self.score_ids = ['roulette_3', 'roulette_6', 'roulette_9', 'roulette_12']
        

    def on_pre_enter(self, *args):
        self.data_table_row_num = 0
        app.current_drill = "roulette"
        app.update_session_id()
        
        # if not self.data_table:
        #     self.data_table = MDDataTable(
        #         pos_hint={"center_y": 0.5, "center_x": 0.5},
        #         use_pagination=False,
        #         rows_num=20,
        #         column_data=[
        #             ("Station", dp(20)),
        #             ("Target", dp(15)),
        #             ("Score", dp(15)),
        #             ("Notes", dp(50)),
        #         ],
        #         row_data=[],
        #     )
        #     self.ids.roulette_current_container.add_widget(self.data_table)
        
        # #clear row_data when screen loads
        # self.data_table.row_data = []


        self.club_menu = CustomMenu(self.clubs,self.ids.club_button)
        self.surface_menu = CustomMenu(self.surfaces,self.ids.surface_button, width_mult=4)
        self.distance_menu = CustomMenu(self.distances,self.ids.distance_button)
        self.carry_menu = CustomMenu(self.carrys,self.ids.carry_button)
        self.stance_menu = CustomMenu(self.stances,self.ids.stance_button)
        self.break_menu = CustomMenu(self.breaks,self.ids.break_button)

        self.menus = [self.club_menu, self.surface_menu, self.distance_menu, self.carry_menu, self.stance_menu, self.break_menu]
        self.menu_fields = ['club', 'surface', 'distance', 'carry', 'stance', 'break']

    def auto_choose(self):
        for menu in self.menus:
            item = random.choice(menu.items)
            menu.callback(item['text'])

        pass


    def submit_score(self):

        session_id = app.session_id
        drill = 'roulette'
        
        #Need to capture ALL the Station + ALL the Scores from root

        input_values = {'drill': drill, 'session_id': session_id}
        for field, menu in zip(self.menu_fields, self.menus):
            if field == 'break':
                field = '_break'
            input_values[field] = menu.caller.text
            menu.caller.text = "--"
        self.auto_choose()

        # print(input_values)

        scores = {}
        for score_id in self.score_ids:
            prox_value = int(score_id.split("_")[-1])
            prox_str = f"{prox_value} ft"
            input_values['prox'] = prox_str
            score_widget = eval("self.ids."+score_id)
            for i in range(score_widget.value):
                db.submit_prox(**input_values)
            score_widget.value = 0

            
        
        pass 

    def submit_session(self, **kwargs):
        print("Session submitted")
        pass 
    
    def pull_current_scores(self):
        session_id = app.session_id
        self.current_scores = db.get_session_scores('star', session_id)

    pass


class CustomMenu(MDDropdownMenu):
    
    def __init__(self, choices, caller, width_mult=2):

        items = []
        for c in choices:
             temp = {
                    "text": c,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=c: self.callback(x),
                }
             items.append(temp)
        super().__init__(caller=caller, items=items,width_mult=width_mult)
    
    def callback(self, x):
        self.caller.text = x
        self.dismiss()

class PlusMinus(MDBoxLayout):

    def plus(self):
        self.parent.parent.value += 1
    def minus(self):
        if self.parent.parent.value > 0:
            self.parent.parent.value -= 1
        else:
            pass

    pass

class RouletteCard(MDCard):
    distance_text = StringProperty()
    

    def __init__(self, **kwargs):
        super(RouletteCard,self).__init__(**kwargs)
        
        


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(DrillsScreen(name='drills'))
sm.add_widget(TwoByFourScreen(name='twobyfour'))
sm.add_widget(StarScreen(name='star'))
sm.add_widget(RouletteScreen(name='roulette'))

class MainApp(MDApp):
    current_drill = None
    current_scores = None
    historical_scores = None
    entry_dialog = None
    session_id = str(uuid.uuid4())

    def update_session_id(self):
        self.session_id = str(uuid.uuid4())

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "700"
    
    # def show_dialog(self, **kwargs):
    #     if not self.entry_dialog:
    #         self.entry_dialog = MDDialog(
    #             title="Enter Score",
    #             type="custom",
    #             content_cls=TwoByFourDialog(),
    #         )

    #     self.entry_dialog.open()
    #     pass 

    # def close_dialog(self, *args):
    #     self.entry_dialog.dismiss()
    #     self.pull_current_scores()
    
    # def pull_current_scores(self):
    #     self.current_scores = db.get_session_scores(self.current_drill, self.session_id)
        # print("APP...Trying to pull scores")
        # print(self.current_scores)
    
    
    

app = MainApp()
app.run()
