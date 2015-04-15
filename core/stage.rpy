##############################################################################
# STAGE DEFINITIONS
#

init -3:
    image clearing_base_texture = im.Scale("tile.png", 50, 30)
    image clearing_active_texture = im.Scale("tileh.png", 50, 30)
    image clearing_project_texture = im.Scale("tilep.png", 50, 30)
    image clearing_trap_texture = im.Scale("tiletrap.png", 50, 30)
    
    image forest_base_texture = im.Scale("tile_grass.png", 50, 30)

init -3 python:
    class Stage:
        """
        Define base textures for tiles and generate the tiles
        """
        def __init__(self, name, pull, range, 
                     base_texture="clearing_base_texture", active_texture="clearing_active_texture", 
                     project_texture="clearing_project_texture", trap_texture="clearing_trap_texture"):
            self.name = name
            self.pull = pull
            self.range = range
            self.base_texture = base_texture
            self.active_texture = active_texture
            self.project_texture = project_texture
            self.trap_texture = trap_texture
            self.tiles = []
            self.tile1 = Tile(1, tile1pos, self.base_texture, self.active_texture, self.trap_texture, self.project_texture, self)
            self.tile2 = Tile(2, tile2pos, self.base_texture, self.active_texture, self.trap_texture, self.project_texture, self)
            self.tile3 = Tile(3, tile3pos, self.base_texture, self.active_texture, self.trap_texture, self.project_texture, self)
            self.tile4 = Tile(4, tile4pos, self.base_texture, self.active_texture, self.trap_texture, self.project_texture, self)
            self.tile5 = Tile(5, tile5pos, self.base_texture, self.active_texture, self.trap_texture, self.project_texture, self)
            self.tile6 = Tile(6, tile6pos, self.base_texture, self.active_texture, self.trap_texture, self.project_texture, self)
            self.tile7 = Tile(7, tile7pos, self.base_texture, self.active_texture, self.trap_texture, self.project_texture, self)
            self.tile8 = Tile(8, tile8pos, self.base_texture, self.active_texture, self.trap_texture, self.project_texture, self)
            self.tile9 = Tile(9, tile9pos, self.base_texture, self.active_texture, self.trap_texture, self.project_texture, self)
            self.tile10 = Tile(10, tile10pos, self.base_texture, self.active_texture, self.trap_texture, self.project_texture, self)
            self.tile11 = Tile(11, tile11pos, self.base_texture, self.active_texture, self.trap_texture, self.project_texture, self)
            self.tile12 = Tile(12, tile12pos, self.base_texture, self.active_texture, self.trap_texture, self.project_texture, self)
            self.tiles = [self.tile1, self.tile2, self.tile3, self.tile4, self.tile5, self.tile6, 
                          self.tile7, self.tile8, self.tile9, self.tile10, self.tile11, self.tile12]
            
        def remove_chakra(self):
            return self.pull + renpy.random.randint(-1, self.range)