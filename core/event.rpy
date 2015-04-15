##############################################################################
# EVENT DEFINITIONS
#

init -8 python:

    from datetime import date, timedelta
    
    ALL_EVENTS = []
    
    class Event:
        """
        These events will show up on the calendar
        start takes tuple e.g. (day, month)
        finish takes tuple e.g. (day, month)
        frequency takes tuple e.g. (day1, day2, day3) e.g. (1, 14, 30) event will happen on 1st, 14th and 30th of month
        chance takes a float e.g. 0.1 (10% chance of event happening)
        """
        def __init__(self, name, small_name, start=None, finish=None, frequency=None, chance=None, label=None, 
                     occurrence=None, npc=None, npc_icon=None):
            self.name = name
            self.small_name = small_name
            self.start = start
            self.finish = finish
            self.frequency = frequency
            self.chance = chance
            self.label = label
            self.location = None
            self.character = None
            self.active = False
            self.occurrence = occurrence # how many times it happens during a day
            self.npc = npc
            self.npc_icon = npc_icon
            self.count = 1
            self.stop = False
            
        def date_range(self, game_time):
            if self.start and self.finish:
                d1 = date(game_time.year,self.start[1],self.start[0])
                d2 = date(game_time.year,self.finish[1],self.finish[0])
                dd = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]
                return dd
            
        def check_active(self, game_time):
            """
            Check is the event is happening now, if it is jump to event label
            """
            if self.start and self.finish:
                if self.start < date(game_time.day, game_time.month) < self.finish:
                    self.active = True
                    if self.label:
                        renpy.call(self.label)
                else:
                    self.active = False
            elif game_time.day in self.frequency:
                self.active = True
                if self.label:
                    renpy.call(self.label)
            else:
                if renpy.random.randint(1, 100) < 100 * self.chance:
                    if self.label:
                        renpy.call(self.label)