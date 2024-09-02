
#dict for levels with their task criteria and check
levels = [
    {
        "task": "Plant 3 potatoes in a row.",
        "check": lambda farm: check_lvl_1(farm, 3, 'potato')
    },
    {
       "task": "Plant 2 carrots in a row.",
        "check": lambda farm: check_lvl_2(farm, 2, 'carrot')
    },
]

#each level gets separate check methods
def check_lvl_1(farm, count, crop):
    for y in range(10):
        count = 0
        for x in range(10):
            if farm.grid[x][y].crop_type == 0:  # 0 for potato
                count += 1
                if count == 3:
                    return True
            else:
                count = 0
    return False

def check_lvl_2(farm,count,crop):
    for y in range(10):
        count = 0
        for x in range(10):
            if farm.grid[x][y].crop_type == 1:  # 1 for carrot
                count += 1
                if count == 3:
                    return True
            else:
                count = 0
    return False