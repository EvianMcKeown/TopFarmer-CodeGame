# levels.py

class Levels:
    def __init__(self): # initialises levels dictionary with data and sets current level to lvl 1
        self.levels = {
            1: {
                'task': 'Plant 5 potatoes in a single row or column.', # just 5 consecvtive potatoes
                'check_completion': self.check_level_1_completion,
                'config': 'plain',
                'unlocked': True
            },
            2: { # a pattern.. must be in row or column
                'task': 'Plant 4 carrots and 4 pumpkins in an alternating pattern. eg: carrot, pumpkin, carrot, pumpkin, etc',
                'check_completion': self.check_level_2_completion,
                'config': 'plain',
                'unlocked': True
            },
            3: { # does not matter orientation; crop count == 10 for each crop type
                'task': 'Plant 10 of each crop type (your entire inventory)',
                'check_completion': self.check_level_3_completion,
                'config': 'grass',
                'unlocked': True
            },
            4: {
                'task': 'Harvest all pumpkins on the farm', 
                'check_completion': self.check_level_4_completion,
                'config': 'crops', # config type with randomly generated crops on dirt farm
                'unlocked': True
            },
            5: {
                'task': 'Replace every pumpkin with a carrot', 
                'check_completion': self.check_level_5_completion,
                'config': 'crops',
                'unlocked': True
            },
            6: {
                'task': 'find the longest consecutive row or column of dirt and fill it with carrots.',
                'check_completion': self.check_level_6_completion,
                'config': 'grass',
                'unlocked': True
            },
            7: {
                'task': 'plant pumpkins along river.',
                'check_completion': self.check_level_7_completion,
                'config': 'tree_river',
                'unlocked': True
            },
            8: {
                'task': 'plant crops around trees(on every tile adjacent to a tree).',
                'check_completion': self.check_level_8_completion,
                'config': 'tree_dirt',
                'unlocked': True
            },
            
        }
        self.current_level = 1

  
    def get_current_task(self): # returns level objective description
        return self.levels[self.current_level]['task']

    def get_current_config(self): # returns farm config for level
        return self.levels[self.current_level]['config']

    def is_level_unlocked(self, level_number): # checks if level is unlocked. locked levels are disabled in levelPage
        return self.levels.get(level_number, {}).get('unlocked', False)

    def unlock_next_level(self): # enables next level to be activated
        next_level = self.current_level + 1
        if next_level in self.levels:
            self.levels[next_level]['unlocked'] = True

    def check_current_level_completion(self, farm_stats): # checks if task is completed
        check_function = self.levels[self.current_level]['check_completion']
        return check_function(farm_stats)

    def check_level_1_completion(self, farm_stats):
        # Check if 5 potatoes are planted in a row
        return farm_stats.check_potatoes_in_row(5)

    def check_level_2_completion(self, farm_stats):
        # Check if 3 carrots and 3 pumpkins are planted
        return (farm_stats.get_carrots_planted() >= 3 and
                farm_stats.get_pumpkins_planted() >= 3)
    
    def check_level_3_completion(self, farm_stats):
        # 'Plant 3 carrots and harvest 2 of em
        return (farm_stats.get_carrots_planted() >= 3 and
                farm_stats.get_pumpkins_harvested() == 2)
    
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

    def advance_to_next_level(self): # advances to next level and unlocks it in levelPage
        self.unlock_next_level()
        self.current_level += 1
        
