# farmtile.py
class FarmTile:
    tile_desc = {0: "dirt", 1: "grass", 2: "water", 3: "crop", 4: "tree"}

    def __init__(self, x, y, tile_type=0):
        self.tile_type = tile_type
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.tile_desc[self.tile_type])
    
    def get_pos(self):
        return (self.x, self.y)
    
    def is_crop(self):
        return self.tile_type == 3
    
    def get_crop_type(self):
        if self.is_crop():
            return self.crop_type
        return None
class CropTile(FarmTile):
    def __init__(self, x, y, crop_type=0):
        super().__init__(x, y, 3)
        self.crop_type = crop_type

    def get_crop_type(self):
        return self.crop_type