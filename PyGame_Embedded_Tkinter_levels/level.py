# levels.py

class Levels:
    def __init__(self):
        self.levels = {
            1: {
                'task': 'Plant 5 potatoes in a row',
                'check_completion': self.check_level_1_completion,
                'config': 'plain',
                'unlocked': True
            },
            2: {
                'task': 'Plant 3 carrots and 3 pumpkins',
                'check_completion': self.check_level_2_completion,
                'config': 'grass',
                'unlocked': False
            },
            3: {
                'task': 'Plant 3 carrots and harvest 2',
                'check_completion': self.check_level_3_completion,
                'config': 'river',
                'unlocked': True
            },
            # Add more levels as needed
        }
        self.current_level = 1

    def get_current_task(self):
        return self.levels[self.current_level]['task']

    def get_current_config(self):
        return self.levels[self.current_level]['config']

    def is_level_unlocked(self, level_number):
        return self.levels.get(level_number, {}).get('unlocked', False)

    def unlock_next_level(self):
        next_level = self.current_level + 1
        if next_level in self.levels:
            self.levels[next_level]['unlocked'] = True

    def check_current_level_completion(self, farm_stats):
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

    def advance_to_next_level(self):
        self.unlock_next_level()
        self.current_level += 1
        
