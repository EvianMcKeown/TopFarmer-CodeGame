# levels.py
from farmgrid import FarmGrid
from farmer import Farmer
from farmtile import FarmTile, CropTile
import json
class Levels:
    def __init__(self): 
    # initialises levels dictionary with data and sets current level to lvl 1
        self.levels = {
            1: {
                'task': 'Plant 5 potatoes in a single row or column.', # just 5 consecvtive potatoes
                'check_completion': self.check_level_1_completion,
                'config': 'plain',
                'requires_multiple_test_cases': False, #  false if code is to be run on only one farm instance
                'unlocked': True
            },
            2: { # a pattern.. must be in row or column
                'task': 'Plant 4 carrots and 4 pumpkins in an alternating pattern. eg: carrot, pumpkin, carrot, pumpkin, etc',
                'check_completion': self.check_level_2_completion,
                'config': 'plain', # dirt only
                'requires_multiple_test_cases': False,
                'unlocked': False
            },
            3: { # does not matter orientation; crop count == 10 for each crop type
                'task': 'Plant 10 of each crop type (your entire inventory)',
                'check_completion': self.check_level_3_completion,
                'config': 'grass', #random patches of grass
                'requires_multiple_test_cases': True, # true if level requires multiple test cases to pass
                'unlocked': True
            },
            4: {
                'task': 'Harvest all pumpkins on the farm', 
                'check_completion': self.check_level_4_completion,
                'config': 'crops', # config type with randomly generated crops on dirt farm
                'requires_multiple_test_cases': True,
                'unlocked': True
            },
            5: {
                'task': 'Replace every pumpkin with a carrot', 
                'check_completion': self.check_level_5_completion,
                'config': 'crops',
                'requires_multiple_test_cases': True,
                'unlocked': True
            },
            6: {
                'task': 'find the longest consecutive row or column of dirt and fill it with carrots.',
                'check_completion': self.check_level_6_completion,
                'config': 'grass',
                'requires_multiple_test_cases': True,
                'unlocked': True
            },
            7: {
                'task': 'plant pumpkins along river (in every spot adjacent to a river).',
                'check_completion': self.check_level_7_completion,
                'config': 'tree_river', # river with tree
                'requires_multiple_test_cases': True,
                'unlocked': True
            },
            8: {
                'task': 'plant crops around trees(on every tile adjacent to a tree).',
                'check_completion': self.check_level_8_completion,
                'config': 'tree_dirt', # dirt farm with 3 randomly placed trees
                'requires_multiple_test_cases': True,
                'unlocked': False
            },
            
        }
        self.current_level = 1
        self.load_progress()

    def save_progress(self):
        # Save the current level and unlocked levels to a JSON file
        progress = {
            'current_level': self.current_level,
            'levels': {k: v['unlocked'] for k, v in self.levels.items()}
        }
        with open('level_progress.json', 'w') as file:
            json.dump(progress, file)
            print("Progress saved")

    def load_progress(self):
        # Load saved progress from json file
        try:
            with open('level_progress.json', 'r') as file:
                print("loading progress...")
                progress = json.load(file)
                self.current_level = progress.get('current_level', 1)
                unlocked_levels = progress.get('levels', {})
                for level_str, unlocked in unlocked_levels.items():
                    level = int(level_str)  # Convert level string to int
                    if level in self.levels:
                        self.levels[level]['unlocked'] = unlocked
        except FileNotFoundError:
            # if file does not exist, initialize to default
            print("no saved game found. creating new save")

  
    def get_current_task(self): 
        # returns level objective description
        return self.levels[self.current_level]['task']

    def get_current_config(self): 
        # returns farm config for level
        return self.levels[self.current_level]['config']
    
    def get_test_cases(self): 
        # returns true if level requires multiple test cases
        return self.levels[self.current_level]['requires_multiple_test_cases']

    def is_level_unlocked(self, level_number): 
        # checks if level is unlocked. locked levels are disabled in levelPage
        return self.levels.get(level_number, {}).get('unlocked', False)

    def unlock_next_level(self): 
        # enables next level to be activated
        next_level = self.current_level + 1
        if next_level in self.levels:
            self.levels[next_level]['unlocked'] = True

    def advance_to_next_level(self):
         # advances to next level and unlocks it in levelPage
        self.unlock_next_level()
        self.current_level += 1
        self.save_progress()


    def check_current_level_completion(self, farm_stats): 
            #generic func that passes level specific check function
            check_function = self.levels[self.current_level]['check_completion']
            return check_function(farm_stats)
    
##Level-specific check functions.## 
    def check_level_1_completion(self, farm_stats):
        # Check if 5 potatoes are planted in a row/col
        return farm_stats.check_potatoes_in_row(5)

    def check_level_2_completion(self, farm_stats):
        pass
    
    def check_level_3_completion(self, farm_stats):
        pass
    
    def check_level_4_completion(self, farm_stats):
        pass

    def check_level_5_completion(self, farm_stats):
        pass

    def check_level_6_completion(self, farm_stats):
        pass

    def check_level_7_completion(self, farm_stats):
        pass
    def check_level_8_completion(self, farm_stats):
        pass


        
