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
            2: { # a pattern.. must be in row
                'task': 'Plant 4 carrots and 4 pumpkins in an alternating pattern. eg: carrot, pumpkin, carrot, pumpkin, etc',
                'check_completion': self.check_level_2_completion,
                'config': 'plain', # dirt only
                'requires_multiple_test_cases': False,
                'unlocked': False
            },
            3: { 
                'task': 'plant pumpkins along the river (all dirt tiles adjacent to river).',
                'check_completion': self.check_level_3_completion,
                'config': 'river_horizontal', 
                'requires_multiple_test_cases': False, # true if level requires multiple test cases to pass
                'unlocked': False
            },
            4: {
                'task': 'Once again you must plant pumpkins along the river (all dirt tiles adjacent to river). But this time your code must now pass all 3 randomised farm cases.', 
                'check_completion': self.check_level_4_completion,
                'config': 'river_horizontal', 
                'requires_multiple_test_cases': True,
                'unlocked': False
            },
            5: {
                'task': 'Replace every pumpkin with a carrot', 
                'check_completion': self.check_level_5_completion,
                'config': 'crop_row',
                'requires_multiple_test_cases': True,
                'unlocked': False
            },
            6: {
                'task': 'harvest every crop on the farm.',
                'check_completion': self.check_level_6_completion,
                'config': 'crops', 
                'requires_multiple_test_cases': False,
                'unlocked': False
            },
            7: {
                'task': 'find the longest consecutive row of dirt and fill it with carrots.',
                'check_completion': self.check_level_7_completion,
                'config': 'grass',
                'requires_multiple_test_cases': False,
                'unlocked': False
            },
            8: {
                'task': 'find the longest consecutive row of dirt and fill it with carrots (no hardcoding; several random test cases apply).\n WARNING: you may want to turn slow mode off in settings as the code you write for this level may take a while to run.',
                'check_completion': self.check_level_8_completion,
                'config': 'grass',
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
        if self.current_level != 8:
            self.unlock_next_level()
            self.current_level += 1
            self.save_progress()


    def check_current_level_completion(self, farm_stats): 
        """generic func that passes level specific check function"""
        check_function = self.levels[self.current_level]['check_completion']
        return check_function(farm_stats)
    
###Level-specific check functions. farm_stats is accessed in order to check farm grid state and allow reuse of functions### 
    def check_level_1_completion(self, farm_stats):
        # Check if 5 potatoes are planted in a row/col
        return farm_stats.check_crops_in_row(5,0)

    def check_level_2_completion(self, farm_stats):
        # check for 4 carrots and 4 pumpkins in an alternating pattern.
        return farm_stats.check_alternating_pattern(4)
    
    def check_level_3_completion(self, farm_stats):
        return farm_stats.check_crops_in_row(10,2) and farm_stats.check_crops_adjacent_to_river()

    def check_level_4_completion(self, farm_stats):
        return farm_stats.check_crops_in_row(10,2) and farm_stats.check_crops_adjacent_to_river()
    
    def check_level_5_completion(self, farm_stats):
        if farm_stats.count_crops(2) == 0 and farm_stats.count_total_crops() == 10:
            return True
 
    def check_level_6_completion(self, farm_stats):
        return farm_stats.count_total_crops() == 0
    
    def check_level_7_completion(self, farm_stats):
        longest = farm_stats.longest_dirt_row()
        print("longest dirt row = ",longest)
        return farm_stats.check_crops_in_row(longest,1)
    
    def check_level_8_completion(self, farm_stats):
        longest = farm_stats.longest_dirt_row()
        print("longest dirt row = ",longest)
        return farm_stats.check_crops_in_row(longest,1)

        
