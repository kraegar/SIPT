import json

settings_json = json.dumps([
    {'type': 'title',
     'title': 'Timer Sttings'},
     
    {'type': 'bool',
     'title': 'Enable Timer',
     'desc': 'Enable the CountdownTimer for Game Phases',
     'section': 'timeroptions',
     'key': 'usetimer'},
     
     {'type': 'numeric',
     'title': 'Timer Seconds',
     'desc': 'How Many Seconds to Count Down',
     'section': 'timeroptions',
     'key': 'timerseconds'},  
     
    {'type': 'title',
     'title': 'First Exploration Screen'},

    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'FirstExplore',
    'key': 'phase'},
    
    {'type': 'bool',
    'title': 'Phase Rules',
    'desc': 'Enable Phase Rules Text',
    'section': 'FirstExplore',
    'key': 'rules'},
    
    {'type': 'title',
     'title': 'Growth Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'Growth',
    'key': 'phase'},
    
    {'type': 'bool',
    'title': 'Spirits Reminders',
    'desc': 'Enable Spirits Reminder text',
    'section': 'Growth',
    'key': 'spirits'},
    
    {'type': 'bool',
    'title': 'Badlands',
    'desc': 'Enable Badlands Text',
    'section': 'Growth',
    'key': 'badlands'},
    
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'Growth',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'Growth',
    'key': 'all'},
    
    {'type': 'title',
     'title': 'Energy Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'Energy',
    'key': 'phase'},

    {'type': 'bool',
    'title': 'Badlands',
    'desc': 'Enable Badlands Text',
    'section': 'Energy',
    'key': 'badlands'},
    
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'Energy',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'Energy',
    'key': 'all'},
    
    {'type': 'title',
     'title': 'Power Cards Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'PowerCards',
    'key': 'phase'},

    {'type': 'bool',
    'title': 'Badlands',
    'desc': 'Enable Badlands Text',
    'section': 'PowerCards',
    'key': 'badlands'},
    
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'PowerCards',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'PowerCards',
    'key': 'all'},   
    
    {'type': 'title',
     'title': 'Fast Power Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'FastPower',
    'key': 'phase'},

    {'type': 'bool',
    'title': 'Badlands',
    'desc': 'Enable Badlands Text',
    'section': 'FastPower',
    'key': 'badlands'},
    
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'FastPower',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'FastPower',
    'key': 'all'},
    
    {'type': 'title',
     'title': 'Blighted Island Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'BlightedIsland',
    'key': 'phase'},

    {'type': 'bool',
    'title': 'Badlands',
    'desc': 'Enable Badlands Text',
    'section': 'BlightedIsland',
    'key': 'badlands'},
    
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'BlightedIsland',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'BlightedIsland',
    'key': 'all'},

    {'type': 'title',
     'title': 'Event Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'Event',
    'key': 'phase'},

    {'type': 'bool',
    'title': 'Badlands',
    'desc': 'Enable Badlands Text',
    'section': 'Event',
    'key': 'badlands'},
    
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'Event',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'Event',
    'key': 'all'},
	
    {'type': 'bool',
    'title': 'Turn 1 Discard Rule',
    'desc': 'Enable Turn 1 Event Card Rule Text',
    'section': 'Event',
    'key': 'discard'},

    {'type': 'title',
     'title': 'Fear Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'Fear',
    'key': 'phase'},

    {'type': 'bool',
    'title': 'Badlands',
    'desc': 'Enable Badlands Text',
    'section': 'Fear',
    'key': 'badlands'},
    
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'Fear',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'Fear',
    'key': 'all'},

    {'type': 'title',
     'title': 'High Immigration Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'HighImmigration',
    'key': 'phase'},

    {'type': 'bool',
    'title': 'Badlands',
    'desc': 'Enable Badlands Text',
    'section': 'HighImmigration',
    'key': 'badlands'},
    
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'HighImmigration',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'HighImmigration',
    'key': 'all'},

    {'type': 'title',
     'title': 'Ravage Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'Ravage',
    'key': 'phase'},

    {'type': 'bool',
    'title': 'Badlands',
    'desc': 'Enable Badlands Text',
    'section': 'Ravage',
    'key': 'badlands'},
    
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'Ravage',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'Ravage',
    'key': 'all'},
	
    {'type': 'bool',
    'title': 'Strife',
    'desc': 'Enable Strife Text',
    'section': 'Ravage',
    'key': 'strife'},

    {'type': 'title',
     'title': 'Build Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'Build',
    'key': 'phase'},

    {'type': 'bool',
    'title': 'Badlands',
    'desc': 'Enable Badlands Text',
    'section': 'Build',
    'key': 'badlands'},
    
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'Build',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'Build',
    'key': 'all'},
	
    {'type': 'bool',
    'title': 'Disease',
    'desc': 'Enable Disease Text',
    'section': 'Build',
    'key': 'disease'},

    {'type': 'title',
     'title': 'Explore Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'Explore',
    'key': 'phase'},

    {'type': 'bool',
    'title': 'Badlands',
    'desc': 'Enable Badlands Text',
    'section': 'Explore',
    'key': 'badlands'},
    
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'Explore',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'Explore',
    'key': 'all'},
	
    {'type': 'bool',
    'title': 'Wilds',
    'desc': 'Enable Disease Text',
    'section': 'Explore',
    'key': 'wilds'},

    {'type': 'title',
     'title': 'Advance Cards Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'AdvanceCards',
    'key': 'phase'},

    {'type': 'bool',
    'title': 'Badlands',
    'desc': 'Enable Badlands Text',
    'section': 'AdvanceCards',
    'key': 'badlands'},
    
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'AdvanceCards',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'AdvanceCards',
    'key': 'all'},

    {'type': 'title',
     'title': 'Slow Power Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'SlowPower',
    'key': 'phase'},

    {'type': 'bool',
    'title': 'Badlands',
    'desc': 'Enable Badlands Text',
    'section': 'SlowPower',
    'key': 'badlands'},
    
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'SlowPower',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'SlowPower',
    'key': 'all'},

    {'type': 'title',
     'title': 'Time Passes Screen'},
     
    {'type': 'bool',
    'title': 'Phase Description',
    'desc': 'Enable Phase Description Text',
    'section': 'TimePasses',
    'key': 'phase'},
   
    {'type': 'bool',
    'title': 'Adversary Phase Rules',
    'desc': 'Enable Adversary Rules Text',
    'section': 'TimePasses',
    'key': 'opponent'},
    
    {'type': 'bool',
    'title': 'Adversary Loss Condition',
    'desc': 'Enable Adversary Loss Condition (and other text that might affect all stages)',
    'section': 'TimePasses',
    'key': 'all'},	
    ])     
