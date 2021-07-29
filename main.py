from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.recycleview import RecycleView
from kivy.config import Config 
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.storage.jsonstore import JsonStore
from settings_json import settings_json
import datetime
import data
Config.set('graphics', 'resizable', True)



class PhaseScreen(Screen):
    I = BooleanProperty(True)
    II = BooleanProperty(False)
    III = BooleanProperty(False)
    stagecheck = BooleanProperty(True)
    blighted = BooleanProperty(False)
    prevM = StringProperty()
    prevP = StringProperty()
    nextP = StringProperty()
    phaseEmpty = BooleanProperty()
    currentP = StringProperty('Main')
    title = StringProperty('Spirit Island Phase Tracker')
    next_button_value = StringProperty('')
    time = StringProperty('')
    setupScreens = BooleanProperty(True)

    ehealth = StringProperty('1')
    edamage = StringProperty('1')
    thealth = StringProperty('2')
    tdamage = StringProperty('2')
    chealth = StringProperty('3')
    cdamage = StringProperty('3')
    dhealth = StringProperty('2')
    ddamage = StringProperty('2')
    def on_enter(self):
        app = App.get_running_app() 
        app.currentPhase = 'Main'
        self.next_button_value = 'Start'
        if app.use_timer:
            self.seconds = app.timer_seconds
            self.time = ''
            self.time = ':'.join(str(datetime.timedelta(seconds=self.seconds)).split(':')[1:])
            self.clock = Clock.schedule_interval(self.timer, 1)
        else:
            self.time = ''
        self.calc_health_damage()
    def on_next_Phase(self):
        app = App.get_running_app()
        self.calc_health_damage()
        if app.currentPhase == 'Main':
            app.previousPhase.append(app.currentPhase)
        elif app.previousPhase[-1] != app.currentPhase:
            app.previousPhase.append(app.currentPhase)
        if app.currentPhase == 'Main':
            nextP = 'SpiritSelect'
        if app.currentPhase == 'SpiritSelect':
            nextP = 'BoardSetup'
        if app.currentPhase == 'BoardSetup':
            nextP = 'SpiritSetup'
        if app.currentPhase == 'SpiritSetup':
            nextP = 'FirstExplore'
        if app.currentPhase == 'FirstExplore':
            nextP = 'Growth'
        if app.currentPhase == 'Growth':
            nextP = 'Energy'
        if app.currentPhase == 'Energy':
            nextP = 'PowerCards'
        if app.currentPhase == 'PowerCards':
            nextP = 'FastPower'
        if app.currentPhase == 'FastPower':
            if app.blight != 'Healthy':
                nextP = 'BlightedIsland'
            elif app.expansion == 'None':
                nextP = 'Fear'
            else:
                nextP = 'Event'
        if app.currentPhase == 'BlightedIsland':
            if app.expansion == 'None':
                nextP = 'Fear'
            else:
                nextP = 'Event'
        if app.currentPhase == 'Event':
            nextP = 'Fear'
        if app.currentPhase == 'Fear':
            if app.opponent == 'England' and int(app.level) == 3  and app.stage != "III" and app.turn > 1:
                nextP = 'HighImmigration'
            elif app.opponent == 'England' and int(app.level) >= 4 and app.turn > 1:
                nextP = 'HighImmigration'
            else:
                if app.turn > 1:
                    nextP = 'Ravage'
                else:
                    nextP = 'Build'
        if app.currentPhase == 'HighImmigration':
            if app.turn > 1:
                nextP = 'Ravage'
            else:
                nextP = 'Build'
        if app.currentPhase == 'Ravage':
            nextP = 'Build'
        if app.currentPhase == 'Build':
            nextP = 'Explore'
        if app.currentPhase == 'Explore':
            nextP = 'AdvanceCards'
        if app.currentPhase == 'AdvanceCards':
            nextP = 'SlowPower'
        if app.currentPhase == 'SlowPower':
            nextP = 'TimePasses'
        if app.currentPhase == 'TimePasses':
            nextP = 'Growth'
        self.title = app.screenTitles[nextP]
        self.currentP = nextP
        self.start_clock()
        if nextP == 'Main':
            self.next_button_value = 'Start'
            self.setupScreens = True
        elif nextP == 'SpiritSelect':
            self.next_button_value = 'Next'
            self.setupScreens = True
        elif nextP == 'BoardSetup':
            self.next_button_value = 'Next'
            self.setupScreens = True
        elif nextP == 'SpiritSetup':
            self.next_button_value = 'Begin Game'
            self.setupScreens = True
        else:
            self.next_button_value = 'Next Phase'
            self.setupScreens = False
        return nextP
        
    def start_clock(self):
        app = App.get_running_app()
        if app.use_timer:
            Clock.unschedule(self.clock)
            self.seconds = app.timer_seconds
            self.time = ':'.join(str(datetime.timedelta(seconds=self.seconds)).split(':')[1:])
            self.clock = Clock.schedule_interval(self.timer, 1)
        else:
            self.time = ''
    def on_back(self):
        app = App.get_running_app()
        
        self.start_clock()
        prev = app.previousPhase[-1]
        self.title = app.screenTitles[prev]
        if prev != 'Main':
            app.previousPhase.pop()
        self.currentP = prev
        if prev == 'Main':
            self.next_button_value = 'Start'
            self.setupScreens = True
        elif prev == 'SpiritSelect':
            self.next_button_value = 'Next'
            self.setupScreens = True            
        elif prev == 'BoardSetup':
            self.next_button_value = 'Next'
            self.setupScreens = True
        elif prev == 'SpiritSetup':
            self.next_button_value = 'Begin Game'
            self.setupScreens = True
        else:
            self.next_button_value = 'Next Phase'
            self.setupScreens = False
        return prev
    def blight_checkbox(self, value):
        app = App.get_running_app()
        if value:
            app.blight = 'Blighted'
            self.blighted = True
            write_state()
            return True
        else:
            app.blight = 'Healthy'
            self.blighted = False
            write_state()
            return False
    def calc_health_damage(self):
        app = App.get_running_app()
        self.ehealth = str(app.opponentmod_rules[app.opponent][int(app.level)][0])
        self.edamage = str(app.opponentmod_rules[app.opponent][int(app.level)][3])
        self.thealth = str(app.opponentmod_rules[app.opponent][int(app.level)][1])
        self.tdamage = str(app.opponentmod_rules[app.opponent][int(app.level)][4])
        self.chealth = str(app.opponentmod_rules[app.opponent][int(app.level)][2])
        self.cdamage = str(app.opponentmod_rules[app.opponent][int(app.level)][5])      
    time = StringProperty()
    def timer(self, *args):
        app = App.get_running_app()
        if app.use_timer:
            if self.seconds == 0:
                self.time = '0'
                self.time_disp = "0"
                Clock.unschedule(self.clock)
            else:
                self.seconds -= 1
                self.time = ':'.join(str(datetime.timedelta(seconds=self.seconds)).split(':')[1:])
        else:
            self.time = ''
    def on_stage_toggle(self, value):
        app = App.get_running_app()
        app.stage = value    
        if app.stage == 'I':
            self.I = True
            self.II = False
            self.III = False
        elif app.stage == 'II':
            self.II = True
            self.I = False
            self.III = False
        elif app.stage == 'III':
            self.III = True
            self.I = False
            self.II = False
        app.on_stage_toggle(app.stage)
        write_state()
    def read_state(self):
        app = App.get_running_app()
        app.branchandclaw = (store.get('branchandclaw')['value'])
        app.jaggedearth = (store.get('jaggedearth')['value'])
        app.promopack1 = (store.get('promopack1')['value'])
        app.promopack2 = (store.get('promopack2')['value'])
        app.expansion = (store.get('expansion')['value'])
        app.opponent = (store.get('opponent')['value'])
        app.thematic = (store.get('thematic')['value'])
        app.spirits = (store.get('spirits')['value'])
        app.aspects = (store.get('aspects')['value'])
        app.scenario = (store.get('scenario')['value'])
        app.level = (store.get('level')['value'])
        app.stage = (store.get('stage')['value'])
        app.blight = (store.get('blight')['value'])
        app.players = (store.get('players')['value'])
        app.fear_tokens = (store.get('fear_tokens')['value'])
        app.turn = (store.get('turn')['value'])
        app.previousPhase = (store.get('previousPhase')['value'])
        app.opponent_list = (store.get('opponent_list')['value'])
        app.spirit_list = (store.get('spirit_list')['value'])
        app.scenarios_list = (store.get('scenarios_list')['value'])
        app.currentPhase = app.previousPhase[-1]
        self.lvl = app.level
        self.calc_health_damage()
        if app.blight != 'Healthy':
            self.blighted = True
        else:
            self.blighted = False
        self.on_stage_toggle(app.stage)
        if app.currentPhase == 'Main':
            nextP = 'SpiritSelect'
        if app.currentPhase == 'SpiritSelect':
            nextP = 'BoardSetup'
        if app.currentPhase == 'BoardSetup':
            nextP = 'SpiritSetup'
        if app.currentPhase == 'SpiritSetup':
            nextP = 'FirstExplore'
        if app.currentPhase == 'FirstExplore':
            nextP = 'Growth'
        if app.currentPhase == 'Growth':
            nextP = 'Energy'
        if app.currentPhase == 'Energy':
            nextP = 'PowerCards'
        if app.currentPhase == 'PowerCards':
            nextP = 'FastPower'
        if app.currentPhase == 'FastPower':
            if app.blight != 'Healthy':
                nextP = 'BlightedIsland'
            elif app.expansion == 'None':
                nextP = 'Fear'
            else:
                nextP = 'Event'
        if app.currentPhase == 'BlightedIsland':
            if app.expansion == 'None':
                nextP = 'Fear'
            else:
                nextP = 'Event'
        if app.currentPhase == 'Event':
            nextP = 'Fear'
        if app.currentPhase == 'Fear':
            if app.opponent == 'England' and int(app.level) == 3  and app.stage != "III" and app.turn > 1:
                nextP = 'HighImmigration'
            elif app.opponent == 'England' and int(app.level) >= 4 and app.turn > 1:
                nextP = 'HighImmigration'
            else:
                if app.turn > 1:
                    nextP = 'Ravage'
                else:
                    nextP = 'Build'
        if app.currentPhase == 'HighImmigration':
            if app.turn > 1:
                nextP = 'Ravage'
            else:
                nextP == 'Build'
        if app.currentPhase == 'Ravage':
            nextP = 'Build'
        if app.currentPhase == 'Build':
            nextP = 'Explore'
        if app.currentPhase == 'Explore':
            nextP = 'AdvanceCards'
        if app.currentPhase == 'AdvanceCards':
            nextP = 'SlowPower'
        if app.currentPhase == 'SlowPower':
            nextP = 'TimePasses'
        if app.currentPhase == 'TimePasses':
            nextP = 'Growth'
        self.title = app.screenTitles[nextP]
        self.currentP = nextP
        self.start_clock()
        if nextP == 'Main':
            self.next_button_value = 'Start'
            self.setupScreens = True
        elif nextP == 'SpiritSelect':
            self.next_button_value = 'Next'
            self.setupScreens = True            
        elif nextP == 'BoardSetup':
            self.next_button_value = 'Next'
            self.setupScreens = True
        elif nextP == 'SpiritSetup':
            self.next_button_value = 'Begin Game'
            self.setupScreens = True
        else:
            self.next_button_value = 'Next Phase'
            self.setupScreens = False
        return nextP

#mainscreen holder. all variables come from the MainApp
#corresponds to kivy Main
class MainScreen(Screen):
    bc = BooleanProperty(False)
    je  = BooleanProperty(False)
    pp1 = BooleanProperty(False)
    pp2 = BooleanProperty(False)
    theme = BooleanProperty(False)
    opp = StringProperty('None')
    lvl = StringProperty('')
    play = StringProperty('1')
    max_play = ListProperty(['1','2','3','4'])
    max_levels = ListProperty(['0'])
    next = StringProperty('BoardSetup')
    opp_list = ListProperty()
    scen_list = ListProperty()
    def on_enter(self):
        app = App.get_running_app()
        self.scen_list = app.scenarios_list
        app.currentPhase = 'Main'
        if app.branchandclaw:
            self.bc = True
        self.je = app.jaggedearth
        self.pp1 = app.promopack1
        self.pp2 = app.promopack2
        self.opp = app.opponent
        self.play = str(app.players)
        self.lvl = app.level
        self.theme = app.thematic
    def bc_clicked(self, value):
        app = App.get_running_app()
        if value == True:
            app.branchandclaw = True
        else:
            app.branchandclaw = False
        self.build_expansions()
        self.build_spirits()
        self.build_scenarios()
        if self.opp not in self.opp_list:
            self.opponent_clicked('None')
    def je_clicked(self, value):
        app = App.get_running_app()
        if value == True:
            app.jaggedearth = True
        else:
            app.jaggedearth = False
        self.build_expansions()
        self.build_spirits()
        self.build_scenarios()
        if self.opp not in self.opp_list:
            self.opponent_clicked('None')
        if self.play not in self.max_play:
            self.players_clicked('0')
    def promo1_clicked(self, value):
        app = App.get_running_app()
        if value == True:
            app.promopack1 = True
        else:
            app.promopack1 = False
        self.build_expansions()
        self.build_spirits()
        self.build_scenarios()
        if self.opp not in self.opp_list:
            self.opponent_clicked('None')
    def promo2_clicked(self, value):
        app = App.get_running_app()
        if value == True:
            app.promopack2 = True
        else:
            app.promopack2 = False
        self.build_expansions()
        self.build_spirits()
        self.build_scenarios()
        if self.opp not in self.opp_list:
            self.opponent_clicked('None')
    def thematic_clicked(self, value):
        app = App.get_running_app()
        if value == True:
            app.thematic = True
        else:
            app.thematic = False
    def opponent_clicked(self, value):
        app = App.get_running_app()
        app.opponent = value
        self.opp = value
        self.build_levels()
        self.lvl = app.level
        if self.opp != 'None' and self.lvl == '0':
            self.level_clicked('1')
        if self.opp == 'None':
            self.level_clicked('0')
    def level_clicked(self, value):
        app = App.get_running_app()
        app.level = value
        self.lvl = app.level
    def players_clicked(self, value):
        app = App.get_running_app()
        app.players = value
        self.play = app.players
        app.stage2_flag['Scotland'] = 'If the invader card has a flag:\nOn the single board with the most coastal towns/cities add one town to the '+ str(app.players) +' lands with the fewest towns.\n'
    def build_expansions(self):
        app = App.get_running_app()
        self.max_play = ['1','2','3','4']
        app.opponent_list = app.base_opp
        if app.branchandclaw:
            app.opponent_list = app.opponent_list + app.bc_opp
        if app.jaggedearth:
            app.opponent_list = app.opponent_list + app.je_opp
            self.max_play = ['1','2','3','4','5','6']
        if app.promopack2:
            app.opponent_list = app.opponent_list + app.pp2_opp
        self.opp_list = sorted(app.opponent_list)
        if app.branchandclaw and app.jaggedearth:
            app.expansion = "BC and JE"
        elif app.branchandclaw and not app.jaggedearth:
            app.expansion = "Branch and Claw"
        elif app.jaggedearth and not app.branchandclaw:
            app.expansion = "Jagged Earth"
        else:
            app.expansion = 'None'
    def build_spirits(self):
        app = App.get_running_app()
        app.spirit_list = app.base_spirits
        if app.branchandclaw:
            app.spirit_list = app.spirit_list + app.bc_spirits
        if app.jaggedearth:
            app.spirit_list = app.spirit_list + app.je_spirits
        if app.promopack1:
            app.spirit_list = app.spirit_list + app.pp1_spirits
        if app.promopack2:
            app.spirit_list = app.spirit_list + app.pp2_spirits
        app.spirit_list = sorted(app.spirit_list)
    def build_scenarios(self):
        app = App.get_running_app()
        scenario_list = app.base_scenarios
        app.scenarios_list = app.base_scenarios
        if app.branchandclaw:
            app.scenarios_list = app.scenarios_list + app.bc_scenarios
        if app.jaggedearth:
            app.scenarios_list = app.scenarios_list + app.je_scenarios
        if app.promopack1:
            app.scenarios_list = app.scenarios_list + app.pp1_scenarios
        if app.promopack2:
            app.scenarios_list = app.scenarios_list + app.pp2_scenarios
        self.scen_list = sorted(app.scenarios_list)   
    def build_levels(self):
        app = App.get_running_app()
        self.max_levels = ['0']
        if app.opponent != 'None':
            self.max_levels = ['1','2','3','4','5','6']

class SpiritSelectScreen(Screen):
    spirit_values = ListProperty([])
    play = NumericProperty(1)
    spirit1 = StringProperty('')
    spirit2 = StringProperty('')
    spirit3 = StringProperty('')
    spirit4 = StringProperty('')
    spirit5 = StringProperty('')
    spirit6 = StringProperty('')
    aspect1 = StringProperty('')
    aspect2 = StringProperty('')
    aspect3 = StringProperty('')
    aspect4 = StringProperty('')
    aspect5 = StringProperty('')
    aspect6 = StringProperty('')
    spirit1_aspects = ListProperty([])
    spirit1_has_aspect = BooleanProperty(False)
    spirit2_aspects = ListProperty([])
    spirit2_has_aspect = BooleanProperty(False)
    spirit3_aspects = ListProperty([])
    spirit3_has_aspect = BooleanProperty(False)
    spirit4_aspects = ListProperty([])
    spirit4_has_aspect = BooleanProperty(False)
    spirit5_aspects = ListProperty([])
    spirit5_has_aspect = BooleanProperty(False)
    spirit6_aspects = ListProperty([])
    spirit6_has_aspect = BooleanProperty(False)
    def on_enter(self):
        app = App.get_running_app()
        self.spirit_values = app.spirit_list
        app.currentPhase = 'SpiritSelect'
        write_state()
        self.play = int(app.players)
        self.spirit1 = app.spirits[0]
        self.spirit2 = app.spirits[1]
        self.spirit3 = app.spirits[2]
        self.spirit4 = app.spirits[3]
        self.spirit5 = app.spirits[4]
        self.spirit6 = app.spirits[5]
        self.aspect1 = app.aspects[0]
        self.aspect2 = app.aspects[1]
        self.aspect3 = app.aspects[2]
        self.aspect4 = app.aspects[3]
        self.aspect5 = app.aspects[4]
        self.aspect6 = app.aspects[5]
    def on_select_spirit(self, player, value):
        app = App.get_running_app()
        if player == 1:
            if len(app.spirit_aspects[value]) == 0:
                self.spirit1_has_aspect = False
            else:
                for item in app.spirit_aspects[value]:
                    if app.branchandclaw:
                        if item.split(':')[0] == 'bc':
                            self.spirit1_aspects.append(item.split(':')[1])
                    if app.jaggedearth:
                        if item.split(':')[0] == 'je':
                            self.spirit1_aspects.append(item.split(':')[1])
                    if app.promopack1:
                        if item.split(':')[0] == 'pp1':
                            self.spirit1_aspects.append(item.split(':')[1])
                    if app.promopack2:
                        if item.split(':')[0] == 'pp2':
                            self.spirit1_aspects.append(item.split(':')[1])
                if len(self.spirit1_aspects) == 0:
                    self.spirit1_has_aspect = False
                else:
                    self.spirit1_has_aspect = True
                    self.spirit1_aspects = ['None'] + self.spirit1_aspects
            app.spirits[0] = value
        if player == 2:
            if len(app.spirit_aspects[value]) == 0:
                self.spirit2_has_aspect = False
            else:
                for item in app.spirit_aspects[value]:
                    if app.branchandclaw:
                        if item.split(':')[0] == 'bc':
                            self.spirit2_aspects.append(item.split(':')[1])
                    if app.jaggedearth:
                        if item.split(':')[0] == 'je':
                            self.spirit2_aspects.append(item.split(':')[1])
                    if app.promopack1:
                        if item.split(':')[0] == 'pp1':
                            self.spirit2_aspects.append(item.split(':')[1])
                    if app.promopack2:
                        if item.split(':')[0] == 'pp2':
                            self.spirit2_aspects.append(item.split(':')[1])
                if len(self.spirit2_aspects) == 0:
                    self.spirit2_has_aspect = False
                else:
                    self.spirit2_has_aspect = True
                    self.spirit2_aspects = ['None'] + self.spirit2_aspects
            app.spirits[1] = value
        if player == 3:
            if len(app.spirit_aspects[value]) == 0:
                self.spirit3_has_aspect = False
            else:
                for item in app.spirit_aspects[value]:
                    if app.branchandclaw:
                        if item.split(':')[0] == 'bc':
                            self.spirit3_aspects.append(item.split(':')[1])
                    if app.jaggedearth:
                        if item.split(':')[0] == 'je':
                            self.spirit3_aspects.append(item.split(':')[1])
                    if app.promopack1:
                        if item.split(':')[0] == 'pp1':
                            self.spirit3_aspects.append(item.split(':')[1])
                    if app.promopack2:
                        if item.split(':')[0] == 'pp2':
                            self.spirit3_aspects.append(item.split(':')[1])
                if len(self.spirit3_aspects) == 0:
                    self.spirit3_has_aspect = False
                else:
                    self.spirit3_has_aspect = True
                    self.spirit3_aspects = ['None'] + self.spirit3_aspects                        
            app.spirits[2] = value
        if player == 4:
            if len(app.spirit_aspects[value]) == 0:
                self.spirit4_has_aspect = False
            else:
                for item in app.spirit_aspects[value]:
                    if app.branchandclaw:
                        if item.split(':')[0] == 'bc':
                            self.spirit4_aspects.append(item.split(':')[1])
                    if app.jaggedearth:
                        if item.split(':')[0] == 'je':
                            self.spirit4_aspects.append(item.split(':')[1])
                    if app.promopack1:
                        if item.split(':')[0] == 'pp1':
                            self.spirit4_aspects.append(item.split(':')[1])
                    if app.promopack2:
                        if item.split(':')[0] == 'pp2':
                            self.spirit4_aspects.append(item.split(':')[1])
                if len(self.spirit4_aspects) == 0:
                    self.spirit4_has_aspect = False
                else:
                    self.spirit4_has_aspect = True
                    self.spirit4_aspects = ['None'] + self.spirit4_aspects
            app.spirits[3] = value
        if player == 5:
            if len(app.spirit_aspects[value]) == 0:
                self.spirit5_has_aspect = False
            else:
                for item in app.spirit_aspects[value]:
                    if app.branchandclaw:
                        if item.split(':')[0] == 'bc':
                            self.spirit5_aspects.append(item.split(':')[1])
                    if app.jaggedearth:
                        if item.split(':')[0] == 'je':
                            self.spirit5_aspects.append(item.split(':')[1])
                    if app.promopack1:
                        if item.split(':')[0] == 'pp1':
                            self.spirit5_aspects.append(item.split(':')[1])
                    if app.promopack2:
                        if item.split(':')[0] == 'pp2':
                            self.spirit5_aspects.append(item.split(':')[1])
                if len(self.spirit5_aspects) == 0:
                    self.spirit5_has_aspect = False
                else:
                    self.spirit5_has_aspect = True
                    self.spirit5_aspects = ['None'] + self.spirit5_aspects
            app.spirits[4] = value
        if player == 6:
            if len(app.spirit_aspects[value]) == 0:
                self.spirit6_has_aspect = False
            else:
                for item in app.spirit_aspects[value]:
                    if app.branchandclaw:
                        if item.split(':')[0] == 'bc':
                            self.spirit6_aspects.append(item.split(':')[1])
                    if app.jaggedearth:
                        if item.split(':')[0] == 'je':
                            self.spirit6_aspects.append(item.split(':')[1])
                    if app.promopack1:
                        if item.split(':')[0] == 'pp1':
                            self.spirit6_aspects.append(item.split(':')[1])
                    if app.promopack2:
                        if item.split(':')[0] == 'pp2':
                            self.spirit6_aspects.append(item.split(':')[1])
                if len(self.spirit6_aspects) == 0:
                    self.spirit6_has_aspect = False
                else:
                    self.spirit6_has_aspect = True
                    self.spirit6_aspects = ['None'] + self.spirit6_aspects
            app.spirits[5] = value

    def on_select_aspect(self, player, value):
        app = App.get_running_app()
        app.aspects[player-1] = value
        
#Board Setup Screen
#Corresponds to kivy main
class BoardSetupScreen(Screen):
    text = StringProperty('')
    def on_enter(self):                 #override of on_enter, runs when screen is constructed
        app = App.get_running_app()
        app.currentPhase = 'BoardSetup'
        write_state()
        start = ''
        fear = ''
        invaders = ''
        exsetup = ''
        ft = ''
        bt = ''
        list = []
        if app.fear_cards[app.opponent][int(app.level)-1] != '':
            fear = 'Fear Cards ' + app.fear_cards[app.opponent][int(app.level)-1] + '\n'  #calculate fear cards into local fear
        if fear != '':
            list.append({'image': app.icons['Fear Cards'], 'text': fear})
        #loop to add all setup changes together (cumulative) from app.setup_changes up to opponent level into local start
        for x in range(int(app.level)):
            start += app.setup_changes[app.opponent][x]
        if start != '':
            list.append({'image': app.icons[app.opponent], 'text': start})    
        invaders = 'Invader Deck: ' + app.invader_deck[app.opponent][int(app.level)-1]  + '\n' #set local invaders to invader deck based on opponent & level
        if invaders != '':
            list.append({'image': app.icons['Invader Cards'], 'text': invaders})
        if app.thematic:
            exsetup = 'Follow the icons on the thematic map for all invaders and tokens.'
        else:
            exsetup = app.expansion_setup[app.expansion]     #copy app.expansion_setup into local exsetup
        if exsetup != '':
            list.append({'image': app.icons['Land'], 'text': exsetup})
        if app.opponent == 'England' and int(app.level) == 6:
            fear_per = 5
        else:
            fear_per = 4

        app.fear_tokens = fear_per * int(app.players)    #calculate number of fear tokens into global fear_tokens
        
        ft = 'Fear Tokens: ' + str(app.fear_tokens) + '\n'   #copy global fear_tokens into local ft
        if ft != '':
            list.append({'image': app.icons['fear tokens'], 'text': ft})
        blight_tokens = (2 * int(app.players)) + 1
        bt = 'Blight Tokens: ' + str(blight_tokens)+ '\n'
        if bt != '':
            list.append({'image': app.icons['blight tokens'], 'text': bt})
        #self.text = '\n'.join([start, fear, invaders, exsetup, ft, bt])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
        
class SpiritSetupScreen(Screen):
    spirits_text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'SpiritSetup'
        self.spirits_text = ''
        list = []
        for spirit in app.spirits:
            if spirit != 'None':
                #self.spirits_text = self.spirits_text + x + ': ' + app.spirit_setup[x] + '\n'
                list.append({'image': app.icons[spirit], 'text': app.spirit_setup[spirit]})
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
        
class FirstExploreScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'FirstExplore'
        write_state()
        description = ''
        rules = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})
        if app.displayopts[app.currentPhase]['rules']:
            for x in range(int(app.level)):
                rules += app.firstexplorescreen_rules[app.opponent][x]
        if rules != '':
            list.append({'image': 'resources/icon.png', 'text': rules})
        #self.text = '\n'.join([description + rules])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
        
#Growth Phase Screen
#Corresponds to Kivy Growth
#First screen with stage and blight tracking.  
#Global variable blight (values Blighted, Normal) and global variable Stage (Values I, II, III)
#Local BooleanProperty is used to control checkbox/button state in Kivy
#Done individually per screen to allow for modifications to screens as needed
#(For example, on explorer screen, stage II updates the stage2 flag field)
class GrowthScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'Growth'
        write_state()
        app.turn = app.turn +1
        self.text = ''
        description = ''
        opprules = ""
        allrules = ""
        badlands = ""
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})
        spirits_text = ''
        if app.displayopts[app.currentPhase]['spirits']:
            for x in app.spirits:
                if app.spirit_growth_count[x] > 1:
                    spirits_text = 'Spirits with more than one Growth action can use energy gained from one action to pay for another.\n'
        if spirits_text != '':
            list.append({'image': app.icons['spirits text'], 'text': spirits_text})

        
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if app.displayopts[app.currentPhase]['opponent']:
            for x in range(int(app.level)):
                opprules += app.growthscreen_rules[app.opponent][x]
        if opprules != '':
            list.append({'image': app.icons[app.opponent], 'text': opprules})
        if app.displayopts[app.currentPhase]['all']:
            for x in range(int(app.level)):
                allrules += app.allscreen_rules[app.opponent][x]
        if allrules != '':
            list.append({'image': app.icons[app.opponent], 'text': allrules})
        #self.text = '\n'.join([description, spirits_text, opprules, badlands, allrules])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
        
        
class EnergyScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'Energy'
        write_state()
        description = ''
        opprules = ""
        allrules = ""
        badlands = ""
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})

        #self.text = '\n'.join([description,opprules, badlands, allrules])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
        
class PowerCardsScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'PowerCards'
        write_state()
        description = ''
        opprules = ""
        allrules = ""
        badlands = ""
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})

        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if app.displayopts[app.currentPhase]['opponent']:
            for x in range(int(app.level)):
                opprules += app.powercardscreen_rules[app.opponent][x]
        if opprules != '':
            list.append({'image': app.icons[app.opponent], 'text': opprules}) 
        if app.displayopts[app.currentPhase]['all']:
            for x in range(int(app.level)):
                allrules += app.allscreen_rules[app.opponent][x]
        if allrules != '':
            list.append({'image': app.icons[app.opponent], 'text': allrules})
        #self.text = '\n'.join([description,opprules, badlands, allrules])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
        
class FastPowerScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        
        app.currentPhase = 'FastPower'
        write_state()
        description = ''
        opprules = ""
        allrules = ""
        badlands = ""
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if app.displayopts[app.currentPhase]['opponent']:
            for x in range(int(app.level)):
                opprules += app.fastpowerscreen_rules[app.opponent][x]
        if opprules != '':
            list.append({'image': app.icons[app.opponent], 'text': opprules}) 
        if app.displayopts[app.currentPhase]['all']:
            for x in range(int(app.level)):
                allrules += app.allscreen_rules[app.opponent][x]
        if allrules != '':
            list.append({'image': app.icons[app.opponent], 'text': allrules})
        #self.text = '\n'.join([description,opprules, badlands, allrules])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
        
class BlightedIslandScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'BlightedIsland'
        write_state()
        opprules = ""
        allrules = ""
        badlands = ""
        description = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})            
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if app.displayopts[app.currentPhase]['opponent']:
            for x in range(int(app.level)):
                opprules += app.blightedislandscreen_rules[app.opponent][x]
        if opprules != '':
            list.append({'image': app.icons[app.opponent], 'text': opprules}) 
        if app.displayopts[app.currentPhase]['all']:
            for x in range(int(app.level)):
                allrules += app.allscreen_rules[app.opponent][x]
        if allrules != '':
            list.append({'image': app.icons[app.opponent], 'text': allrules})
        #self.text = '\n'.join([description,opprules, badlands, allrules])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
        
class EventScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'Event'
        write_state()
        description = ''
        opprules = ""
        allrules = ""
        badlands = ""
        discard = ""
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description}) 
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if app.displayopts[app.currentPhase]['opponent']:
            for x in range(int(app.level)):
                opprules += app.eventscreen_rules[app.opponent][x]
        if opprules != '':
            list.append({'image': app.icons[app.opponent], 'text': opprules})                
        if app.displayopts[app.currentPhase]['all']:
            for x in range(int(app.level)):
                allrules += app.allscreen_rules[app.opponent][x]
        if allrules != '':
            list.append({'image': app.icons[app.opponent], 'text': allrules})                
        if app.displayopts[app.currentPhase]['discard']:
            if app.turn == 1:
                discard += 'Turn over the first event card, but discard it with no action.\n'
        if discard != '':
            list.append({'image': app.icons['discard'], 'text': discard})
        #self.text = '\n'.join([description, opprules, badlands, allrules, discard])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
            
class FearScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'Fear'
        write_state()
        description = ''
        opprules = ""
        allrules = ""
        badlands = ""
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description}) 
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if app.displayopts[app.currentPhase]['opponent']:
            for x in range(int(app.level)):
                opprules += app.fearscreen_rules[app.opponent][x]
        if opprules != '':
            list.append({'image': app.icons[app.opponent], 'text': opprules})                     
        if app.displayopts[app.currentPhase]['all']:
            for x in range(int(app.level)):
                allrules += app.allscreen_rules[app.opponent][x]
        if allrules != '':
            list.append({'image': app.icons[app.opponent], 'text': allrules})   
        #self.text = '\n'.join([description,opprules, badlands, allrules])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list          
        
class HighImmigrationScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'HighImmigration'
        write_state()
        description = ''
        opprules = ""
        allrules = ""
        badlands = ""
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})            
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if app.displayopts[app.currentPhase]['opponent']:
            for x in range(int(app.level)):
                opprules += app.highimmigrationscreen_rules[app.opponent][x]
        if opprules != '':
            list.append({'image': app.icons[app.opponent], 'text': opprules})
        if app.displayopts[app.currentPhase]['all']:
            for x in range(int(app.level)):
                allrules += app.allscreen_rules[app.opponent][x]
        if allrules != '':
            list.append({'image': app.icons[app.opponent], 'text': allrules})
        #self.text = '\n'.join([description,opprules, badlands, allrules])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list   
        
class RavageScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'Ravage'
        write_state()
        description = ''
        opprules = ""
        allrules = ""
        badlands = ""
        strife = ""
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})  
        if app.displayopts[app.currentPhase]['strife']:
            if app.expansion != 'None':
                strife = 'If present, Strife Tokens block specific invaders from doing damage. Remove the token.\n'
        if strife != '':
            list.append({'image': app.icons['strife'], 'text': strife})
        if app.opponent == 'Russia' and int(app.level) ==6  and app.turn > 1:
            opprules += "After the ravage step, on each board where it added no blight: in the land with the most explorers (min 1) add one explorer and one town.\n"
        if opprules != '':
            list.append({'image': app.icons[app.opponent], 'text': opprules})
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if app.displayopts[app.currentPhase]['opponent']:
            for x in range(int(app.level)):
                opprules += app.ravagescreen_rules[app.opponent][x]
        if opprules != '':
            list.append({'image': app.icons[app.opponent], 'text': opprules})
        if app.displayopts[app.currentPhase]['all']:
            for x in range(int(app.level)):
                allrules += app.allscreen_rules[app.opponent][x]
        if allrules != '':
            list.append({'image': app.icons[app.opponent], 'text': allrules})
        #self.text = '\n'.join([description,strife,opprules, badlands, allrules])            
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list   
        
class BuildScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'Build'
        write_state()
        description = ''
        opprules = ""
        allrules = ""
        badlands = ""
        disease = ""
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description}) 
        if app.displayopts[app.currentPhase]['disease']:
            if app.expansion != 'None':
                disease = 'If present, Disease tokens prevent this build. Remove the token.\n'
        if disease != '':
            list.append({'image': app.icons['disease'], 'text': disease})
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if app.displayopts[app.currentPhase]['opponent']:
            for x in range(int(app.level)):
                opprules += app.buildscreen_rules[app.opponent][x]
        if opprules != '':
            list.append({'image': app.icons[app.opponent], 'text': opprules})
        if app.displayopts[app.currentPhase]['all']:
            for x in range(int(app.level)):
                allrules += app.allscreen_rules[app.opponent][x]
        if allrules != '':
            list.append({'image': app.icons[app.opponent], 'text': allrules})
        #self.text = '\n'.join([description,disease,opprules, badlands, allrules])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list   
        
#Explore Screen
#Corresponds to Kivy Explore
#Note extra local variable flag, and update to the on_stage_toggle method
class ExploreScreen(Screen):
    text = StringProperty('')
    list = ListProperty([])
    s2list = ListProperty([])
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'Explore'
        write_state()
        description = ''
        opprules = ""
        allrules = ""
        badlands = ""
        wilds = ""
        self.list = []
        if app.flagicon == True:
            self.s2list = [{'image': app.icons['stage2flag'], 'text': app.stage2_flag[app.opponent]}]
        else:
            self.s2list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            self.list.append({'image': app.icons[app.currentPhase], 'text': description}) 
        if app.displayopts[app.currentPhase]['wilds']:
            if app.expansion != 'None':
                wilds = 'If a wilds token is present, skip that exploration and discard one wilds token.\n'
        if wilds != '':
            self.list.append({'image': app.icons['wilds'], 'text': wilds})
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                self.list.append({'image': app.icons['badlands'], 'text': badlands})
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if app.displayopts[app.currentPhase]['opponent']:
            for x in range(int(app.level)):
                opprules += app.explorescreen_rules[app.opponent][x]
        if opprules != '':
            self.list.append({'image': app.icons[app.opponent], 'text': opprules})
        if app.displayopts[app.currentPhase]['all']:
            for x in range(int(app.level)):
                allrules += app.allscreen_rules[app.opponent][x]
        if allrules != '':
            self.list.append({'image': app.icons[app.opponent], 'text': allrules})
        #self.text = '\n'.join([description,wilds,opprules, badlands, allrules])
        
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = self.list + self.s2list
    def on_stage_toggle(self):
        app = App.get_running_app()
        if app.flagicon == True:
            self.s2list = [{'image': app.icons['stage2flag'], 'text': app.stage2_flag[app.opponent]}]
        else:
            self.s2list = []
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = self.list + self.s2list
        
class AdvanceCardsScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'AdvanceCards'
        write_state()
        opprules = ""
        allrules = ""
        description = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]

        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if app.displayopts[app.currentPhase]['opponent']:
            for x in range(int(app.level)):
                opprules += app.advancecardsscreen_rules[app.opponent][x]
        if opprules != '':
            list.append({'image': app.icons[app.opponent], 'text': opprules})
        if app.displayopts[app.currentPhase]['all']:
            for x in range(int(app.level)):
                allrules += app.allscreen_rules[app.opponent][x]
        if allrules != '':
            list.append({'image': app.icons[app.opponent], 'text': allrules})
        #self.text = '\n'.join([description,opprules, badlands, allrules])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
        
class SlowPowerScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'SlowPower'
        write_state()
        opprules = ""
        allrules = ""
        badlands = ""
        description = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if app.displayopts[app.currentPhase]['opponent']:
            for x in range(int(app.level)):
                opprules += app.slowpowerscreen_rules[app.opponent][x]
        if opprules != '':
            list.append({'image': app.icons[app.opponent], 'text': opprules})
        if app.displayopts[app.currentPhase]['all']:
            for x in range(int(app.level)):
                allrules += app.allscreen_rules[app.opponent][x]
        if allrules != '':
            list.append({'image': app.icons[app.opponent], 'text': allrules})
        #self.text = '\n'.join([description,opprules, badlands, allrules])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
            
class TimePassesScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'TimePasses'
        write_state()
        description = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        #self.text = '\n'.join([description,opprules, allrules])
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
        
store = JsonStore('sipt.json')
def write_state():
    app = App.get_running_app()
    store.put('branchandclaw', value=app.branchandclaw)
    store.put('jaggedearth', value=app.jaggedearth)
    store.put('promopack1', value=app.promopack1)
    store.put('promopack2', value=app.promopack2)
    store.put('expansion', value=app.expansion)
    store.put('opponent', value=app.opponent)
    store.put('thematic', value=app.thematic)
    store.put('spirits', value=app.spirits)
    store.put('aspects', value=app.aspects)
    store.put('scenario', value=app.scenario)
    store.put('level', value=app.level)
    store.put('stage', value=app.stage)
    store.put('blight', value=app.blight)
    store.put('players', value=app.players)
    store.put('fear_tokens', value=app.fear_tokens)
    store.put('turn', value=app.turn)
    store.put('previousPhase', value=app.previousPhase)
    store.put('opponent_list', value=app.opponent_list)
    store.put('currentPhase', value=app.currentPhase)
    store.put('spirit_list', value=app.spirit_list)
    store.put('scenarios_list', value=app.scenarios_list)


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        app = App.get_running_app()
        self.data = []

  
#Screen manager that controls which screen is which
class MainManager(ScreenManager):
    pass

class PhaseManager(ScreenManager):
    pass

#Loading kivy file not needed, as long as the name matches the python script name.
#presentation = Builder.load_file("spiritIsland.kv")


#Main App
#Referenced as "app.local" in Kivy screens
class MainApp(App):
    fastpowernext = StringProperty('Event')
    flagicon = BooleanProperty(False)
    stage2flag = StringProperty('')
    s2list = ListProperty([])
    ## Imports from data.py
    base_opp = data.base_opp
    bc_opp = data.bc_opp
    je_opp = data.je_opp
    pp2_opp = data.pp2_opp
    base_spirits = data.base_spirits
    bc_spirits = data.bc_spirits
    je_spirits = data.je_spirits
    pp1_spirits = data.pp1_spirits
    pp2_spirits = data.pp2_spirits
    spirit_aspects = data.spirit_aspects
    spirit_setup = data.spirit_setup
    spirit_growth_count = data.spirit_growth_count
    base_scenarios = data.base_scenarios
    bc_scenarios = data.bc_scenarios
    je_scenarios = data.je_scenarios
    pp1_scenarios = data.pp1_scenarios
    pp2_scenarios = data.pp2_scenarios
    fear_cards = data.fear_cards
    setup_changes = data.setup_changes
    expansion_setup = data.expansion_setup
    invader_deck = data.invader_deck
    stage2_flag = data.stage2_flag
    allscreen_rules = data.allscreen_rules
    opponentmod_rules = data.opponentmod_rules
    firstexplorescreen_rules = data.firstexplorescreen_rules
    growthscreen_rules = data.growthscreen_rules
    energyscreen_rules = data.energyscreen_rules
    powercardscreen_rules = data.powercardscreen_rules
    fastpowerscreen_rules = data.fastpowerscreen_rules
    blightedislandscreen_rules = data.blightedislandscreen_rules
    eventscreen_rules = data.eventscreen_rules
    fearscreen_rules = data.fearscreen_rules
    highimmigrationscreen_rules = data.highimmigrationscreen_rules
    ravagescreen_rules = data.ravagescreen_rules
    buildscreen_rules = data.buildscreen_rules
    explorescreen_rules = data.explorescreen_rules
    advancecardsscreen_rules = data.advancecardsscreen_rules
    slowpowerscreen_rules = data.slowpowerscreen_rules
    timepassesscreen_rules = data.timepassesscreen_rules
    screenTitles = data.screenTitles
    screenDescriptions = data.screenDescriptions
    icons = data.icons
    ##
    data = ListProperty([])
    
    ## Global variables
    branchandclaw = False
    jaggedearth = False
    promopack1 = False
    promopack2 = False
    expansion = 'None'          #global variable for expansion
    opponent = 'None'           #global variable for opponent
    thematic = False
    spirits = ['None', 'None', 'None', 'None', 'None', 'None']
    aspects = ['None', 'None', 'None', 'None', 'None', 'None']
    scenario = 'None'
    level = '0'              #global variable for opponent level
    stage = 'I'             #global variable for current stage
    blight = 'Healthy'      #global variable for current blight (Healthy, Blighted)
    players = 1             #global variable for player count
    fear_tokens = 4         #global variable for fear token count
    turn = 0
    previousPhase = []
    currentPhase = 'FirstExplore'
    use_timer = True
    timer_seconds = 180
    displayopts = {}
    spirit_list = base_spirits
    scenarios_list = base_scenarios
    opponent_list = base_opp
    ##
    
       
    def build(self):
        if int(self.config.get('timeroptions', 'usetimer')) == 0:
            self.use_timer = False
        else:
            self.use_timer = True
        self.timer_seconds = int(self.config.get('timeroptions', 'timerseconds'))
        self.displayopts['FirstExplore'] = {}
        self.displayopts['All'] = {}
        for item in ['phase', 'badlands']:
            self.displayopts['All'][item] = int(self.config.get('All', item))
        self.displayopts['FirstExplore'] = {}
        for item in ['rules']:
            self.displayopts['FirstExplore'][item] = int(self.config.get('FirstExplore', item))
        self.displayopts['Growth'] = {}
        for item in ['opponent', 'all', 'spirits']:
            self.displayopts['Growth'][item] = int(self.config.get('Growth', item))
        self.displayopts['PowerCards'] = {}
        for item in ['opponent', 'all']:
            self.displayopts['PowerCards'][item] = int(self.config.get('PowerCards', item))
        self.displayopts['FastPower'] = {}
        for item in ['opponent', 'all']:
            self.displayopts['FastPower'][item] = int(self.config.get('FastPower', item))
        self.displayopts['BlightedIsland'] = {}
        for item in ['opponent', 'all']:
            self.displayopts['BlightedIsland'][item] = int(self.config.get('BlightedIsland', item))
        self.displayopts['Event'] = {}
        for item in ['opponent', 'all', 'discard']:
            self.displayopts['Event'][item] = int(self.config.get('Event', item))
        self.displayopts['Fear'] = {}
        for item in ['opponent', 'all']:
            self.displayopts['Fear'][item] = int(self.config.get('Fear', item))
        self.displayopts['HighImmigration'] = {}
        for item in ['opponent', 'all']:
            self.displayopts['HighImmigration'][item] = int(self.config.get('HighImmigration', item))
        self.displayopts['Ravage'] = {}
        for item in ['opponent', 'all', 'strife']:
            self.displayopts['Ravage'][item] = int(self.config.get('Ravage', item))
        self.displayopts['Build'] = {}
        for item in ['opponent', 'all', 'disease']:
            self.displayopts['Build'][item] = int(self.config.get('Build', item))
        self.displayopts['Explore'] = {}
        for item in ['opponent', 'all', 'wilds']:
            self.displayopts['Explore'][item] = int(self.config.get('Explore', item))
        self.displayopts['AdvanceCards'] = {}
        for item in ['opponent', 'all']:
            self.displayopts['AdvanceCards'][item] = int(self.config.get('AdvanceCards', item))
        self.displayopts['SlowPower'] = {}
        for item in ['opponent', 'all']:
            self.displayopts['SlowPower'][item] = int(self.config.get('SlowPower', item))          
    def on_stop(self):
        return True

    #build_config method, sets default values for the config if no .ini exists
    def build_config(self, config):
        config.setdefaults('timeroptions', {
                                'usetimer': 1,
                                'timerseconds': '180'
                            }
                        )
        config.setdefaults('All', {
                                'phase': 1,
                                'badlands': 1
                            })
        config.setdefaults('FirstExplore', {
                                'rules': 1
                            })
        config.setdefaults('Growth', {
                                'spirits': 1,
                                'opponent': 1,
                                'all': 1,
                            })
        config.setdefaults('PowerCards', {
                                'opponent': 1,
                                'all': 1,
                            })
        config.setdefaults('FastPower', {
                                'opponent': 1,
                                'all': 1,
                            })
        config.setdefaults('BlightedIsland', {
                                'opponent': 1,
                                'all': 1,
                            })  
        config.setdefaults('Event', {
                                'opponent': 1,
                                'all': 1,
								'discard': 1
                            })
        config.setdefaults('Fear', {
                                'opponent': 1,
                                'all': 1,
                            })
        config.setdefaults('HighImmigration', {
                                'opponent': 1,
                                'all': 1,
                            })
        config.setdefaults('Ravage', {
                                'opponent': 1,
                                'all': 1,
                                'strife': 1
                            })
        config.setdefaults('Build', {
                                'opponent': 1,
                                'all': 1,
                                'disease': 1
                            })
        config.setdefaults('Explore', {
                                'opponent': 1,
                                'all': 1,
                                'wilds': 1
                            })
        config.setdefaults('AdvanceCards', {
                                'opponent': 1,
                                'all': 1,
                            })
        config.setdefaults('SlowPower', {
                                'opponent': 1,
                                'all': 1,
                            })
                     
    #build_settigns loads the json file, and  defines the name for the panel in the settings screen
    def build_settings(self, settings):
        settings.add_json_panel('Spirit Island',
                                self.config,
                                data=settings_json)
        
    #on_config_change method - called when a user changes anything in settings screen, similar to the build.                            
    def on_config_change(self, config, section, key, value):
        if section == 'timeroptions':
            if int(self.config.get('timeroptions', 'usetimer')) == 0:
                self.use_timer = False
            else:
                self.use_timer = True
            self.timer_seconds = int(self.config.get('timeroptions', 'timerseconds'))
        else:
            #displayopts[section]={}
            self.displayopts[section][key]=int(value)
            
    def on_stage_toggle(self, value):
        if value == 'II':
            if self.opponent != 'None':
                self.flagicon = True
                self.stage2flag = self.stage2_flag[self.opponent]
                self.stage2flag = self.stage2_flag[self.opponent]
            else:
                self.flagicon = False
                self.stage2flag = ''
        else:
            self.flagicon = False
            self.stage2flag = ''
        if self.currentPhase == 'Explore':
            self.root.get_screen('Phase').ids.PhaseManager.get_screen(self.currentPhase).on_stage_toggle()
        return self

        
        
MainApp().run()


