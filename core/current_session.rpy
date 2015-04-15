##############################################################################
# CURRENT SESSION DEFINITIONS
#

init -5 python:
    
    class CurrentSession:
        """
        This used to store information about recent actions (since renpy does 
        not have a call action for screens and jumps don't take params)
        """
        def __init__(self):
            self.main_player = None
            self.location = None
            self.village = None
            self.limb = None
            self.tile = None
            self.mission = None
            self.mission_rank = None
            self.skill = None
            self.skill_type = None
            self.item = None
            self.time_to_advance = {'hours': 0, 'days': 0, 'months': 0, 'years': 0}
            self.enemy_tag = []
            self.player_tag = []
            self.stage = None
            self.win_label = None
            self.lose_label = None
            self.draw_label = None
            self.fight_limit = 0
            self.last_match_result = None
            self.initial_pos = True
            self.rest = False
            self.spar = []
            self.battles = []
            self.team = None
            self.team_store = None
            self.battle = None
            self.battle_follow_on = None
            self.battle_outcome = 'loss'
            
        def clear(self):
            self.main_player = None
            self.location = None
            self.village = None
            self.limb = None
            self.tile = None
            self.mission = None
            self.mission_rank = None
            self.item = None
            self.skill = None
            self.skill_type = None
            self.enemy_tag = []
            self.player_tag = []
            self.stage = None
            self.win_label = None
            self.lose_label = None
            self.draw_label = None
            self.fight_limit = 0
            self.last_match_result = None
            self.initial_pos = True
            self.rest = False
            self.spar = []
            self.battles = []
            self.team = None
            self.team_store = None
            self.battle = None
            self.battle_follow_on = None
            self.battle_outcome = 'loss'
            
        def clear_time_to_advance(self):
            self.rest = False
            self.time_to_advance = {'hours': 0, 'days': 0, 'months': 0, 'years': 0}
            
        def time_to_advance_in_days(self):
            days = 0
            
            if self.time_to_advance.get('hours'):
                days += self.time_to_advance['hours'] / 24
            
            if self.time_to_advance.get('days'):
                days += self.time_to_advance['days']
                
            if self.time_to_advance.get('months'):
                days += self.time_to_advance['months'] * 30
                
            if self.time_to_advance.get('years'):
                days += self.time_to_advance['years'] * 365
                
            return days