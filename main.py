from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.config import Config 
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.storage.jsonstore import JsonStore
from settings_json import settings_json
import datetime
Config.set('graphics', 'resizable', True)
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
#current ='Main'
currentPhase = 'FirstExplore'
use_timer = True
timer_seconds = 180
displayopts = {}

base_opp = ['None', 'Brandenburg-Prussia', 'England', 'Sweden']
bc_opp = ['France']
je_opp = ['Russia', "Habsburg"]
pp2_opp = ['Scotland']
opponent_list = base_opp

base_spirits = ['Lightnings Swift Strike','River Surges in Sunlight', 'Vital Strength of the Earth', 'Shadows Flicker Like Flame', 'Thunderspeaker', 'A Spread of Rampant Green', 'Oceans Hungry Grasp', 'Bringer of Dreams and Nightmares']
bc_spirits = ['Sharp Fangs Behind the Leaves', 'Keeper of the Forbidden Wilds']
je_spirits = ['Stones Unyielding Defiance', 'Shifting Memory of Ages', 'Grinning Trickster Stirs up Trouble', 'Lure of the Deep Wilderness', 'Many minds Move as One', 'Volcano Looming High', 'Shroud of Silent Mist', 'Vengeance as a Burning Plague', 'Starlight Seeks Its Form', 'Fractured Days Split the Sky']
pp1_spirits = ['Heart of Wildfire', 'Serpent Slumbering Beneath the Island']
pp2_spirits = ['Downpour Drenches the World', 'Finder of Paths Unseen']
spirit_list = base_spirits
spirit_aspects = {  'Lightnings Swift Strike': ['pp2:Immense', 'je:Pandemonium', 'je:Wind'],
                    'River Surges in Sunlight': ['je:Sunshine', 'pp2:Travel'],
                    'Vital Strength of the Earth': ['pp2:Might', 'je:Resilience'],
                    'Shadows Flicker Like Flame': ['pp2:Amorphous', 'pp2:Foreboding', 'je:Madness', 'je:Reach'],
                    'Thunderspeaker': [],
                    'A Spread of Rampant Green': [],
                    'Oceans Hungry Grasp': [],
                    'Bringer of Dreams and Nightmares': [],
                    'Sharp Fangs Behind the Leaves': [],
                    'Keeper of the Forbidden Wilds': [],
                    'Stones Unyielding Defiance': [],
                    'Shifting Memory of Ages': [],
                    'Grinning Trickster Stirs up Trouble': [],
                    'Lure of the Deep Wilderness': [],
                    'Many minds Move as One': [],
                    'Volcano Looming High': [],
                    'Shroud of Silent Mist': [],
                    'Vengeance as a Burning Plague': [],
                    'Starlight Seeks Its Form': [],
                    'Fractured Days Split the Sky': [],
                    'Heart of Wildfire': [],
                    'Serpent Slumbering Beneath the Island': [],
                    'Downpour Drenches the World': [],
                    'Finder of Paths Unseen': [],
                    'None': []}

spirit_setup = {    'Lightnings Swift Strike': 'Put 2 presence on your starting board in the highest-numbered Sands.\n',
                    'River Surges in Sunlight': 'Put 1 presence on your starting board in the highest-numbered Wetlands.\n',
                    'Vital Strength of the Earth': 'Put 3 presence on your starting board: 2 in the highest-numbered Mountain, 1 in the highest-numbered Jungle.\n',
                    'Shadows Flicker Like Flame': 'Put 3 presence on your starting board: 2 in the highest numbered Jungle, and one in land #5.\n',
                    'Thunderspeaker': 'Put 2 presence on your starting board: 1 in each of the 2 lands with the most Dahan.\n',
                    'A Spread of Rampant Green': 'Put 2 presence on your starting board: 1 in the highest-numbered Wetland, and 1 in the Jungle without any Dahan. (If there is more than one such jungle, you may choose)\n',
                    'Oceans Hungry Grasp': 'Put 2 presence onto your starting board: 1 in the Ocean, and 1 in a coastal land of your choice.\n',
                    'Bringer of Dreams and Nightmares': 'Put 2 presence on your starting board in the highest-numbered Sands.\n',
                    'Sharp Fangs Behind the Leaves': 'Put 1 presence and 1 beast token on your starting board in the highest-numbered Jungle. Put 1 presence in a land of your choice with a beast token anywhere on the island.\n',
                    'Keeper of the Forbidden Wilds': 'Put 1 presence and 1 wilds token on your starting board in the highest-numbered Jungle.',
                    'Stones Unyielding Defiance': 'Put 2 presence on your starting board: 1 in the lowest-numbered Mountain without Dahan; 1 in an adjacent land that has blight. (if possible) or Sands (if not)\n',
                    'Shifting Memory of Ages': 'Put 2 presence on your starting board in the highest-numbered land that is Sands or Mountain. Prepare 1 moon, 1 Air, and 1 Earth marker (put them by your Special Rules)\n',
                    'Grinning Trickster Stirs up Trouble': 'Put 2 presence on your starting board: 1 in the highest-numbered land with Dahan, and 1 in land #4.\n',
                    'Lure of the Deep Wilderness': 'Put 3 presence on your starting board: 2 in land #8, and 1 in land #7. Add 1 beast token to land #8.\n',
                    'Many minds Move as One': 'Put 1 presence and 1 beast token on your starting board, in a land with a beast token. Note that you have 5 unique power cards.\n',
                    'Volcano Looming High': 'Put 1 presence on your starting board in a mountain of your choice. Push all Dahan from that land.\n',
                    'Shroud of Silent Mist': 'Put 2 presence on your starting board: 1 in the highest-numbered Wetland and 1 in the highest-numbered Mountain.\n',
                    'Vengeance as a Burning Plague': '1 of your presence starts the game already Destroyed. Put 2 presence on your starting board, 1 in a land with blight, 1 in a Wetland without Dahan.\n',
                    'Starlight Seeks Its Form': 'Put 1 presence on your starting board, in a land with blight.\n',
                    'Fractured Days Split the Sky': 'Put 3 presence on your starting board: 1 in the lowest-numbered land with 1 Dahan, and 2 in the highest-numbered land without Dahan. Deal 4 Minor and Major Powers face-up as your initial Days that Never Were cards; in a 1 or 2 player game, instead deal 6 of each. In a 1-board game, gain 1 Time.\n',
                    'Heart of Wildfire': 'Put 3 presence and 2 blight on your starting board in the highest-numbered Sands. (Blight comes from the box, not the blight card)\n',
                    'Serpent Slumbering Beneath the Island': 'Put one presence on your starting board in land #5.\n',
                    'Downpour Drenches the World': 'Put 1 presence on your starting baord in the lowest-numbered Wetlands.\n',
                    'Finder of Paths Unseen': 'Put 1 presence on your starting board in land #d. Put 1 presence on any board in land #1. Not that you have 6 unique power cards.\n',
                    'None': ''}                    

spirit_growth_count = { 'Lightnings Swift Strike': 1,
                        'River Surges in Sunlight': 1,
                        'Vital Strength of the Earth': 1,
                        'Shadows Flicker Like Flame': 1,
                        'Thunderspeaker': 1,
                        'A Spread of Rampant Green': 1,
                        'Oceans Hungry Grasp': 1,
                        'Bringer of Dreams and Nightmares': 1,
                        'Sharp Fangs Behind the Leaves': 2,
                        'Keeper of the Forbidden Wilds': 2,
                        'Stones Unyielding Defiance': 1,
                        'Shifting Memory of Ages': 1,
                        'Grinning Trickster Stirs up Trouble': 2,
                        'Lure of the Deep Wilderness': 2,
                        'Many minds Move as One': 1,
                        'Volcano Looming High': 1,
                        'Shroud of Silent Mist': 1,
                        'Vengeance as a Burning Plague': 1,
                        'Starlight Seeks Its Form': 3,
                        'Fractured Days Split the Sky': 1,
                        'Heart of Wildfire': 1,
                        'Serpent Slumbering Beneath the Island': 2,
                        'Downpour Drenches the World': 1,
                        'Finder of Paths Unseen': 1,
                        'None': 1}

base_scenarios = ['Blitz', 'Guard the Isles Heart', 'None', 'Rituals of Terror', 'Dahan Insurrection']
bc_scenarios = ['Second Wave', 'Powers Long Forgotten', 'Ward the Shores', 'Rituals of the Destroying Flame']
je_scenarios = ['Elemental Invocation', 'Despicable Theft', 'The Great River']
pp1_scenarios = []
pp2_scenarios = ['A Diversity of Spirits', 'Varied Terrains']
scenarios_list = base_scenarios

#Fear Card counts, taken from Opponent cards
#Dictionary accessed with fear_cards[opponent][level]
fear_cards = {'None':                ['9(3/3/3)',
                                      '9(3/3/3)',
                                      '9(3/3/3)',
                                      '9(3/3/3)',
                                      '9(3/3/3)',
                                      '9(3/3/3)'],
              'Brandenburg-Prussia': ['9(3/3/3)', 
                                      '9(3/3/3)',
                                      '10(3/4/3)',
                                      '11(4/4/3)',
                                      '11(4/4/3)',
                                      '12(4/4/4)'],
              'England':            ['10(3/4/3)',
                                      '11(4/4/3)',
                                      '13(4/5/4)',
                                      '14(3/4/5)',
                                      '14(4/5/5)',
                                      '13(4/5/4)'],
              'France':              ['9(3/3/3)',
                                      '10(3/4/3)',
                                      '11(4/4/3)',
                                      '12(4/4/4)',
                                      '13(4/5/4)',
                                      '14(4/5/5)'],
              'Sweden':              ['9(3/3/3)',
                                      '10(3/4/3)',
                                      '10(3/4/3)',
                                      '11(3/4/4)',
                                      '12(4/4/4)',
                                      '13(4/4/5)'],
              'Scotland':            ['10(3/4/3)',
                                      '11(4/4/3)',
                                      '13(4/5/4)',
                                      '14(5/5/4)',
                                      '15(5/6/4)',
                                      '16(6/6/4)'],
               'Russia':              ['10(3/3/4)',
                                       '11(4/3/4)',
                                       '11(4/4/3)',
                                       '12(4/4/4)',
                                       '13(4/5/4)',
                                       '13(4/5/4)'],
               'Habsburg':            ['10(3/4/3)',
                                       '11(4/5/2)',
                                       '12(4/5/3)',
                                       '13(4/5/3)',
                                       '13(4/6/3)',
                                       '14(5/6/3)']                                     
              }

#Dictionary of changes made during game setup based on opponent
#Accessed with setup_changes[opponent][level]
setup_changes = { 'None':                ['',
                                          '',
                                          '',
                                          '',
                                          '',
                                          ''],
                  'Brandenburg-Prussia': ['Add one town land #3 on each board\n',
                                          'Put one stage 3 card between Stage I and Stage II\n',
                                          'Remove an additional Stage I card.\n',
                                          'Remove an additional Stage II card.\n',
                                          'Remove an additional Stage I Card.\n',
                                          'Remove all Stage I Cards.\n'],
                  'England':             ['',
                                          'On each board add one city to land #1 and one town to land #2\n',
                                          'Put the High Immigration tile on the invader board to the left of ravage\n',
                                          '',
                                          '',
                                          'Add an additional fear to the pool per player\n'],
                  'France':              ['Return all but 7 towns per player to the box before setup.\n',
                                          'Put the Slave Rebellion Event under the top 3 cards of the event deck.\n',
                                          'On each board add one town to the highest numbered land without a town.\nAdd one town to land 1.\n',
                                          '',
                                          '',
                                          ''],
                  'Sweden':              ['',
                                          'On each board add one city to land #4.\nOn boards where land #4 starts with blight, put that blight in land #5 instead.\n',
                                          '',
                                          'After adding all invaders, discard the top card of the invader deck. On each board add one town to the land of that terrain with the fewest invaders.\n',
                                          '',
                                          'On each board add one town and one blight to land #8.\n(Take the blight from the box, not the blight card)\n'],
                  'Scotland':            ['',
                                          'Add one city to land #2.\nPlace "Coastal Lands" as the 3rd stage II invader card, and move the two stage II cards above it up by one.\n',
                                          '',
                                          'Replace the bottom stage I Card with the bottom stage III card\n',
                                          '',
                                          ''],
                  'Russia':               ['On each board, add one beast and one explorer to the highest-numbered land without towns/cities.\n',
                                           '',
                                           '',
                                           '',
                                           'Put an unused Stage II Invader card under the top 3 fear cards, and an unused Stage III Card under the top 7 fear cards. When revealed, immediately place it in the build space (face up)\n',
                                           ''],
                  'Habsburg':             ['',
                                           'On each board, add one town to land #2 and one town to the highest-numbered land without setup symbols.\n',
                                           '',
                                           '',
                                           'Put the Habsburg Reminder Card under the top 5 invader cards.\n',
                                           '']                                        
                  }

#Global variable for game setup changes based on expansion
#Simple dictionary, access via expansion_setup[expansion] = value
expansion_setup = { 'None': '',
                    'Branch and Claw': 'On each board:\nPut one Beast Token in the lowest land with no printed icons.\nPut one Disease Token in land #2',
                    'Jagged Earth': 'On each board:\nPut one Beast Token in the lowest land with no printed icons.\nPut one Disease Token in land #2',
                    'BC and JE': ''
                    }

#Global variable for invader deck
#dictionary accessed via invader_deck[opponent][level]
invader_deck = { 'None':                ['111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333'],
                 'Brandenburg-Prussia': ['111-2222-33333',
                                         '111-3-2222-3333',
                                         '11-3-2222-3333',
                                         '11-3-222-3333',
                                         '1-3-222-3333',
                                         '3-222-3333'],
                  'England':            ['111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333'],
                  'France':             ['111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333'],
                  'Sweden':             ['111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333'],
                  'Scotland':           ['111-2222-33333',
                                         '11-22-1-C2-33333 (C2 is Coastal Lands Stage II Card)',
                                         '11-22-1-C2-33333 (C2 is Coastal Lands Stage II Card)',
                                         '11-22-3-C2-3333 (C2 is Coastal Lands Stage II Card)',
                                         '11-22-3-C2-3333 (C2 is Coastal Lands Stage II Card)',
                                         '11-22-3-C2-3333 (C2 is Coastal Lands Stage II Card)'],
                  'Russia':             ['111-2222-33333',
                                         '111-2222-33333',
                                         '111-2222-33333',
                                         '111-2-3-2-3-2-3-2-33',
                                         '111-2-3-2-3-2-3-2-33',
                                         '111-2-3-2-3-2-3-2-33'],
                  'Habsburg':           ['111-2222-33333',
                                         '111-2222-33333',
                                         '11-2222-33333',
                                         '11-2222-33333',
                                         '11-2222-33333',
                                         '11-2222-33333']                          
                }

#global variable for the stage 2 invader card flag impact
#dictionary accessed via stage2_flag[opponent] = value
#scotland must be updated during MainApp build due to change to player count
stage2_flag = { 'None': '',
                'Brandenburg-Prussia': 'If the invader card has a flag:\nOn each board with towns or cities: Add one town to a land without a town.\n',
                'England': 'If the invader card has a flag:\nOn each board with towns or cities: Build in the land with the most towns/cities.\n',
                'France': 'If the invader card has a flag:\nAfter exploring, on each board, pick a land of the shown terrain. If it has towns/cities, add one blight. Otherwise add one town.',
                'Sweden': 'If the invader card has a flag:\nAfter invaders explore into each land this phase, if that land has at least as many invaders as dahan, replace one dahan with one town.\n',
                'Scotland': 'If the invader card has a flag:\nOn the single board with the most coastal towns/cities add one town to the '+ str(players) +' lands with the fewest towns.\n',
                'Russia': 'If the invader card has a flag: On each board:\nAdd 2 explorers (total) among lands with beasts. If you can\'t, instead add 2 explorers among lands with beasts on a different board.\n',
                'Habsburg': 'If the invader card has a flag:\nAfter exploring: On each board with 4 or fewer blight, add one town to a land without towns/blight. On each board with 2 or fewer blight, do so again.\n'
                }

#allscreen rules has 7 entries instead of the usual 6.  The first entry is for any additional loss condition.
allscreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            'Loss condition: If 7 or more towns/cities are ever in a single land, the invaders win.\n',
                            '',
                            '',
                            '',
                            '',
                            'Towns and Cities have +1 health\n',
                            ''],
    'France': [
                            'Loss condition: Invaders win if you ever cannot place a town.\n',
                            '',
                            '',
                            '',
                            '',
                            'When you remove blight from the board, put it on the adversary card instead of on the blight card. As soon as you have 3 blight per player on the card, move it all back to the blight card.\n',
                            ''],
    'Sweden': [             
                            '',
                            '',
                            '',
                            'Towns deal 3 damage. Cities deal 5 damage.\n',
                            '',
                            '',
                            ''],
    'Scotland': [            
                            'Loss condition: If the number of coastal lands with cities is ever greater than (2x # of boards) the invaders win.\n',
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            'Loss condition: Put beasts destroyed by adversary rules on the adversary panel. If there are ever more beasts on that panel than the island, the invaders win.\n',
                            'Explorers do +1 damage.\n',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            'Loss condition: Track how many blight come off the blight cards during ravages that do 8+ damage to the land. If that number ever exceeds players, the invaders win.\n',
                            '',
                            '',
                            '',
                            'Towns in lands without blight are Durable: they have +2 health, and \'Destroy town\' effects instead deal 2 damage (to towns only) per town they could destroy. (\"Destroy all towns\" works normally.)\n',
                            '',
                            '']
    }

# These are the opponent health/damage values
# order is:
# explorer health, town health, city health, explorer damage, town damage, city damage    
opponentmod_rules = {
    'None':                 [
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123'],
    'Brandenburg-Prussia':  [
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123'],
    'England': [             
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '134123',
                            '134123'],
    'France': [
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123'],
    'Sweden': [             
                            '123123',
                            '123123',
                            '123123',
                            '123135',
                            '123135',
                            '123135',
                            '123135'],
    'Scotland': [            
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123'],
    'Russia': [              
                            '123223',
                            '123223',
                            '123223',
                            '123223',
                            '123223',
                            '123223',
                            '123223'],
    'Habsburg': [            
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123',
                            '123123']
    }
    
firstexplorescreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'France': [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Sweden': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            '']
    }

growthscreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'France': [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Sweden': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            '']
    }

energyscreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'France': [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Sweden': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            '']
    }

powercardscreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'France': [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Sweden': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            '']
    }

fastpowerscreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'France': [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Sweden': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            '']
    }
    
blightedislandscreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'France': [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Sweden': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            '']
    }
    
eventscreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'France': [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Sweden': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            '']
    }
    
fearscreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            'If no fear cards are resolved, perform the build from High Immigration Twice on this round.\n'],
    'France': [
                            '',
                            '',
                            '',
                            '',
                            '',
                            'Fear card effects never remove explorers. If one would, you may instead push that explorer.\n'],
    'Sweden': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            'When the stage III card is revealed, immediately place it in the build space (face up).\n',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            '']
    }
    
highimmigrationscreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            'If no fear cards were resolved, perform this build Twice.\n'],
    'France': [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Sweden': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            '']
    }

ravagescreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'France': [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Sweden': [              
                            'If the invaders do at least 6 damage to the land during Ravage, add and extra blight. OThe additional blight does not destroy presence or cascade.\n',
                            '',
                            '',
                            '',
                            'When ravaging adds at least one blight to a land, also add one town to an adjacent land without towns/cities. Cascading blight does not cause this effect.\n',
                            ''],
    'Scotland': [             
                            '',
                            '',
                            '',
                            '',
                            'After a ravage card adds blight to a coastal land, add one blight to that board\'s ocean (without cascading). Treat the ocean as a coastal wetland for this rule and for blight removal/movement.\n',
                            'After the ravage step, add one town to each inland land that matches a ravage card and is within one distance of a town/city.\n'],
    'Russia': [              
                            'When ravage adds blight to a land (including cascades), destroy one beast in that land.\n',
                            '',
                            'Ravage cards also match lands with 3 or more explorers. (If the land already matched the ravage card, it still ravages just once.)\n',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            'Ravages do +2 damage (total) if any adjacent lands have towns. (This does not cause lands without invaders to ravage)\n']
    }

buildscreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            'Invader build actions affect lands without invaders, if they are adjacent to at least 2 towns/cities before the build action\n',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'France': [
                            '',
                            'After invaders build in a land with 2 explorers or more, replace all but one explorer there with an equal number of towns.\n',
                            '',
                            'Whenever invaders build a coastal city, add one town to the adjacent land with the fewest towns.\n',
                            '',
                            ''],
    'Sweden': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [             
                            '',
                            '',
                            'In coastal lands, build cards affect lands without invaders, so long as there is an adjacent city.\n',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            'After the normal build step: In each land matching a build card, gather one town from a land not matching a build card. (In board/land order.)\n',
                            'When invaders would build one city in an inland land, they instead build two towns.\n',
                            '',
                            '',
                            '',
                            '']
    }

explorescreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'France': [
                            'After invaders successfully explore into a land which had no towns/cities, add one explorer there.\n',
                            '',
                            '',
                            '',
                            '',
                            'After the normal explore, on each board add one explorer to a land without any.\n'],
    'Sweden': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [             
                            'In coastal lands, explore cards add one town instead of explorer. \'Coastal lands\' invader cards do this for a maximum 2 lands per board.\n',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            'When the Habsburg reminder card is revealed, on each board, add one city to a coastal land without cities and one town to the 3 inland lands with the fewest blight.\n',
                            '']
    }

advancecardsscreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            'Remove the High Immigration tile when a stage II card is moved to it.\n',
                            '',
                            '',
                            ''],
    'France': [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Sweden': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            '']
    }

slowpowerscreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'France': [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Sweden': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            '']
    }

timepassesscreen_rules = {
    'Brandenburg-Prussia':  [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'England': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'France': [
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Sweden': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Scotland': [             
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Russia': [              
                            '',
                            '',
                            '',
                            '',
                            '',
                            ''],
    'Habsburg': [            
                            '',
                            '',
                            '',
                            '',
                            '',
                            '']
    }

screenTitles = { 'Main': 'Spirit Island Phase Tracker',
                 'SpiritSelect': 'Select Spirits',
                 'BoardSetup': 'Board Setup',
                 'SpiritSetup': 'Spirits Setup',
                 'FirstExplore': 'First Exploration', 
                 'Growth': 'Growth Phase', 
                 'Energy': 'Gain Energy',
                 'PowerCards': 'Select Power Cards', 
                 'FastPower': 'Fast Powers', 
                 'BlightedIsland': 'Blighted Island Effects', 
                 'Event': 'Event Card', 
                 'Fear': 'Fear Cards', 
                 'HighImmigration': 'High Immigration', 
                 'Ravage': 'Invaders Ravage the Island', 
                 'Build': 'Invaders Build on the Island', 
                 'Explore': 'Invaders Explore the Island', 
                 'AdvanceCards': 'Advance the Invader Cards', 
                 'SlowPower': 'Slow Powers', 
                 'TimePasses': 'Time Passes'}

screenDescriptions = {  'FirstExplore': 'Reveal the top card of the Invader deck. The invaders explore that land type. When done exploring, place this card in the Build space.\n', 
                        'Growth': 'Choose one option (unless stated otherwise) next to "Growth" at the upper right of the Spirit panel. Each section is a separate choice. You must do everything shown, but may choose the order.\n', 
                        'Energy': 'Gain an amount of Energy equal to the highest uncovered number on your Energy Presence Track.\n',
                        'PowerCards': 'Select the Power Cards you will use this turn. You must immediately pay Energy for all power cards played, even slow ones. Do not resolve the effects of the Power Cards yet.\n', 
                        'FastPower': 'Resolve fast powers - both Innate Powers on your spirit panel, and power cards played.\n', 
                        'BlightedIsland': '', 
                        'Event': 'Draw and Resolve Event Card', 
                        'Fear': 'If any Fear cards have been earned, pick up the whole face-down stack, flip it over and resolve the cards one at a time in the order they were earned.\n', 
                        'HighImmigration': 'Invaders take this Build action before Ravaging.\n', 
                        'Ravage': 'Look at the Invader Card in the Ravage Action space on the invader board (if any): the Invaders Ravage in each land of the shown type. First, Invaders deal Damage to the land and Dahan. Then, any surviving Dahan fight back.\n', 
                        'Build': 'Look at the Invader Card in the Build Action Space on the Invader board: the Invadrs build in each land of the shown type only.\n', 
                        'Explore': 'Turn the top card of the Invader Deck face-up. Invaders explore in accessible lands of the shown type only, venturing for from Towns and Cities or approaching from the Ocean.\n', 
                        'AdvanceCards': 'Slide all of the Invader cards left.', 
                        'SlowPower': 'Players resolve slow powers, which may be either Innate Powers printed on their Spirit Panel or Power cards they played.\n', 
                        'TimePasses': 'Players discard all Power cards played this turn into their personal discard piles. All elements go away. All Damage done during the turn goes away. If using any reminder tokens for single-turn effects, remove those at this time.\n'}

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
        global currentPhase 
        currentPhase = 'Main'
        self.next_button_value = 'Start'
        if use_timer:
            self.seconds = timer_seconds
            self.time = ''
            self.time = ':'.join(str(datetime.timedelta(seconds=self.seconds)).split(':')[1:])
            self.clock = Clock.schedule_interval(self.timer, 1)
        else:
            self.time = ''
        self.calc_health_damage()
    def on_next_Phase(self):
        global turn
        global previousPhase
        global opponent
        global currentPhase
        global use_timer
        global expansion
        global blight
        global level
        global stage
        self.calc_health_damage()
        previousPhase.append(currentPhase)
        if currentPhase == 'Main':
            nextP = 'SpiritSelect'
        if currentPhase == 'SpiritSelect':
            nextP = 'BoardSetup'
        if currentPhase == 'BoardSetup':
            nextP = 'SpiritSetup'
        if currentPhase == 'SpiritSetup':
            nextP = 'FirstExplore'
        if currentPhase == 'FirstExplore':
            nextP = 'Growth'
        if currentPhase == 'Growth':
            nextP = 'Energy'
        if currentPhase == 'Energy':
            nextP = 'PowerCards'
        if currentPhase == 'PowerCards':
            nextP = 'FastPower'
        if currentPhase == 'FastPower':
            if blight != 'Healthy':
                nextP = 'BlightedIsland'
            elif expansion == 'None':
                nextP = 'Fear'
            else:
                nextP = 'Event'
        if currentPhase == 'BlightedIsland':
            if expansion == 'None':
                nextP = 'Fear'
            else:
                nextP = 'Event'
        if currentPhase == 'Event':
            nextP = 'Fear'
        if currentPhase == 'Fear':
            if opponent == 'England' and int(level) == 3  and stage != "III" and turn > 1:
                nextP = 'HighImmigration'
            elif opponent == 'England' and int(level) >= 4 and turn > 1:
                nextP = 'HighImmigration'
            else:
                if turn > 1:
                    nextP = 'Ravage'
                else:
                    nextP = 'Build'
        if currentPhase == 'HighImmigration':
            if turn > 1:
                nextP = 'Ravage'
            else:
                nextP = 'Build'
        if currentPhase == 'Ravage':
            nextP = 'Build'
        if currentPhase == 'Build':
            nextP = 'Explore'
        if currentPhase == 'Explore':
            nextP = 'AdvanceCards'
        if currentPhase == 'AdvanceCards':
            nextP = 'SlowPower'
        if currentPhase == 'SlowPower':
            nextP = 'TimePasses'
        if currentPhase == 'TimePasses':
            nextP = 'Growth'
        self.title = screenTitles[nextP]
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
        if use_timer:
            Clock.unschedule(self.clock)
            self.seconds = timer_seconds
            self.time = ':'.join(str(datetime.timedelta(seconds=self.seconds)).split(':')[1:])
            self.clock = Clock.schedule_interval(self.timer, 1)
        else:
            self.time = ''
    def on_back(self):
        global previousPhase
        global level
        self.start_clock()
        prev = previousPhase[-1]
        self.title = screenTitles[prev]
        if prev != 'Main':
            previousPhase.pop()
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
        global blight
        if value:
            blight = 'Blighted'
            self.blighted = True
            write_state()
            return True
        else:
            blight = 'Healthy'
            self.blighted = False
            write_state()
            return False
    def calc_health_damage(self):
        self.ehealth = str(opponentmod_rules[opponent][int(level)][0])
        self.edamage = str(opponentmod_rules[opponent][int(level)][3])
        self.thealth = str(opponentmod_rules[opponent][int(level)][1])
        self.tdamage = str(opponentmod_rules[opponent][int(level)][4])
        self.chealth = str(opponentmod_rules[opponent][int(level)][2])
        self.cdamage = str(opponentmod_rules[opponent][int(level)][5])      
    time = StringProperty()
    def timer(self, *args):
        if use_timer:
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
        global stage
        global opponent
        global stage2_flag
        stage = value    
        app = App.get_running_app()
        if stage == 'I':
            self.I = True
            self.II = False
            self.III = False
        elif stage == 'II':
            self.II = True
            self.I = False
            self.III = False
        elif stage == 'III':
            self.III = True
            self.I = False
            self.II = False
        app.on_stage_toggle(stage)
        write_state()
    def read_state(self):
        global branchandclaw
        global jaggedearth
        global promopack1
        global promopack2
        global expansion
        global opponent
        global thematic
        global spirits
        global aspects
        global scenario
        global level
        global stage
        global blight
        global players
        global fear_tokens
        global turn
        global previousPhase
        global oppnent_list
        global spirit_list
        global scenarios_list
        global currentPhase
        branchandclaw = (store.get('branchandclaw')['value'])
        jaggedearth = (store.get('jaggedearth')['value'])
        promopack1 = (store.get('promopack1')['value'])
        promopack2 = (store.get('promopack2')['value'])
        expansion = (store.get('expansion')['value'])
        opponent = (store.get('opponent')['value'])
        thematic = (store.get('thematic')['value'])
        spirits = (store.get('spirits')['value'])
        aspects = (store.get('aspects')['value'])
        scenario = (store.get('scenario')['value'])
        level = (store.get('level')['value'])
        stage = (store.get('stage')['value'])
        blight = (store.get('blight')['value'])
        players = (store.get('players')['value'])
        fear_tokens = (store.get('fear_tokens')['value'])
        turn = (store.get('turn')['value'])
        previousPhase = (store.get('previousPhase')['value'])
        opponent_list = (store.get('opponent_list')['value'])
        spirit_list = (store.get('spirit_list')['value'])
        scenarios_list = (store.get('scenarios_list')['value'])
        #currentPhase=(store.get('currentPhase')['value'])
        #previousPhase.append(currentPhase)
        currentPhase = previousPhase[-1]
        self.lvl = level
        self.calc_health_damage()
        if blight != 'Healthy':
            self.blighted = True
        else:
            self.blighted = False
        self.on_stage_toggle(stage)
        if currentPhase == 'Main':
            nextP = 'SpiritSelect'
        if currentPhase == 'SpiritSelect':
            nextP = 'BoardSetup'
        if currentPhase == 'BoardSetup':
            nextP = 'SpiritSetup'
        if currentPhase == 'SpiritSetup':
            nextP = 'FirstExplore'
        if currentPhase == 'FirstExplore':
            nextP = 'Growth'
        if currentPhase == 'Growth':
            nextP = 'Energy'
        if currentPhase == 'Energy':
            nextP = 'PowerCards'
        if currentPhase == 'PowerCards':
            nextP = 'FastPower'
        if currentPhase == 'FastPower':
            if blight != 'Healthy':
                nextP = 'BlightedIsland'
            elif expansion == 'None':
                nextP = 'Fear'
            else:
                nextP = 'Event'
        if currentPhase == 'BlightedIsland':
            if expansion == 'None':
                nextP = 'Fear'
            else:
                nextP = 'Event'
        if currentPhase == 'Event':
            nextP = 'Fear'
        if currentPhase == 'Fear':
            if opponent == 'England' and int(level) == 3  and stage != "III" and turn > 1:
                nextP = 'HighImmigration'
            elif opponent == 'England' and int(level) >= 4 and turn > 1:
                nextP = 'HighImmigration'
            else:
                if turn > 1:
                    nextP = 'Ravage'
                else:
                    nextP = 'Build'
        if currentPhase == 'HighImmigration':
            if turn > 1:
                nextP = 'Ravage'
            else:
                nextP == 'Build'
        if currentPhase == 'Ravage':
            nextP = 'Build'
        if currentPhase == 'Build':
            nextP = 'Explore'
        if currentPhase == 'Explore':
            nextP = 'AdvanceCards'
        if currentPhase == 'AdvanceCards':
            nextP = 'SlowPower'
        if currentPhase == 'SlowPower':
            nextP = 'TimePasses'
        if currentPhase == 'TimePasses':
            nextP = 'Growth'
        self.title = screenTitles[nextP]
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
    opp_list = ListProperty(base_opp)
    scen_list = ListProperty(base_scenarios)
    def on_enter(self):
        global branchandclaw
        global jaggedearth
        global promopack1
        global promopack2
        global opponent
        global level
        global players
        global stage2_flag
        global currentPhase
        global scenarios_list
        self.scen_list = scenarios_list
        currentPhase = 'Main'
        if branchandclaw:
            self.bc = True
        self.je = jaggedearth
        self.pp1 = promopack1
        self.pp2 = promopack2
        self.opp = opponent
        self.play = str(players)
        self.lvl = level
        self.theme = thematic
    def bc_clicked(self, value):
        global branchandclaw
        if value == True:
            branchandclaw = True
        else:
            branchandclaw = False
        self.build_expansions()
        self.build_spirits()
        self.build_scenarios()
        if self.opp not in self.opp_list:
            self.opponent_clicked('None')
    def je_clicked(self, value):
        global jaggedearth
        if value == True:
            jaggedearth = True
        else:
            jaggedearth = False
        self.build_expansions()
        self.build_spirits()
        self.build_scenarios()
        if self.opp not in self.opp_list:
            self.opponent_clicked('None')
        if self.play not in self.max_play:
            self.players_clicked('0')
    def promo1_clicked(self, value):
        global promopack1
        if value == True:
            promopack1 = True
        else:
            promopack1 = False
        self.build_expansions()
        self.build_spirits()
        self.build_scenarios()
        if self.opp not in self.opp_list:
            self.opponent_clicked('None')
    def promo2_clicked(self, value):
        global promopack2
        if value == True:
            promopack2 = True
        else:
            promopack2 = False
        self.build_expansions()
        self.build_spirits()
        self.build_scenarios()
        if self.opp not in self.opp_list:
            self.opponent_clicked('None')
    def thematic_clicked(self, value):
        global thematic
        if value == True:
            thematic = True
        else:
            thematic = False
    def opponent_clicked(self, value):
        global opponent
        global level
        opponent = value
        self.opp = value
        self.build_levels()
        self.lvl = level
        if self.opp != 'None' and self.lvl == '0':
            self.level_clicked('1')
        if self.opp == 'None':
            self.level_clicked('0')
    def level_clicked(self, value):
        global level
        level = value
        self.lvl = level
    def players_clicked(self, value):
        global players
        players = value
        self.play = players
        stage2_flag['Scotland'] = 'If the invader card has a flag:\nOn the single board with the most coastal towns/cities add one town to the '+ str(players) +' lands with the fewest towns.\n'
    def build_expansions(self):
        global branchandclaw
        global jaggedearth
        global promopack2
        global expansion
        self.max_play = ['1','2','3','4']
        opponent_list = base_opp
        if branchandclaw:
            opponent_list = opponent_list + bc_opp
        if jaggedearth:
            opponent_list = opponent_list + je_opp
            self.max_play = ['1','2','3','4','5','6']
        if promopack2:
            opponent_list = opponent_list + pp2_opp
        self.opp_list = sorted(opponent_list)
        if branchandclaw and jaggedearth:
            expansion = "BC and JE"
        elif branchandclaw and not jaggedearth:
            expansion = "Branch and Claw"
        elif jaggedearth and not branchandclaw:
            expansion = "Jagged Earth"
        else:
            expansion = 'None'
    def build_spirits(self):
        global base_spirits
        global branchandclaw
        global jaggedearth
        global promopack1
        global promopack2
 #       global spirits
        global spirit_list
        spirit_list = base_spirits
        if branchandclaw:
            spirit_list = spirit_list + bc_spirits
        if jaggedearth:
            spirit_list = spirit_list + je_spirits
        if promopack1:
            spirit_list = spirit_list + pp1_spirits
        if promopack2:
            spirit_list = spirit_list + pp2_spirits
        spirit_list = sorted(spirit_list)
    def build_scenarios(self):
        global branchandclaw
        global jaggedearth
        global promopack1
        global promopack2
        global scenarios
        global scenarios_list
        scenario_list = base_scenarios
        scenarios_list = base_scenarios
        if branchandclaw:
            scenarios_list = scenarios_list + bc_scenarios
        if jaggedearth:
            scenarios_list = scenarios_list + je_scenarios
        if promopack1:
            scenarios_list = scenarios_list + pp1_scenarios
        if promopack2:
            scenarios_list = scenarios_list + pp2_scenarios
        self.scen_list = sorted(scenarios_list)   
    def build_levels(self):
        self.max_levels = ['0']
        global levels
        if opponent != 'None':
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
        global currentPhase
        global spirit_list
        global players
        global aspects
        self.spirit_values = spirit_list
        currentPhase = 'SpiritSelect'
        write_state()
        self.play = int(players)
        self.spirit1 = spirits[0]
        self.spirit2 = spirits[1]
        self.spirit3 = spirits[2]
        self.spirit4 = spirits[3]
        self.spirit5 = spirits[4]
        self.spirit6 = spirits[5]
        self.aspect1 = aspects[0]
        self.aspect2 = aspects[1]
        self.aspect3 = aspects[2]
        self.aspect4 = aspects[3]
        self.aspect5 = aspects[4]
        self.aspect6 = aspects[5]
    def on_select_spirit(self, player, value):
        global spirit_aspects
        global jaggedearth
        global branchandclaw
        global promopack1
        global promopack2
        global spirits
        if player == 1:
            if len(spirit_aspects[value]) == 0:
                self.spirit1_has_aspect = False
            else:
                for item in spirit_aspects[value]:
                    if branchandclaw:
                        if item.split(':')[0] == 'bc':
                            self.spirit1_aspects.append(item.split(':')[1])
                    if jaggedearth:
                        if item.split(':')[0] == 'je':
                            self.spirit1_aspects.append(item.split(':')[1])
                    if promopack1:
                        if item.split(':')[0] == 'pp1':
                            self.spirit1_aspects.append(item.split(':')[1])
                    if promopack2:
                        if item.split(':')[0] == 'pp2':
                            self.spirit1_aspects.append(item.split(':')[1])
                if len(self.spirit1_aspects) == 0:
                    self.spirit1_has_aspect = False
                else:
                    self.spirit1_has_aspect = True
                    self.spirit1_aspects = ['None'] + self.spirit1_aspects
            spirits[0] = value
        if player == 2:
            if len(spirit_aspects[value]) == 0:
                self.spirit2_has_aspect = False
            else:
                for item in spirit_aspects[value]:
                    if branchandclaw:
                        if item.split(':')[0] == 'bc':
                            self.spirit2_aspects.append(item.split(':')[1])
                    if jaggedearth:
                        if item.split(':')[0] == 'je':
                            self.spirit2_aspects.append(item.split(':')[1])
                    if promopack1:
                        if item.split(':')[0] == 'pp1':
                            self.spirit2_aspects.append(item.split(':')[1])
                    if promopack2:
                        if item.split(':')[0] == 'pp2':
                            self.spirit2_aspects.append(item.split(':')[1])
                if len(self.spirit2_aspects) == 0:
                    self.spirit2_has_aspect = False
                else:
                    self.spirit2_has_aspect = True
                    self.spirit2_aspects = ['None'] + self.spirit2_aspects
            spirits[1] = value
        if player == 3:
            if len(spirit_aspects[value]) == 0:
                self.spirit3_has_aspect = False
            else:
                for item in spirit_aspects[value]:
                    if branchandclaw:
                        if item.split(':')[0] == 'bc':
                            self.spirit3_aspects.append(item.split(':')[1])
                    if jaggedearth:
                        if item.split(':')[0] == 'je':
                            self.spirit3_aspects.append(item.split(':')[1])
                    if promopack1:
                        if item.split(':')[0] == 'pp1':
                            self.spirit3_aspects.append(item.split(':')[1])
                    if promopack2:
                        if item.split(':')[0] == 'pp2':
                            self.spirit3_aspects.append(item.split(':')[1])
                if len(self.spirit3_aspects) == 0:
                    self.spirit3_has_aspect = False
                else:
                    self.spirit3_has_aspect = True
                    self.spirit3_aspects = ['None'] + self.spirit3_aspects                        
            spirits[2] = value
        if player == 4:
            if len(spirit_aspects[value]) == 0:
                self.spirit4_has_aspect = False
            else:
                for item in spirit_aspects[value]:
                    if branchandclaw:
                        if item.split(':')[0] == 'bc':
                            self.spirit4_aspects.append(item.split(':')[1])
                    if jaggedearth:
                        if item.split(':')[0] == 'je':
                            self.spirit4_aspects.append(item.split(':')[1])
                    if promopack1:
                        if item.split(':')[0] == 'pp1':
                            self.spirit4_aspects.append(item.split(':')[1])
                    if promopack2:
                        if item.split(':')[0] == 'pp2':
                            self.spirit4_aspects.append(item.split(':')[1])
                if len(self.spirit4_aspects) == 0:
                    self.spirit4_has_aspect = False
                else:
                    self.spirit4_has_aspect = True
                    self.spirit4_aspects = ['None'] + self.spirit4_aspects
            spirits[3] = value
        if player == 5:
            if len(spirit_aspects[value]) == 0:
                self.spirit5_has_aspect = False
            else:
                for item in spirit_aspects[value]:
                    if branchandclaw:
                        if item.split(':')[0] == 'bc':
                            self.spirit5_aspects.append(item.split(':')[1])
                    if jaggedearth:
                        if item.split(':')[0] == 'je':
                            self.spirit5_aspects.append(item.split(':')[1])
                    if promopack1:
                        if item.split(':')[0] == 'pp1':
                            self.spirit5_aspects.append(item.split(':')[1])
                    if promopack2:
                        if item.split(':')[0] == 'pp2':
                            self.spirit5_aspects.append(item.split(':')[1])
                if len(self.spirit5_aspects) == 0:
                    self.spirit5_has_aspect = False
                else:
                    self.spirit5_has_aspect = True
                    self.spirit5_aspects = ['None'] + self.spirit5_aspects
            spirits[4] = value
        if player == 6:
            if len(spirit_aspects[value]) == 0:
                self.spirit6_has_aspect = False
            else:
                for item in spirit_aspects[value]:
                    if branchandclaw:
                        if item.split(':')[0] == 'bc':
                            self.spirit6_aspects.append(item.split(':')[1])
                    if jaggedearth:
                        if item.split(':')[0] == 'je':
                            self.spirit6_aspects.append(item.split(':')[1])
                    if promopack1:
                        if item.split(':')[0] == 'pp1':
                            self.spirit6_aspects.append(item.split(':')[1])
                    if promopack2:
                        if item.split(':')[0] == 'pp2':
                            self.spirit6_aspects.append(item.split(':')[1])
                if len(self.spirit6_aspects) == 0:
                    self.spirit6_has_aspect = False
                else:
                    self.spirit6_has_aspect = True
                    self.spirit6_aspects = ['None'] + self.spirit6_aspects
            spirits[5] = value
    def on_select_aspect(self, player, value):
        global aspects
        aspects[player-1] = value
        
#Board Setup Screen
#Corresponds to kivy main
class BoardSetupScreen(Screen):
    text = StringProperty('')
    def on_enter(self):                 #override of on_enter, runs when screen is constructed
        #pull in global variables needed to access or update on this screen
        global expansion
        global fear_cards
        global fear_tokens
        global players
        global currentPhase
        global thematic
        currentPhase = 'BoardSetup'
        write_state()
        start = ''
        fear = ''
        invaders = ''
        exsetup = ''
        ft = ''
        bt = ''
        
        if fear_cards[opponent][int(level)-1] != '':
            fear = 'Fear Cards ' + fear_cards[opponent][int(level)-1] + '\n'  #calculate fear cards into local fear
        
        #loop to add all setup changes together (cumulative) from setup_changes up to opponent level into local start
        for x in range(int(level)):
            start += setup_changes[opponent][x]
            
        invaders = 'Invader Deck: ' + invader_deck[opponent][int(level)-1]  + '\n' #set local invaders to invader deck based on opponent & level
        if thematic:
            exsetup = 'Follow the icons on the thematic map for all invaders and tokens.'
        else:
            exsetup = expansion_setup[expansion]     #copy expansion_setup into local exsetup
        if opponent == 'England' and int(level) == 6:
            fear_per = 5
        else:
            fear_per = 4
        fear_tokens = fear_per * int(players)    #calculate number of fear tokens into global fear_tokens
        ft = 'Fear Tokens: ' + str(fear_tokens) + '\n'   #copy global fear_tokens into local ft
        blight_tokens = (2 * int(players)) + 1
        bt = 'Blight Tokens: ' + str(blight_tokens)+ '\n'
        self.text = '\n'.join([start, fear, invaders, exsetup, ft, bt])
        
class SpiritSetupScreen(Screen):
    spirits_text = StringProperty('')
    def on_enter(self):
        global currentPhase
        global spirits
        global spirits_setup
        currentPhase = 'SpiritSetup'
        self.spirits_text = ''
        for x in spirits:
            if x != 'None':
                self.spirits_text = self.spirits_text + x + ': ' + spirit_setup[x] + '\n'
                
class FirstExploreScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'FirstExplore'
        write_state()
        global firstexplorescreen_rules
        global screenDescriptions
        description = ''
        rules = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        if displayopts[currentPhase]['rules']:
            for x in range(int(level)):
                rules += firstexplorescreen_rules[opponent][x]
        self.text = '\n'.join([description + rules])
        
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
        global currentPhase
        currentPhase = 'Growth'
        write_state()
        global turn
        turn = turn +1
        global growthscreen_rules
        global expansion
        global spirits
        global spirit_growth_count
        global screenDescriptions
        self.text = ''
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        spirits_text = ''
        if displayopts[currentPhase]['spirits']:
            for x in spirits:
                if spirit_growth_count[x] > 1:
                    self.spirits_text = 'Spirits with more than one Growth action can use energy gained from one action to pay for another.\n'
        opprules = ""
        allrules = ""
        badlands = ""
        if expansion == "BC and JE" or expansion == "Jagged Earth":
            if displayopts[currentPhase]['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += growthscreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        self.text = '\n'.join([description, spirits_text, opprules, badlands, allrules])
        
class EnergyScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'Energy'
        write_state()
        global energyscreen_rules
        global expansion
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        opprules = ""
        allrules = ""
        badlands = ""
        if expansion == "BC and JE" or expansion == "Jagged Earth":
            if displayopts[currentPhase]['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += energyscreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        self.text = '\n'.join([description,opprules, badlands, allrules])
            
class PowerCardsScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'PowerCards'
        write_state()
        global powercardscreen_rules
        global expansion
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        opprules = ""
        allrules = ""
        badlands = ""
        if expansion == "BC and JE" or expansion == "Jagged Earth":
            if displayopts[currentPhase]['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += powercardscreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        self.text = '\n'.join([description,opprules, badlands, allrules])
            
class FastPowerScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'FastPower'
        write_state()
        global fastpowerscreen_rules
        global expansion
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        opprules = ""
        allrules = ""
        badlands = ""
        if expansion == "BC and JE" or expansion == "Jagged Earth":
            if displayopts[currentPhase]['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += fastpowerscreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        self.text = '\n'.join([description,opprules, badlands, allrules])
        
class BlightedIslandScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'BlightedIsland'
        write_state()
        global blightedislandscreen_rules
        global expansion
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        opprules = ""
        allrules = ""
        badlands = ""
        if expansion == "BC and JE" or expansion == "Jagged Earth":
            if displayopts[currentPhase]['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += blightedislandscreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        self.text = '\n'.join([description,opprules, badlands, allrules])
            
class EventScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'Event'
        write_state()
        global turn
        global eventscreen_rules
        global expansion
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        opprules = ""
        allrules = ""
        badlands = ""
        discard = ""
        if expansion == "BC and JE" or expansion == "Jagged Earth":
            if displayopts[currentPhase]['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += eventscreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        if displayopts[currentPhase]['discard']:
            if turn == 1:
                discard += 'Turn over the first event card, but discard it with no action. (Optional rule for Branch and Claw)\n'
        self.text = '\n'.join([description, opprules, badlands, allrules, discard])

            
class FearScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'Fear'
        write_state()
        global fearscreen_rules
        global opponent
        global level
        global expansion
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        opprules = ""
        allrules = ""
        badlands = ""
        if expansion == "BC and JE" or expansion == "Jagged Earth":
            if displayopts[currentPhase]['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += fearscreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        self.text = '\n'.join([description,opprules, badlands, allrules])
            
class HighImmigrationScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'HighImmigration'
        write_state()
        global highimmigrationscreen_rules
        global expansion
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        opprules = ""
        allrules = ""
        badlands = ""
        if expansion == "BC and JE" or expansion == "Jagged Earth":
            if displayopts[currentPhase]['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += highimmigrationscreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        self.text = '\n'.join([description,opprules, badlands, allrules])
            
class RavageScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'Ravage'
        write_state()
        global ravagescreen_rules
        global expansion
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        opprules = ""
        allrules = ""
        badlands = ""
        strife = ""
        if displayopts[currentPhase]['strife']:
            if expansion != 'None':
                strife = 'If present, Strife Tokens block specific invaders from doing damage. Remove the token.\n'
        if opponent == 'Russia' and int(level) ==6  and turn > 1:
            opprules += "After the ravage step, on each board where it added no blight: in the land with the most explorers (min 1) add one explorer and one town.\n"
        if expansion == "BC and JE" or expansion == "Jagged Earth":
            if displayopts[currentPhase]['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += ravagescreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        self.text = '\n'.join([description,strife,opprules, badlands, allrules])            
            
class BuildScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'Build'
        write_state()
        global buildscreen_rules
        global expansion
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        opprules = ""
        allrules = ""
        badlands = ""
        disease = ""
        if displayopts[currentPhase]['disease']:
            if expansion != 'None':
                disease = 'If present, Disease tokens prevent this build. Remove the token.\n'
        if expansion == "BC and JE" or expansion == "Jagged Earth":
            if displayopts[currentPhase]['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += buildscreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        self.text = '\n'.join([description,disease,opprules, badlands, allrules])
      
#Explore Screen
#Corresponds to Kivy Explore
#Note extra local variable flag, and update to the on_stage_toggle method
class ExploreScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'Explore'
        write_state()
        global explorescreen_rules
        global expansion
        global opponent
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        opprules = ""
        allrules = ""
        badlands = ""
        wilds = ""
        if displayopts[currentPhase]['wilds']:
            if expansion != 'None':
                wilds = 'If a wilds token is present, skip that exploration and discard one wilds token.\n'
        if expansion == "BC and JE" or expansion == "Jagged Earth":
            if displayopts[currentPhase]['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += explorescreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        self.text = '\n'.join([description,wilds,opprules, badlands, allrules])       

        
class AdvanceCardsScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'AdvanceCards'
        write_state()
        global advancecardsscreen_rules
        global opponent
        global level
        global expansion
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        opprules = ""
        allrules = ""
        badlands = ""
        if expansion == "BC and JE" or expansion == "Jagged Earth":
            if displayopts[currentPhase]['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += advancecardsscreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        self.text = '\n'.join([description,opprules, badlands, allrules])
            
class SlowPowerScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'SlowPower'
        write_state()
        global slowpowerscreen_rules
        global expansion
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        opprules = ""
        allrules = ""
        badlands = ""
        if expansion == "BC and JE" or expansion == "Jagged Earth":
            if displayopts[currentPhase]['badlands']:
                badlands = 'Badlands token increases damage to Invaders/Dahan by 1. (Once per action.)\n'
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += slowpowerscreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        self.text = '\n'.join([description,opprules, badlands, allrules])
            
class TimePassesScreen(Screen):
    text = StringProperty('')
    def on_enter(self):
        global currentPhase
        currentPhase = 'TimePasses'
        write_state()
        global timepassesscreen_rules
        description = ''
        if displayopts[currentPhase]['phase']:
            description = screenDescriptions[currentPhase]
        opprules = ""
        allrules = ""
        #loop to add all phase changes together (cumulative) up to opponent level into local opprules
        if displayopts[currentPhase]['opponent']:
            for x in range(int(level)):
                opprules += timepassesscreen_rules[opponent][x]
        if displayopts[currentPhase]['all']:
            for x in range(int(level)):
                allrules += allscreen_rules[opponent][x]
        self.text = '\n'.join([description,opprules, allrules])
    
store = JsonStore('sipt.json')
def write_state():
    global branchandclaw
    global jaggedearth
    global promopack2
    global expansion
    global opponent
    global thematic
    global level
    global stage
    global blight
    global players
    global fear_tokens
    global turn
    global previousPhase
    global oppnent_list
    global currentPhase
    store.put('branchandclaw', value=branchandclaw)
    store.put('jaggedearth', value=jaggedearth)
    store.put('promopack1', value=promopack1)
    store.put('promopack2', value=promopack2)
    store.put('expansion', value=expansion)
    store.put('opponent', value=opponent)
    store.put('thematic', value=thematic)
    store.put('spirits', value=spirits)
    store.put('aspects', value=aspects)
    store.put('scenario', value=scenario)
    store.put('level', value=level)
    store.put('stage', value=stage)
    store.put('blight', value=blight)
    store.put('players', value=players)
    store.put('fear_tokens', value=fear_tokens)
    store.put('turn', value=turn)
    store.put('previousPhase', value=previousPhase)
    store.put('opponent_list', value=opponent_list)
    store.put('currentPhase', value=currentPhase)
    store.put('spirit_list', value=spirit_list)
    store.put('scenarios_list', value=scenarios_list)



   
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
    blah = 0
    def build(self):
        global use_timer
        global timer_seconds
        if int(self.config.get('timeroptions', 'usetimer')) == 0:
            use_timer = False
        else:
            use_timer = True
        timer_seconds = int(self.config.get('timeroptions', 'timerseconds'))
        global displayopts
        displayopts['FirstExplore'] = {}
        for item in ['phase', 'rules']:
            displayopts['FirstExplore'][item] = int(self.config.get('FirstExplore', item))
        displayopts['Growth'] = {}
        for item in ['phase', 'badlands', 'opponent', 'all', 'spirits']:
            displayopts['Growth'][item] = int(self.config.get('Growth', item))
        displayopts['Energy'] = {}
        for item in ['phase', 'badlands', 'opponent', 'all']:
            displayopts['Energy'][item] = int(self.config.get('Energy', item))
        displayopts['PowerCards'] = {}
        for item in ['phase', 'badlands', 'opponent', 'all']:
            displayopts['PowerCards'][item] = int(self.config.get('PowerCards', item))
        displayopts['FastPower'] = {}
        for item in ['phase', 'badlands', 'opponent', 'all']:
            displayopts['FastPower'][item] = int(self.config.get('FastPower', item))
        displayopts['BlightedIsland'] = {}
        for item in ['phase', 'badlands', 'opponent', 'all']:
            displayopts['BlightedIsland'][item] = int(self.config.get('BlightedIsland', item))
        displayopts['Event'] = {}
        for item in ['phase', 'badlands', 'opponent', 'all', 'discard']:
            displayopts['Event'][item] = int(self.config.get('Event', item))
        displayopts['Fear'] = {}
        for item in ['phase', 'badlands', 'opponent', 'all']:
            displayopts['Fear'][item] = int(self.config.get('Fear', item))
        displayopts['HighImmigration'] = {}
        for item in ['phase', 'badlands', 'opponent', 'all']:
            displayopts['HighImmigration'][item] = int(self.config.get('HighImmigration', item))
        displayopts['Ravage'] = {}
        for item in ['phase', 'badlands', 'opponent', 'all', 'strife']:
            displayopts['Ravage'][item] = int(self.config.get('Ravage', item))
        displayopts['Build'] = {}
        for item in ['phase', 'badlands', 'opponent', 'all', 'disease']:
            displayopts['Build'][item] = int(self.config.get('Build', item))
        displayopts['Explore'] = {}
        for item in ['phase', 'badlands', 'opponent', 'all', 'wilds']:
            displayopts['Explore'][item] = int(self.config.get('Explore', item))
        displayopts['AdvanceCards'] = {}
        for item in ['phase', 'badlands', 'opponent', 'all']:
            displayopts['AdvanceCards'][item] = int(self.config.get('AdvanceCards', item))
        displayopts['SlowPower'] = {}
        for item in ['phase', 'badlands', 'opponent', 'all']:
            displayopts['SlowPower'][item] = int(self.config.get('SlowPower', item))        
        displayopts['TimePasses'] = {}
        for item in ['phase', 'opponent', 'all']:
            displayopts['TimePasses'][item] = int(self.config.get('TimePasses', item))  
    def on_stop(self):
        return True

    #build_config method, sets default values for the config if no .ini exists
    def build_config(self, config):
        config.setdefaults('timeroptions', {
                                'usetimer': 1,
                                'timerseconds': '180'
                            }
                        )
        config.setdefaults('FirstExplore', {
                                'phase': 1,
                                'rules': 1
                            }
                        )
        config.setdefaults('Growth', {
                                'phase': 1,
                                'spirits': 1,
                                'badlands': 1,
                                'opponent': 1,
                                'all': 1,
                            }
                        )
        config.setdefaults('Energy', {
                                'phase': 1,
                                'badlands': 1,
                                'opponent': 1,
                                'all': 1,
                            }
                        )
        config.setdefaults('PowerCards', {
                                'phase': 1,
                                'badlands': 1,
                                'opponent': 1,
                                'all': 1,
                            }
                        )
        config.setdefaults('FastPower', {
                                'phase': 1,
                                'badlands': 1,
                                'opponent': 1,
                                'all': 1,
                            }
                        )
        config.setdefaults('BlightedIsland', {
                                'phase': 1,
                                'badlands': 1,
                                'opponent': 1,
                                'all': 1,
                            }
                        )  
        config.setdefaults('Event', {
                                'phase': 1,
                                'badlands': 1,
                                'opponent': 1,
                                'all': 1,
								'discard': 1
                            }
                        )
        config.setdefaults('Fear', {
                                'phase': 1,
                                'badlands': 1,
                                'opponent': 1,
                                'all': 1,
                            }
                        )
        config.setdefaults('HighImmigration', {
                                'phase': 1,
                                'badlands': 1,
                                'opponent': 1,
                                'all': 1,
                            }
                        )
        config.setdefaults('Ravage', {
                                'phase': 1,
                                'badlands': 1,
                                'opponent': 1,
                                'all': 1,
                                'strife': 1
                            }
                        )
        config.setdefaults('Build', {
                                'phase': 1,
                                'badlands': 1,
                                'opponent': 1,
                                'all': 1,
                                'disease': 1
                            }
                        )
        config.setdefaults('Explore', {
                                'phase': 1,
                                'badlands': 1,
                                'opponent': 1,
                                'all': 1,
                                'wilds': 1
                            }
                        )
        config.setdefaults('AdvanceCards', {
                                'phase': 1,
                                'badlands': 1,
                                'opponent': 1,
                                'all': 1,
                            }
                        )
        config.setdefaults('SlowPower', {
                                'phase': 1,
                                'badlands': 1,
                                'opponent': 1,
                                'all': 1,
                            }
                        )
        config.setdefaults('TimePasses', {
                                'phase': 1,
                                'opponent': 1,
                                'all': 1,
                            }
                        )                        
    #build_settigns loads the json file, and  defines the name for the panel in the settings screen
    def build_settings(self, settings):
        settings.add_json_panel('Spirit Island',
                                self.config,
                                data=settings_json)
        
    #on_config_change method - called when a user changes anything in settings screen, similar to the build.                            
    def on_config_change(self, config, section, key, value):
        global use_timer
        global timer_seconds
        global displayopts
        if section == 'timeroptions':
            if int(self.config.get('timeroptions', 'usetimer')) == 0:
                use_timer = False
            else:
                use_timer = True
            timer_seconds = int(self.config.get('timeroptions', 'timerseconds'))
        else:
            #displayopts[section]={}
            displayopts[section][key]=int(value)
            
    def on_stage_toggle(self, value):
        global opponent
        self.blah = 1
        if value == 'II':
            if opponent != 'None':
                self.flagicon = True
                self.stage2flag = stage2_flag[opponent]
                self.stage2flag = stage2_flag[opponent]
            else:
                self.flagicon = False
                self.stage2flag = ''
        else:
            self.flagicon = False
            self.stage2flag = ''
        return self

        
        
MainApp().run()


