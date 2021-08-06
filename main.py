from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
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
import random
import math
import data # this louds our variables from data.py

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
    def __init__(self, **kwargs):
        super(PhaseScreen, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
    def _on_keyboard_down(self, instance, keyboard, keycode, other, other1):
            if keycode == 40 or keycode == 128:  # 40 - Enter key pressed
                phase = App.get_running_app().root.get_screen('Phase').ids.PhaseManager #.get_screen(app.currentPhase).ids.RV
                phase.current = self.on_next_Phase()
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
            nextP = 'MapLayout'
        if app.currentPhase == 'MapLayout':        
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
            if app.blight != 'Healthy' and app.blightscreeninactive == False:
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
            England3 = False
            England4 = False
            for x in range(len(app.opponents)):
                if app.opponents[x] == 'England' and int(app.levels[x]) == 3:
                    England3 = True
                elif app.opponents[x] == 'England' and int(app.levels[x]) >=4:
                    England4 = True
            if England3 == True  and app.stage != "III" and app.turn > 1:
                nextP = 'HighImmigration'
            elif England4 == True and app.turn > 1:
                nextP = 'HighImmigration'
            elif app.turn > 1:
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
        elif nextP == 'MapLayout':
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
        if app.currentPhase == 'Growth':
            app.turn = app.turn - 1
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
        elif prev == 'MapLayout':
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
        self.ehealth = '1'
        self.edamage = '1'
        self.thealth = '2'
        self.tdamage = '2'
        self.chealth = '3'
        self.cdamage = '3'
        self.dhealth = '2'
        self.ddamage = '2'
        for x in range(len(app.opponents)):
            self.ehealth = str(int(self.ehealth) + app.opponentmod_rules[app.opponents[x]][int(app.levels[x])][0])
            self.edamage = str(int(self.edamage) + app.opponentmod_rules[app.opponents[x]][int(app.levels[x])][4])
            self.thealth = str(int(self.thealth) + app.opponentmod_rules[app.opponents[x]][int(app.levels[x])][1])
            self.tdamage = str(int(self.tdamage) + app.opponentmod_rules[app.opponents[x]][int(app.levels[x])][5])
            self.chealth = str(int(self.chealth) + app.opponentmod_rules[app.opponents[x]][int(app.levels[x])][2])
            self.cdamage = str(int(self.cdamage) + app.opponentmod_rules[app.opponents[x]][int(app.levels[x])][6]) 
            self.dhealth = str(int(self.dhealth) + app.opponentmod_rules[app.opponents[x]][int(app.levels[x])][3])
            self.ddamage = str(int(self.ddamage) + app.opponentmod_rules[app.opponents[x]][int(app.levels[x])][7])
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
        app.opponents = (store.get('opponents')['value'])
        app.thematic = (store.get('thematic')['value'])
        app.extraboard = (store.get('extraboard')['value'])
        app.spirits = (store.get('spirits')['value'])
        app.aspects = (store.get('aspects')['value'])
        app.scenario = (store.get('scenario')['value'])
        app.levels = (store.get('levels')['value'])
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

        app.fromLoad = True
        self.calc_health_damage()
        app.stage2_flag['Scotland'] = 'Loss condition: If the invader card has a flag:\nOn the single board with the most coastal towns/cities add one town to the '+ str(app.players) +' lands with the fewest towns.\n'
        app.loss_rules['Habsburg'] = 'Loss condition: Track how many blight come off the blight cards during ravages that do 8+ damage to the land. If that number ever exceeds ' + str(app.players) +' , the invaders win.\n'
        if app.blight != 'Healthy':
            self.blighted = True
        else:
            self.blighted = False
        self.on_stage_toggle(app.stage)
        if app.currentPhase == 'Main':
            nextP = 'SpiritSelect'
        if app.currentPhase == 'SpiritSelect':
            nextP = 'MapLayout'
        if app.currentPhase == 'MapLayout':
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
            if app.blight != 'Healthy' and app.blightscreeninactive == False:
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
            England3 = False
            England4 = False
            for x in range(len(app.opponents)):
                if app.opponents[x] == 'England' and int(app.levels[x]) == 3:
                    England3 = True
                elif app.opponents[x] == 'England' and int(app.levels[x]) >=4:
                    England4 = True
            if England3 == True  and app.stage != "III" and app.turn > 1:
                nextP = 'HighImmigration'
            elif England4 == True and app.turn > 1:
                nextP = 'HighImmigration'
            elif app.turn > 1:
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
        elif nextP == 'MapLayout':
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
    extrab = BooleanProperty(False)
    opp = ListProperty(['None', 'None'])
    lvl = ListProperty(['',''])
    play = StringProperty('1')
    max_play = ListProperty(['1','2','3','4'])
    max_levels = ListProperty([['0'],['0']])
    next = StringProperty('BoardSetup')
    opp_list = ListProperty()
    scen_list = ListProperty()
    diff = StringProperty('0')
    notoke = BooleanProperty(False)
    notoken_disabled = BooleanProperty(True)
    scen = StringProperty('None')
    def on_enter(self):
        app = App.get_running_app()
        self.scen_list = app.scenarios_list
        app.currentPhase = 'Main'
        if app.branchandclaw:
            self.bc = True
        self.je = app.jaggedearth
        self.pp1 = app.promopack1
        self.pp2 = app.promopack2
        self.opp = app.opponents
        self.play = str(app.players)
        self.lvl = app.levels
        self.theme = app.thematic
        self.extrab = app.extraboard
        self.opp_list = sorted(app.opponent_list)
        self.diff = app.difficulty
        self.notoke = app.notokens
        self.scen = app.scenario
    def bc_clicked(self, value):
        app = App.get_running_app()
        if value == True:
            app.branchandclaw = True
        else:
            app.branchandclaw = False
        self.build_expansions()
        self.build_spirits()
        self.build_scenarios()
        for x in range(len(self.opp)):
            if self.opp[x] not in self.opp_list:
                self.opponent_clicked(x, 'None')
        self.eval_tokens()
    def je_clicked(self, value):
        app = App.get_running_app()
        if value == True:
            app.jaggedearth = True
        else:
            app.jaggedearth = False
        self.build_expansions()
        self.build_spirits()
        self.build_scenarios()
        for x in range(len(self.opp)):
            if self.opp[x] not in self.opp_list:
                self.opponent_clicked(x, 'None')  
        if self.play not in self.max_play:
            self.players_clicked('0')
        self.eval_tokens()
    def promo1_clicked(self, value):
        app = App.get_running_app()
        if value == True:
            app.promopack1 = True
        else:
            app.promopack1 = False
        self.build_expansions()
        self.build_spirits()
        self.build_scenarios()
        for x in range(len(self.opp)):
            if self.opp[x] not in self.opp_list:
                self.opponent_clicked(x, 'None')
    def promo2_clicked(self, value):
        app = App.get_running_app()
        if value == True:
            app.promopack2 = True
        else:
            app.promopack2 = False
        self.build_expansions()
        self.build_spirits()
        self.build_scenarios()
        for x in range(len(self.opp)):
            if self.opp[x] not in self.opp_list:
                self.opponent_clicked(x, 'None')
    def thematic_clicked(self, value):
        app = App.get_running_app()
        if value == True:
            app.thematic = True
        else:
            app.thematic = False
            self.notoke = False
            app.notoke = False
        self.calculate_difficulty()
        self.eval_tokens()
    def eval_tokens(self):
        app = App.get_running_app()
        if app.thematic == True and (app.branchandclaw == True or app.jaggedearth == True):
            self.notoken_disabled = False
        else:
            self.notoken_disabled = True
    def notokens_clicked(self, value):
        app = App.get_running_app()
        self.notoke = value
        app.notokens = value
        self.calculate_difficulty()
    def extraboard_clicked(self,value):
        app = App.get_running_app()
        if value == True:
            app.extraboard = True
        else:
            app.extraboard = False
        self.calculate_difficulty()
    def opponent_clicked(self, num, value):
        app = App.get_running_app()
        if(value == 'Random'):
            rlist = app.opponent_list[:]
            rlist.remove('Random')
            rlist.remove('None')
            value = random.choice(rlist)
            self.opp[num] = value
        app.opponents[num] = value
        self.opp[num] = value
        self.build_levels(num)
        self.lvl[num] = app.levels[num]
        if self.opp[num] == 'None':
            self.level_clicked(num, '0')
        self.calculate_difficulty()
    def scenario_clicked(self, value):
        app = App.get_running_app()
        self.scen = value
        app.scenario = value
        self.calculate_difficulty()
    def level_clicked(self, num, value):
        app = App.get_running_app()
        app.levels[num] = value
        self.lvl[num] = app.levels[num]
        self.calculate_difficulty()
    def players_clicked(self, value):
        app = App.get_running_app()
        app.players = value
        self.play = app.players
        app.stage2_flag['Scotland'] = 'Loss condition: If the invader card has a flag:\nOn the single board with the most coastal towns/cities add one town to the '+ str(app.players) +' lands with the fewest towns.\n'
        app.loss_rules['Habsburg'] = 'Loss condition: Track how many blight come off the blight cards during ravages that do 8+ damage to the land. If that number ever exceeds ' + str(app.players) +' , the invaders win.\n'
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
        self.calculate_difficulty()
    def build_levels(self, num):
        app = App.get_running_app()
        if app.opponents[num] == 'None':
            self.max_levels[num] = ['0']
        else:
            self.max_levels[num] = ['0','1','2','3','4','5','6']
    def calculate_difficulty(self):
        app = App.get_running_app()
        d1 = app.opponent_difficulty[app.opponents[0]][int(app.levels[0])]
        d2 = app.opponent_difficulty[app.opponents[1]][int(app.levels[1])]
        ds = app.scenario_difficulty[app.scenario]
        dh = max(d1,d2)
        dl = 0.5 * float(min(d1,d2))
        dl = math.ceil(dl)
        ad = float(dh) + dl
        if app.thematic == True:
            if app.branchandclaw == False and app.jaggedearth == False:
                ad = ad + 3
            else:
                if self.notoke == True:
                    ad = ad + 3
                else:
                    ad = ad + 1
        if app.extraboard:
            eb = ad/3
            eb = math.ceil(eb)
            ad = ad + eb + 2
        self.diff = str(int(ad + ds))
        app.difficulty = self.diff

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
        ## Testing Deck Calculator. Uncomment one or two lines to see the invader and fear decks
        #app.scotland_decks(4)
        #app.russia_decks(4)
        #app.england_decks(4)
        #app.bp_decks(4)
        #app.sweden_decks(4)
        #app.france_decks(4)
        #app.habsburg_decks(4)
        self.spirit_values = sorted(app.spirit_list)
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
        rselect = False
        if player == 1:
            if(value == 'Random'):
                rselect = True
                rlist = app.spirit_list[:]
                rlist.remove('Random')
                rlist.remove('None')
                value = random.choice(rlist)
            if len(app.spirit_aspects[value]) == 0:
                self.spirit1_has_aspect = False
            else:
                self.spirit1_aspects = []
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
                if rselect == True:
                    alist = self.spirit1_aspects[:]
                    #alist.remove('None')
                    aspvalue = random.choice(alist)
                    self.aspect1 = aspvalue
                    app.aspects[0] = aspvalue
                    self.aspect1 = app.aspects[0]
            self.spirit1 = value
            app.spirits[0] = value
            self.spirit1 = app.spirits[0]
        if player == 2:
            if(value == 'Random'):
                rselect = True
                rlist = app.spirit_list[:]
                rlist.remove('Random')
                rlist.remove('None')
                value = random.choice(rlist)
            if len(app.spirit_aspects[value]) == 0:
                self.spirit2_has_aspect = False
            else:
                self.spirit2_aspects = []
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
                if rselect == True:
                    alist = self.spirit2_aspects[:]
                    #alist.remove('None')
                    aspvalue = random.choice(alist)
                    self.aspect2 = aspvalue
                    app.aspects[1] = aspvalue
                    self.aspect2 = app.aspects[1]
            self.spirit2 = value
            app.spirits[1] = value
            self.spirit2 = app.spirits[1]
        if player == 3:
            if(value == 'Random'):
                rselect = True
                rlist = app.spirit_list[:]
                rlist.remove('Random')
                rlist.remove('None')
                value = random.choice(rlist)
            if len(app.spirit_aspects[value]) == 0:
                self.spirit3_has_aspect = False
            else:
                self.spirit3_aspects = []
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
                if rselect == True:
                    alist = self.spirit3_aspects[:]
                    #alist.remove('None')
                    aspvalue = random.choice(alist)
                    self.aspect3 = aspvalue
                    app.aspects[2] = aspvalue
                    self.aspect3 = app.aspects[2]
            self.spirit3 = value
            app.spirits[2] = value
            self.spirit3 = app.spirits[2]
        if player == 4:
            if(value == 'Random'):
                rselect = True
                rlist = app.spirit_list[:]
                rlist.remove('Random')
                rlist.remove('None')
                value = random.choice(rlist)
            if len(app.spirit_aspects[value]) == 0:
                self.spirit4_has_aspect = False
            else:
                self.spirit4_aspects = []
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
                if rselect == True:
                    alist = self.spirit4_aspects[:]
                    #alist.remove('None')
                    aspvalue = random.choice(alist)
                    self.aspect4 = aspvalue
                    app.aspects[3] = aspvalue
                    self.aspect4 = app.aspects[3]
            self.spirit4 = value
            app.spirits[3] = value
            self.spirit4 = app.spirits[3]
        if player == 5:
            if(value == 'Random'):
                rselect = True
                rlist = app.spirit_list[:]
                rlist.remove('Random')
                rlist.remove('None')
                value = random.choice(rlist)
            if len(app.spirit_aspects[value]) == 0:
                self.spirit5_has_aspect = False
            else:
                self.spirit5_aspects = []
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
                if rselect == True:
                    alist = self.spirit5_aspects[:]
                    #alist.remove('None')
                    aspvalue = random.choice(alist)
                    self.aspect5 = aspvalue
                    app.aspects[4] = aspvalue
                    self.aspect5 = app.aspects[4]
            self.spirit5 = value
            app.spirits[4] = value
            self.spirit5 = app.spirits[4]
        if player == 6:
            if(value == 'Random'):
                rselect = True
                rlist = app.spirit_list[:]
                rlist.remove('Random')
                rlist.remove('None')
                value = random.choice(rlist)
            if len(app.spirit_aspects[value]) == 0:
                self.spirit6_has_aspect = False
            else:
                self.spirit6_aspects = []
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
                if rselect == True:
                    alist = self.spirit6_aspects[:]
                    #alist.remove('None')
                    aspvalue = random.choice(alist)
                    self.aspect6 = aspvalue
                    app.aspects[5] = aspvalue
                    self.aspect6 = app.aspects[5]
            self.spirit6 = value
            app.spirits[5] = value
            self.spirit6 = app.spirits[5]

    def on_select_aspect(self, player, value):
        app = App.get_running_app()
        app.aspects[player-1] = value

class MapLayoutScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'MapLayout'
        write_state()  
        maplist = []
        boards = int(app.players)
        if app.extraboard == True:
            boards = boards+1
            if boards == 7:
                boards = 6
        if boards == 1 and app.thematic == False:
            maplist.append({'text': 'Solo Standard', 'image': 'resources/maps/1player-standard.png'})
        elif boards == 1 and app.thematic == True:
            maplist.append({'text': 'Solo Thematic', 'image': 'resources/maps/1player-thematic.png'})
        elif boards == 2 and app.thematic == False:
            maplist.append({'text': '2 Player Standard', 'image': 'resources/maps/2player-standard.png'})
            maplist.append({'text': '2 Player Fragmented', 'image': 'resources/maps/2player-fragment.png'})
            maplist.append({'text': '2 Player Opposite Shores', 'image': 'resources/maps/2player-oppositeshores.png'})
        elif boards == 2 and app.thematic == True:
            maplist.append({'text': '2 Player Thematic', 'image': 'resources/maps/2player-thematic.png'})
        elif boards == 3 and app.thematic == False:
            maplist.append({'text': '3 Player Standard', 'image': 'resources/maps/3player-standard.png'})
            maplist.append({'text': '3 Player Coastline', 'image': 'resources/maps/3player-coastline.png'})
        elif boards == 3 and app.thematic == True:
            maplist.append({'text': '3 Player Thematic', 'image': 'resources/maps/3player-thematic.png'})
        elif boards == 4 and app.thematic == False:
            maplist.append({'text': '4 Player Standard', 'image': 'resources/maps/4player-standard.png'})
            maplist.append({'text': '4 Player Leaf', 'image': 'resources/maps/4player-leaf.png'})    
            maplist.append({'text': '4 Player Snake', 'image': 'resources/maps/4player-snake.png'})    
        elif boards == 4 and app.thematic == True:
            maplist.append({'text': '4 Player Thematic', 'image': 'resources/maps/4player-thematic.png'})
        elif boards == 5:
            maplist.append({'text': '5 Player Standard', 'image': 'resources/maps/5player-standard.png'})
            maplist.append({'text': '5 Player Peninsula', 'image': 'resources/maps/5player-peninsula.png'})    
            maplist.append({'text': '5 Player Snail', 'image': 'resources/maps/5player-snail.png'})   
            maplist.append({'text': '5 Player V', 'image': 'resources/maps/5player-v.png'})
        elif boards == 6:
            maplist.append({'text': '6 Player Standard', 'image': 'resources/maps/6player-standard.png'})
            maplist.append({'text': '6 Player Caldera', 'image': 'resources/maps/6player-caldera.png'})  
            maplist.append({'text': '6 Player Flower', 'image': 'resources/maps/6player-flower.png'})
            maplist.append({'text': '6 Player Star', 'image': 'resources/maps/6player-star.png'})
            maplist.append({'text': '6 Player Archipelago', 'image': 'resources/maps/6player-archipelagos.png'})
        maprv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.MAPRV
        maprv.data = maplist
        
#Board Setup Screen
#Corresponds to kivy main
class BoardSetupScreen(Screen):
    text = StringProperty('')
    ideck = ['1','1','1','2','2','2','2','3','3','3','3','3']
    def on_enter(self):                 #override of on_enter, runs when screen is constructed
        app = App.get_running_app()
        app.currentPhase = 'BoardSetup'
        write_state()
        
        fear = ''
        #invaders = 
        exsetup = ''
        ft = ''
        bt = ''
        list = []
        fdeck = [3,3,3]
        fear_per = 4
        self.ideck = ['1','1','1','2','2','2','2','3','3','3','3','3']
        for x in range(len(app.opponents)):
            start = ''
            fdeck[0] = fdeck[0] + app.fear_cards[app.opponents[x]][int(app.levels[x])][0]
            fdeck[1] = fdeck[1] + app.fear_cards[app.opponents[x]][int(app.levels[x])][1]
            fdeck[2] = fdeck[2] + app.fear_cards[app.opponents[x]][int(app.levels[x])][2]

        #loop to add all setup changes together (cumulative) from app.setup_changes up to opponent level into local start
            if app.opponents[x] == 'France':
                towns = 7
                if not 'None' in app.opponents and int(app.levels[x]) >=2:
                    towns = 8
                start += 'Return all but ' + str(towns*int(app.players)) + ' towns to the box before setup.\n'
            if app.opponents[x] == 'Scotland' and not 'None' in app.opponents:
                start  += 'If the other Adversary\'s Setup instructions would add a city to a Coastal land other than land #2, instead add the city to an adjacent Inland land.\n'
            for lvl in range(int(app.levels[x])+1):
                start += app.setup_changes[app.opponents[x]][lvl]
            if start != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': start})    
        ## Invader Deck
            if(app.opponents[x]) == 'Brandenburg-Prussia':
                self.bp_invaderdeck(app.levels[x])
            if(app.opponents[x]) == 'Scotland': 
                self.scotland_invaderdeck(app.levels[x])
            if(app.opponents[x]) == 'Russia':
                self.russia_invaderdeck(app.levels[x])
            if(app.opponents[x]) == 'Habsburg':
                self.habsburg_invaderdeck(app.levels[x])
            fear_per = fear_per + app.opp_fear_tokens[app.opponents[x]][int(app.levels[x])]
        app.fear_tokens = fear_per * int(app.players)    #calculate number of fear tokens into global fear_tokens
        if app.extraboard:
            app.fear_tokens = app.fear_tokens + int(app.players)
            
        ### Build display items
        ftotal = fdeck[0] + fdeck[1] + fdeck[2]
        fear = 'Fear Cards: ' + str(ftotal) + '(' + '/'.join(map(str, fdeck))+ ')\n'  #calculate fear cards into local fear
        if fear != '':
            list.append({'image': app.icons['Fear Cards'], 'text': fear})
        ft = 'Fear Tokens: ' + str(app.fear_tokens) + '\n'   #copy global fear_tokens into local ft
        if ft != '':
            list.append({'image': app.icons['fear tokens'], 'text': ft})
        invaders = 'Invader Deck: '
        last = self.ideck[0]
        for card in self.ideck:
            if card == last:
                invaders = invaders + card
            else:
                invaders = invaders + '-'
                invaders = invaders + card
            last = card
        list.append({'image': app.icons['Invader Cards'], 'text': invaders})
        if app.thematic:
            if app.expansion == 'None':
                exsetup = 'Follow the icons on the thematic map for all invaders, ignore the extra token icons.'
            elif app.notokens == True:
                exsetup = 'Follow the icons on the thematic map for all invaders, but no not place any extra tokens.'
            else:
                exsetup = 'Follow the icons on the thematic map for all invaders and tokens. Land #9 on the West board should have 2 Badlands tokens, not just 1.'
        else:
            exsetup = app.expansion_setup[app.expansion]     #copy app.expansion_setup into local exsetup
        if exsetup != '':
            list.append({'image': app.icons['Land'], 'text': exsetup})
        bp = int(app.players)
        if app.extraboard == True:
            bp = bp+1
        blight_tokens = (2 * bp) + 1
        bt = 'Blight Tokens: ' + str(blight_tokens)+ '\n'
        if bt != '':
            list.append({'image': app.icons['blight tokens'], 'text': bt})
        if app.extraboard == True:
            list.append({'image': 'resources/maps/1player-standard.png', 'text': 'On the extra board setup up dahan, blight, and tokens normally. Do NOT place any Invaders or Blight tokens indicated by Adversary setup on the extra board.'})
            if int(app.players) == 1:
                list.append({'image': 'resources/maps/1player-standard.png', 'text': 'Do not place any adversary tokens on the extra board'})
            if int(app.players) == 2:
                list.append({'image': 'resources/maps/1player-standard.png', 'text': 'Do not place any adversary tokens on the extra board'})
            if int(app.players) == 3:
                list.append({'image': 'resources/maps/1player-standard.png', 'text': 'Perform the only the coastal adversary setup on the extra board.'})
            if int(app.players) == 4:
                list.append({'image': 'resources/maps/1player-standard.png', 'text': 'Perform the only the inland adversary setup on the extra board.'})
            if int(app.players) == 5:
                list.append({'image': 'resources/maps/1player-standard.png', 'text': 'Perform the normal adversary setup on the extra board.'})
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
        
    def bp_invaderdeck(self, lvl):
        ## When making the Invader Deck, put 1 of the Stage III cards between Stage I and Stage II. (New Deck Order:111-3-2222-3333)
        if int(lvl) >= 2:
            index = self.ideck.index('2')
            self.ideck.insert(index, '3')
            self.ideck.reverse()
            index = self.ideck.index('3')
            self.ideck.pop(index)
            self.ideck.reverse()
        ##When making the Invader Deck, remove an additional Stage I card. (New Deck Order:11-3-2222-3333)
        if('1' in self.ideck):
            if int(lvl) >= 3:
                index = self.ideck.index('1')
                self.ideck.pop(index)
        ##When making the Invader Deck, remove an additional Stage II card. (New Deck Order:11-3-222-3333)
        if int(lvl) >= 4:
            index = self.ideck.index('2')
            self.ideck.pop(index)
        ##When making the Invader Deck, remove an additional Stage I card. (New Deck Order:1-3-222-3333)
        if('1' in self.ideck):
            if int(lvl) >= 5:
                index = self.ideck.index('1')
                self.ideck.pop(index)
        ##When making the Invader Deck, remove all Stage I cards. (New Deck Order:3-222-3333) 
        if('1' in self.ideck):
            if int(lvl) >= 6:
                index = self.ideck.index('1')
                self.ideck.pop(index)
    def habsburg_invaderdeck(self, lvl):
        ## When making the Invader Deck, Remove 1 additional Stage I Card. (New deck order: 11-2222-33333) 
        if int(lvl) >= 3:
            if '1' in self.ideck:
                index = self.ideck.index('1')
                self.ideck.pop(index)
    def russia_invaderdeck(self, lvl):
        ##When making the Invader Deck, put 1 Stage III Card after each Stage II Card. (New Deck Order: 111-2-3-2-3-2-3-2-33) 
        if int(lvl) >= 4:
            rideck = self.ideck[:]
            rideck.reverse()
            count = 0
            newdeck = []
            for x in  range(len(self.ideck)):
                if rideck[0] == '3' and self.ideck[x] == '2':
                    newdeck.append(self.ideck[x])
                    newdeck.append('3')
                    rideck.pop(0)
                    count = count +1
                elif rideck[0] == '3' and self.ideck[x] == 'C':
                    newdeck.append(self.ideck[x])
                    newdeck.append('3')
                    rideck.pop(0)
                    count = count +1
                else:
                    newdeck.append(self.ideck[x])
            for x in range(count):
                newdeck.pop(-1)
            self.ideck = newdeck
    def scotland_invaderdeck(self, lvl):
        ##Place "Coastal Lands" as the 3rd Stage II card, and move the two Stage II Cards above it up by one. (New Deck Order: 11-22-1-C2-33333, where C is the Stage II Coastal Lands Card.) 
        if int(lvl) >= 2:
            self.ideck.reverse()
            index = self.ideck.index('2')
            index = self.ideck.index('2', index+1)
            self.ideck.pop(index)
            self.ideck.insert(index, 'C')
            index = self.ideck.index('2')
            index = self.ideck.index('2', index+1)
            self.ideck.pop(index)
            self.ideck.insert(index+2, '2')
            index = self.ideck.index('2')
            index = self.ideck.index('2', index+1)
            self.ideck.pop(index)
            self.ideck.insert(index+2, '2')
            self.ideck.reverse()
        ##During Setup, replace the bottom Stage I Card with the bottom Stage III Card. (New Deck Order: 11-22-3-C2-3333)) 
        if int(lvl) >= 4:
            self.ideck.reverse()
            index = self.ideck.index('3')
            self.ideck.pop(index)
            if '1' in self.ideck:
                index = self.ideck.index('1')
                self.ideck.pop(index)
            self.ideck.insert(index, '3')
            self.ideck.reverse()
        
class SpiritSetupScreen(Screen):
    spirits_text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'SpiritSetup'
        self.spirits_text = ''
        list = []
        for spirit in app.spirits:
            if spirit != 'None':
                list.append({'image': app.icons[spirit], 'text': spirit + ':\n' + app.spirit_setup[spirit]})
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = list
        
class FirstExploreScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        app.currentPhase = 'FirstExplore'
        write_state()
        description = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})
        if app.displayopts[app.currentPhase]['rules']:
            for x in range(len(app.opponents)):
                rules = ''
                for lvl in range(int(app.levels[x])+1):
                    rules += app.firstexplorescreen_rules[app.opponents[x]][lvl]
                if rules != '':
                    list.append({'image': app.icons[app.opponents[x]], 'text': rules})
        #self.text = '\n'.join([description + rules])
        if app.extraboard == True:
            if int(app.players) == 1:
                list.append({'image': 'resources/maps/1player-standard.png', 'text': 'Do not perform this explore on the extra board'})
            if int(app.players) == 2:
                list.append({'image': 'resources/maps/1player-standard.png', 'text': 'Do not perform this explore on the extra board'})
            if int(app.players) == 3:
                list.append({'image': 'resources/maps/1player-standard.png', 'text': 'Perform this explore on the extra board.'})
            if int(app.players) == 4:
                list.append({'image': 'resources/maps/1player-standard.png', 'text': 'Perform this explore on the extra board.'})
            if int(app.players) == 5:
                list.append({'image': 'resources/maps/1player-standard.png', 'text': 'Perform this explore on the extra board.'})
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
        if app.currentPhase != 'Energy' and app.fromLoad != True:
            app.turn = app.turn + 1
        app.currentPhase = 'Growth'
        write_state()
        self.text = ''
        description = ''
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
                    spirits_text = 'Spirits with more than one Growth action can use energy gained from one action to pay for another.  The same growth option cannot be chosen twice.\n'
        if spirits_text != '':
            list.append({'image': app.icons['spirits text'], 'text': spirits_text})

        
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})        
        for x in range(len(app.opponents)):
            opprules = ''
            allrules = ''
            loss = ''
            if app.displayopts[app.currentPhase]['opponent']:
                for lvl in range(int(app.levels[x])+1):
                    opprules += app.growthscreen_rules[app.opponents[x]][lvl]
            if opprules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': opprules})
            if app.displayopts[app.currentPhase]['all']:
                for lvl in range(int(app.levels[x])+1):
                    allrules += app.allscreen_rules[app.opponents[x]][lvl]
            if allrules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': allrules})
            if app.displayopts['All']['loss']:
                loss = app.loss_rules[app.opponents[x]]
            if loss != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': loss})
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
        loss = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})
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
        loss = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})

        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        for x in range(len(app.opponents)):
            opprules = ''
            allrules = ''
            loss = ''
            if app.displayopts[app.currentPhase]['opponent']:
                for lvl in range(int(app.levels[x])+1):
                    opprules += app.powercardscreen_rules[app.opponents[x]][lvl]
            if opprules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': opprules})
            if app.displayopts[app.currentPhase]['all']:
                for lvl in range(int(app.levels[x])+1):
                    allrules += app.allscreen_rules[app.opponents[x]][lvl]
            if allrules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': allrules})
            if app.displayopts['All']['loss']:
                loss = app.loss_rules[app.opponents[x]]
            if loss != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': loss})
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
        loss = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        for x in range(len(app.opponents)):
            opprules = ''
            allrules = ''
            loss = ''
            if app.displayopts[app.currentPhase]['opponent']:
                for lvl in range(int(app.levels[x])+1):
                    opprules += app.fastpowerscreen_rules[app.opponents[x]][lvl]
            if opprules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': opprules})
            if app.displayopts[app.currentPhase]['all']:
                for lvl in range(int(app.levels[x])+1):
                    allrules += app.allscreen_rules[app.opponents[x]][lvl]
            if allrules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': allrules})
            if app.displayopts['All']['loss']:
                loss = app.loss_rules[app.opponents[x]]
            if loss != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': loss})
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
        loss = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})            
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        for x in range(len(app.opponents)):
            opprules = ''
            allrules = ''
            loss = ''
            if app.displayopts[app.currentPhase]['opponent']:
                for lvl in range(int(app.levels[x])+1):
                    opprules += app.blightedislandscreen_rules[app.opponents[x]][lvl]
            if opprules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': opprules})
            if app.displayopts[app.currentPhase]['all']:
                for lvl in range(int(app.levels[x])+1):
                    allrules += app.allscreen_rules[app.opponents[x]][lvl]
            if allrules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': allrules})
            if app.displayopts['All']['loss']:
                loss = app.loss_rules[app.opponents[x]]
            if loss != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': loss})
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
        loss = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description}) 
        if app.displayopts[app.currentPhase]['discard']:
            if app.turn == 1:
                discard += 'Turn over the first event card, but discard it with no action.\n'
        if discard != '':
            list.append({'image': app.icons['discard'], 'text': discard})
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        for x in range(len(app.opponents)):
            opprules = ''
            allrules = ''
            loss = ''
            if app.displayopts[app.currentPhase]['opponent']:
                for lvl in range(int(app.levels[x])+1):
                    opprules += app.eventscreen_rules[app.opponents[x]][lvl]
            if opprules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': opprules})
            if app.displayopts[app.currentPhase]['all']:
                for lvl in range(int(app.levels[x])+1):
                    allrules += app.allscreen_rules[app.opponents[x]][lvl]
            if allrules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': allrules})
            if app.displayopts['All']['loss']:
                loss = app.loss_rules[app.opponents[x]]
            if loss != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': loss})
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
        loss = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description}) 
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        for x in range(len(app.opponents)):
            opprules = ''
            allrules = ''
            loss = ''
            if app.displayopts[app.currentPhase]['opponent']:
                for lvl in range(int(app.levels[x])+1):
                    opprules += app.fearscreen_rules[app.opponents[x]][lvl]
            if opprules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': opprules})
            if app.displayopts[app.currentPhase]['all']:
                for lvl in range(int(app.levels[x])+1):
                    allrules += app.allscreen_rules[app.opponents[x]][lvl]
            if allrules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': allrules})
            if app.displayopts['All']['loss']:
                loss = app.loss_rules[app.opponents[x]]
            if loss != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': loss})
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
        disease = ""
        loss = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})            
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        if app.displayopts[app.currentPhase]['disease']:
            if app.expansion != 'None':
                disease = 'If present, Disease tokens prevent this build. Remove the token.\n'
        if disease != '':
            list.append({'image': app.icons['disease'], 'text': disease})
        for x in range(len(app.opponents)):
            opprules = ''
            allrules = ''
            loss = ''
            if app.displayopts[app.currentPhase]['opponent']:
                for lvl in range(int(app.levels[x])+1):
                    opprules += app.highimmigrationscreen_rules[app.opponents[x]][lvl]
            if opprules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': opprules})
            if app.displayopts[app.currentPhase]['all']:
                for lvl in range(int(app.levels[x])+1):
                    allrules += app.allscreen_rules[app.opponents[x]][lvl]
            if allrules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': allrules})
            if app.displayopts['All']['loss']:
                loss = app.loss_rules[app.opponents[x]]
            if loss != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': loss})        
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
        loss = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})  
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        if app.displayopts[app.currentPhase]['strife']:
            if app.expansion != 'None':
                strife = 'If present, Strife Tokens block specific invaders from doing damage. Remove the token.\n'
        if strife != '':
            list.append({'image': app.icons['strife'], 'text': strife})

        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        for x in range(len(app.opponents)):
            opprules = ''
            allrules = ''
            loss = ''
            if app.displayopts[app.currentPhase]['opponent']:
                if app.opponents[x] == 'Russia' and int(app.levels[x]) == 6  and app.turn > 1:
                    opprules += "After the ravage step, on each board where it added no blight: in the land with the most explorers (min 1) add one explorer and one town.\n"
                for lvl in range(int(app.levels[x])+1):
                    opprules += app.ravagescreen_rules[app.opponents[x]][lvl]
            if opprules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': opprules})
            if app.displayopts[app.currentPhase]['all']:
                for lvl in range(int(app.levels[x])+1):
                    allrules += app.allscreen_rules[app.opponents[x]][lvl]
            if allrules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': allrules})
            if app.displayopts['All']['loss']:
                loss = app.loss_rules[app.opponents[x]]
            if loss != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': loss})
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
        loss = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description}) 
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        if app.displayopts[app.currentPhase]['disease']:
            if app.expansion != 'None':
                disease = 'If present, Disease tokens prevent this build. Remove the token.\n'
        if disease != '':
            list.append({'image': app.icons['disease'], 'text': disease})
        for x in range(len(app.opponents)):
            opprules = ''
            allrules = ''
            loss = ''
            if app.displayopts[app.currentPhase]['opponent']:
                for lvl in range(int(app.levels[x])+1):
                    opprules += app.buildscreen_rules[app.opponents[x]][lvl]
            if opprules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': opprules})
            if app.displayopts[app.currentPhase]['all']:
                for lvl in range(int(app.levels[x])+1):
                    allrules += app.allscreen_rules[app.opponents[x]][lvl]
            if allrules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': allrules})
            if app.displayopts['All']['loss']:
                loss = app.loss_rules[app.opponents[x]]
            if loss != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': loss})
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
        loss = ''
        self.list = []

        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            self.list.append({'image': app.icons[app.currentPhase], 'text': description}) 
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                self.list.append({'image': app.icons['badlands'], 'text': badlands})
        if app.displayopts[app.currentPhase]['wilds']:
            if app.expansion != 'None':
                wilds = 'If a wilds token is present, skip that exploration and discard one wilds token.\n'
        if wilds != '':
            self.list.append({'image': app.icons['wilds'], 'text': wilds})
        self.on_stage_toggle()
        for x in range(len(app.opponents)):
            opprules = ''
            allrules = ''
            loss = ''

            if app.displayopts[app.currentPhase]['opponent']:
                for lvl in range(int(app.levels[x])+1):
                    opprules += app.explorescreen_rules[app.opponents[x]][lvl]
            if opprules != '':
                self.list.append({'image': app.icons[app.opponents[x]], 'text': opprules})
            if app.displayopts[app.currentPhase]['all']:
                for lvl in range(int(app.levels[x])+1):
                    allrules += app.allscreen_rules[app.opponents[x]][lvl]
            if allrules != '':
                self.list.append({'image': app.icons[app.opponents[x]], 'text': allrules})
            if app.displayopts['All']['loss']:
                loss = app.loss_rules[app.opponents[x]]
            if loss != '':
                self.list.append({'image': app.icons[app.opponents[x]], 'text': loss})       
        rv = App.get_running_app().root.get_screen('Phase').ids.PhaseManager.get_screen(app.currentPhase).ids.RV
        rv.data = self.list + self.s2list
    def on_stage_toggle(self):
        app = App.get_running_app()
        if app.flagicon2 == True:
            self.s2list = [{'image': app.icons['stage2flag'], 'text': 'If the invader card has an escalation icon:\n' + app.stage2_flag[app.opponents[0]]}]
        elif app.flagicon3 == True:
            self.s2list = [{'image': app.icons['stage2flag'], 'text': 'Escalation effects apply to all Invader cards: (If the escalation is specific to a terrain, choose one of the terrains randomly.)\n' + app.stage2_flag[app.opponents[1]]}]
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
        loss = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        for x in range(len(app.opponents)):
            opprules = ''
            allrules = ''
            loss = ''
            if app.displayopts[app.currentPhase]['opponent']:
                for lvl in range(int(app.levels[x])+1):
                    if not (app.opponents[x] == 'England' and lvl == 3 and int(app.levels[x]) >= 4):
                        opprules += app.advancecardsscreen_rules[app.opponents[x]][lvl]
            if opprules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': opprules})
            if app.displayopts[app.currentPhase]['all']:
                for lvl in range(int(app.levels[x])+1):
                    allrules += app.allscreen_rules[app.opponents[x]][lvl]
            if allrules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': allrules})
            if app.displayopts['All']['loss']:
                loss = app.loss_rules[app.opponents[x]]
            if loss != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': loss})        
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
        loss = ''
        list = []
        if app.displayopts['All']['phase']:
            description = app.screenDescriptions[app.currentPhase]
        if description != '':
            list.append({'image': app.icons[app.currentPhase], 'text': description})
        if app.expansion == "BC and JE" or app.expansion == "Jagged Earth":
            if app.displayopts['All']['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
                list.append({'image': app.icons['badlands'], 'text': badlands})
        for x in range(len(app.opponents)):
            opprules = ''
            allrules = ''
            loss = ''
            if app.displayopts[app.currentPhase]['opponent']:
                for lvl in range(int(app.levels[x])+1):
                    opprules += app.slowpowerscreen_rules[app.opponents[x]][lvl]
            if opprules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': opprules})
            if app.displayopts[app.currentPhase]['all']:
                for lvl in range(int(app.levels[x])+1):
                    allrules += app.allscreen_rules[app.opponents[x]][lvl]
            if allrules != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': allrules})
            if app.displayopts['All']['loss']:
                loss = app.loss_rules[app.opponents[x]]
            if loss != '':
                list.append({'image': app.icons[app.opponents[x]], 'text': loss})        
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
    store.put('opponents', value=app.opponents)
    store.put('thematic', value=app.thematic)
    store.put('extraboard', value=app.extraboard)
    store.put('spirits', value=app.spirits)
    store.put('aspects', value=app.aspects)
    store.put('scenario', value=app.scenario)
    store.put('levels', value=app.levels)
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
        self.data = []


class MAPRV(RecycleView):
    def __init__(self, **kwargs):
        super(MAPRV, self).__init__(**kwargs)
        self.data = []#[{'text': '2 Player Standard', 'image': 'resources/maps/2player-standard.png'}] #app.maplist
  
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
    flagicon2 = BooleanProperty(False)
    flagicon3 = BooleanProperty(False)
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
    stage2_flag = data.stage2_flag
    loss_rules = data.loss_rules
    allscreen_rules = data.allscreen_rules
    opponentmod_rules = data.opponentmod_rules
    opp_fear_tokens = data.opp_fear_tokens
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
    opponent_difficulty = data.oppoenent_difficulty
    scenario_difficulty = data.scenario_difficulty
    ##
    #data = ListProperty([])

    ## Global variables
    branchandclaw = False
    jaggedearth = False
    promopack1 = False
    promopack2 = False
    expansion = 'None'          #global variable for expansion
    opponents = ['None','None']
    thematic = False
    notokens = False
    extraboard = False
    spirits = ['None', 'None', 'None', 'None', 'None', 'None']
    aspects = ['None', 'None', 'None', 'None', 'None', 'None']
    scenario = 'None'
    levels = ['0','0']
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
    difficulty = '0'
    fontsize = NumericProperty(15)
    imagewidth = NumericProperty(0.07)
    ##
    blightscreeninactive = False
    fromLoad = False
    def build(self):
        self.fdeck = [3,3,3]
        self.maplist = []
        if int(self.config.get('timeroptions', 'usetimer')) == 0:
            self.use_timer = False
        else:
            self.use_timer = True
        self.timer_seconds = int(self.config.get('timeroptions', 'timerseconds'))
        self.fontsize = int(self.config.get('Display', 'fontsize'))
        self.imagewdith = float(self.config.get('Display', 'imagewidth'))/100
        self.displayopts['All'] = {}
        for item in ['phase', 'badlands', 'loss']:
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
        for item in ['opponent', 'all', 'disease']:
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
        config.setdefaults('Display', {
                                'fontsize': 15,
                                'imagewidth': 7.5
                            })
        config.setdefaults('All', {
                                'phase': 1,
                                'badlands': 1
                            })
        config.setdefaults('All', {
                                'phase': 1,
                                'loss': 1
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
                                'disease': 1,
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
        elif section == 'Display': 
            self.imagewidth = float(self.config.get('Display', 'imagewidth'))/100
            self.fontsize = int(self.config.get('Display', 'fontsize'))
        else:
            self.displayopts[section][key]=int(value)
            
    def on_stage_toggle(self, value):
        if value == 'II':
            if self.opponents[0] != 'None':
                self.flagicon2 = True
                self.flagicon3 = False
        elif value == 'III':
            if self.opponents[1] != 'None':
                self.flagicon2 = False
                self.flagicon3 = True
            else:
                self.flagicon2 = False
                self.flagicon3 = False
        else:
            self.flagicon2 = False
            self.flagicon3 = False
        if self.currentPhase == 'Explore':
            self.root.get_screen('Phase').ids.PhaseManager.get_screen(self.currentPhase).on_stage_toggle()
        return self
    def no_blight_screen(self, value):
        if value == True:
            self.blightscreeninactive = True
        else:
            self.blightscreeninactive = False

            


        
MainApp().run()


