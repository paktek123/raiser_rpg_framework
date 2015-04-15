##############################################################################
# GAMETIME DEFINITIONS
#

init -9 python:
    import random
    import copy
    
    class GameTime:
        def __init__(self, hour, day, month, year):
            self.minute = 5
            self.hour = hour
            self.day = day
            self.month = month
            self.year = year
            self.months = ["Stub", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
            self.counter = 0
            self.current_time = self.now()
            
        def now(self):
            if self.counter == 2:
                self.counter = 0
                self.advance_time(minutes=1)
            else:
                self.counter += 1
            return "{}:{} {} {} {}".format(str(self.hour).zfill(2), str(self.minute).zfill(2), self.day, self.months[self.month], self.year)
            
        def dawn(self):
            minute = random.randint(0, 59)
            self.hour = random.randint(1,5)
            return "{}:{} {} {} {}".format(self.hour, minute, self.day, self.months[self.month], self.year)
            
        def morning(self):
            minute = random.randint(0, 59)
            self.hour = random.randint(6,11)
            return "{}:{} {} {} {}".format(self.hour, minute, self.day, self.months[self.month], self.year)
            
        def afternoon(self):
            minute = random.randint(0, 59)
            self.hour = random.randint(12,17)
            return "{}:{} {} {} {}".format(self.hour, minute, self.day, self.months[self.month], self.year)
            
        def evening(self):
            minute = random.randint(0, 59)
            self.hour = random.randint(18,20)
            return "{}:{} {} {} {}".format(self.hour, minute, self.day, self.months[self.month], self.year)
            
        def night(self):
            minute = random.randint(0, 59)
            self.hour = random.randint(21,23)
            return "{}:{} {} {} {}".format(self.hour, minute, self.day, self.months[self.month], self.year)
            
        def next_month(self):
            if self.month > 11:
                self.year += 1
                self.month = 1
            else:
                self.month += 1
            
        def next_day(self):
            if self.day > 29:
                self.next_month()
                self.day = 1
            else:
                self.day += 1
                
        def next_hour(self):
            if self.hour > 23:
                self.next_day()
                self.hour = 1
            else:
                self.hour += 1
                
        def next_minute(self):
            if self.minute > 59:
                self.next_hour()
                self.minute = 1
            else:
                self.minute += 1
                
        def advance_time(self, minutes=0, hours=0, days=0, months=0, years=0):
            
            if minutes:
                while minutes > 0:
                    minutes -= 1
                    self.next_minute()
            
            if hours:
                while hours > 0:
                    hours -= 1
                    self.next_hour()
            
            if days:
                while days > 0:
                    days -= 1
                    self.next_day()
                
            if months:
                while months > 0:
                    months -= 1
                    self.next_month()
                    
            self.current_time = self.now()
            
    class Month:
        def __init__(self, number, days=[]):
            self.number = number 
            self.days = []
            
        def __repr__(self):
            return "Month: {}".format(self.number)
            
    class Day:
        def __init__(self, number, month, events=[]):
            self.number = number
            self.events = events
            self.month = month
            
        def parse_events(self):
            """
            Return events for a day (comma delimited)
            """
            if self.events:
                names = [e.small_name for e in self.events]
                return ', '.join(names)
            else:
                return ' '
            
        def __repr__(self):
            return "Day: {}".format(self.number)
            
    ### TIME, DAY AND MONTHS ###
    months = [copy.deepcopy(Month(m)) for m in range(1,13)]
    
    def get_month(number):
        if number == 13:
            number = 1
        elif number == 0:
            number = 12
        
        return [m for m in months if m.number == number][0]
        
    def get_current_month():
        return [m for m in months if m.number == main_time.month][0]
        
    def get_today(game_time):
        return [d for d in ALL_DAYS if d.number == game_time.day and d.month.number == game_time.month][0]
    
    for m in months:
        m.days = [copy.deepcopy(Day(d, m)) for d in range(1,31)]
        
    ALL_DAYS = []
    
    for m in months:
        ALL_DAYS += m.days