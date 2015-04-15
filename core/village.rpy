##############################################################################
# VILLAGE AND LOCATION DEFINITIONS
#

init -6 python:
    
    import random
    class Village:
        def __init__(self, id, name, leader, marker_xpos, marker_ypos, map, wealth=100, army=1000, 
                     locations=None, village_tag='', mission_locations=1):
            
            self.id = id
            self.name = name
            self.leader = leader
            self.army = army
            self.wealth = wealth
            self.marker_xpos = marker_xpos
            self.marker_ypos = marker_ypos
            self.marker_position = Position(xpos=marker_xpos, ypos=marker_ypos)
            self.map = map
            self.wealth_change = 0
            self.original_value = 0
            self.locations = locations
            self.mission_locations = ["{}_{}".format(village_tag, x) for x in range(1,mission_locations+1)]

        def random_mission_location(self):
            return random.choice(self.mission_locations)
            
        def random_wealth_event(self):
            change = renpy.random.randint(-10, 10)
            add_say = ["Many missions completed", "Taxes are raised", "Feudal Lord is feeling generous", "It rains money!", "Not many expenses",
                       "Economy is improving", "Wealth is compounding", "Negotiations are increasing", "Merchants are trading more"]
            minus_say = ["Economy is doing bad", "Not many missions are coming through", "Tax are decreased", "Feudal lord is unhappy", 
                         "Expenses have gone up", "Bad negotiations are failing", "Recession is underway", "Corrupt leader stole wealth and left"]
            
            self.original_wealth = self.wealth
            self.wealth += change
            self.wealth_change = change
            
            if change < 0:
                renpy.say(self.leader.character, "Gang members decreased by {}, total is {}.".format(change, self.wealth))
            else:
                renpy.say(self.leader.character, "Gang members increased by {}, total is {}.".format(change, self.wealth))
            
        def random_event(self):
            renpy.show("world_marker", [ self.marker_position ])
            self.random_wealth_event()
            
        def __repr__(self):
            return "<Village>: {}".format(self.name)
            
    class Location:
        def __init__(self, name, label, background=None, events=[], map_pic_idle=None, map_pic_hover=None, npc=[], visits=0):
            self.name = name
            self.label = label
            self.background = background
            #self.village = village
            self.events = events
            self.map_pic_idle = map_pic_idle
            self.map_pic_hover = map_pic_hover
            self.npc = npc
            self.visits = visits
            self.unlocked = False
            
        def interact(self, player, village):
            renpy.call(self.label, player, village)
            
    import math
    def time_between_village(village1, village2):
        distance = math.sqrt( (village1.marker_xpos - village2.marker_xpos)**2 + (village1.marker_ypos - village2.marker_ypos)**2 )
        time_weeks = abs(distance / 0.1)
        days = time_weeks * 7
        return int(days/4)
        
    
            