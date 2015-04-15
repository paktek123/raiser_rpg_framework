##############################################################################
# EVENT DEFINITIONS
#

init -7 python:

    class Mission(object):
        def __init__(self, name, hours=0, days=0, months=0, rank="D", dialogue=[], fights=None):
           self.name = name
           self.hours = hours
           self.days = days
           self.months = months
           self.dialogue = dialogue
           self.rank = rank
           self.success = False
           self.fights = fights
           self.REWARDS = {"D": {'ryo': 5000, 'exp': 50},
                           "C": {'ryo': 30000, 'exp': 150},
                           "B": {'ryo': 150000, 'exp': 450},
                           "A": {'ryo': 450000, 'exp': 1000},
                           "S": {'ryo': 1000000, 'exp': 10000}}
           
        def reward(self, player, half=False):
            exp_reward = renpy.random.randint(0, self.REWARDS[self.rank]['exp']) + self.REWARDS[self.rank]['exp']
            ryo_reward = renpy.random.randint(0, self.REWARDS[self.rank]['ryo']) + self.REWARDS[self.rank]['ryo']
            
            if half:
                exp_reward = exp_reward / 2
                ryo_reward = ryo_reward / 2
            
            player.gain_exp(exp_reward)
            player.ryo += ryo_reward
            
            return {'exp': exp_reward, 'ryo': ryo_reward}
    
    class BasicMission(Mission):
        """
        No fighting just advance time with current background
        One line of dialogue, Rank D
        Mission cannot fail
        Dialogue Structure = [('character', "I say this")]
        """
        def __init__(self, name, hours=0, days=0, months=0, rank="D", dialogue=[("char", "Time to do {}")]):
            super(self.__class__, self).__init__(name, hours, days, months, rank, dialogue)
            
        def do_mission(self, player, village, dest_village=None):
            for p, d in self.dialogue:
                renpy.say(player.character, d.format(self.name))
                
            # chance of injury to the player
            player.injury_chance(0.05)
            main_time.advance_time(hours=self.hours, days=self.days)
            self.success = True
            self.reward(player)
            # clear the mission because it does not need to carry on
            current_session.mission = None
            show_village_map(village, player)
            
    class LabelMission(Mission):
        """
        Jumps to label
        """
        def __init__(self, name, label, hours=0, days=0, months=0, rank="D", dialogue=[("char", " ")], location=None):
            super(self.__class__, self).__init__(name, hours, days, months, rank, dialogue)
            self.label = label
            self.location = location
            
        def do_mission(self, player, village, dest_village=None):
            # advance time
            main_time.advance_time(hours=self.hours, days=self.days)
            renpy.call(self.label)
            # handle reward and redirect in label ^^^
            
    class SimpleFightMission(Mission):
        """
        Travel to a destination and fight an enemy
        BETA, do not use
        Many lines of dailogue, Rank C/D
        Mission can fail / failure is either death or half exp
        Dialogue Structure = [('character', "I say this")]
        Fights = {'stage': someplace, 
                  'win_label': win_label, 
                  'lose_label': lose_label, 
                  'enemy': enemy_character, 
                  'tag': [enemy_tag_1, enemy_tag_2]}
        """
        def __init__(self, name, hours=0, days=0, months=0, rank="D", dialogue=[("char", " ")], fights={}, background=None, location=None):
            super(self.__class__, self).__init__(name, hours, days, months, rank, dialogue, fights)
            self.background = None
            self.location = None
            
        def do_mission(self, player, from_village, dest_village):
            if self.background:
                renpy.show(self.background)
            
            # advance time
            if self.days:
                main_time.advance_time(hours=self.hours, days=self.days)
            else:
                main_time.advance_time(hours=self.hours, days=time_between_village(from_village, dest_village))
            if player.team:
                player_team = player.team.members() 
            else:
                player_team = []
            renpy.show(dest_village.random_mission_location())
            for p, d in self.dialogue:
                renpy.say(p.character, d)
            renpy.call('fight', player, self.fights['enemy'], player_team, self.fights['tag'], self.fights['stage'], self.fights['win_label'], self.fights['lose_label'])
            
            if current_session.last_match_result == 'win':
                self.success = True
            
            # this maybe useless
            if self.success:
                self.reward(player)
            else:
                self.reward(player, half=True)
            show_village_map(from_village, player)

    class BattleMission(Mission):
        def __init__(self, name, hours=0, days=0, months=0, rank="D", good_team=[], 
                     battles={'1':[], '2':[], 'last':[]}, follow_on=None, all_battles=[], background=None):
            super(self.__class__, self).__init__(name, hours, days, months, rank, [], [])
            self.good_team = good_team
            self.battles = battles
            self.follow_on = follow_on
            self.all_battles = ALL_BATTLES
            self.background = background

        def do_mission(self, player):
            renpy.hide_screen('battle_selection_screen')
            renpy.hide_screen('battle_prep_screen')

            if self.background:
                renpy.hide(self.background)
                renpy.show(self.background)

            current_session.team = self.good_team

            battle_data = []
            for battle in self.all_battles:
                if self.battles.get(battle.id):
                    battle.bad_team = self.battles[battle.id]
                    battle_data.append(battle)

            current_session.battles = battle_data
            current_session.battle_follow_on = self.follow_on
            renpy.call('battle_choose')
            
    def get_character(name):
        for player in ALL_PLAYERS:
            if player.name.lower() == name:
                return player.character
                
    class MultiPartMission(Mission):
        """
        BETA, not ready yet
        Travel to destinations and fight an enemy
        Many lines of dailogue, Rank C/B/A/S
        Mission can fail / failure is either death or half exp
        Dialogue Structure = [('character', 'name', "I say this"),
                              ('fight', 1),
                              ('sprite', 'show image name'),
                              ('scene', "image name"),
                              ('screen', "call a screen"),
                              ('time', 12),
                              ('mission', "last_match|success")]
        Fights = [('stage': someplace, 
                  'win_label': win_label, 
                  'lose_label': lose_label, 
                  'enemy': enemy_character, 
                  'tag': [enemy_tag_1, enemy_tag_2],
                  'number': 1}]
        """
        def __init__(self, name, hours=0, days=0, months=0, rank="D", dialogue=[("char", " ")], fights=[]):
            super(self.__class__, self).__init__(name, hours, days, months, rank, dialogue, fights)
            
        def evaluate_function(self, function, player, village):
            if function[0] == 'character':
                # TODO: get_character does not exist yet
                renpy.say(get_character(function[1]), function[2])
            elif function[0] == 'fight':
                if player.team:
                    player_team = player.team.members() 
                else:
                    player_team = []
                fight = [f for f in self.fights if f['number'] == function[1]][0]
                renpy.call('fight', player, fight['enemy'], player_team, fight['tag'], fight['stage'], fight['win_label'], fight['lose_label'])
                
            elif function[0] == 'sprite':
                renpy.show(function[1])
                
            elif function[0] == 'scene':
                renpy.show(function[1])
                
            elif function[0] == 'screen':
                renpy.show_screen(function[1], player, screen)
                
            elif function[0] == 'time':
                 main_time.advance_time(hours=function[1])
                
            elif function[0] == 'mission':
                if function[1] == 'success':
                    self.success = True
                elif function[1] == 'last_match':
                    if current_session.last_match_result == 'win':
                        self.success = True
                    else:
                        self.success = False
            
        def do_mission(self, player, from_village, dest_village):
            # advance time
            main_time.advance_time(hours=self.hours, days=time_between_village(from_village, dest_village))
            for function in dialogue:
                self.evaluate_function(function)
            
            # this maybe useless
            if self.success:
                self.reward(player)
            else:
                self.reward(player, half=True)
            show_village_map(from_village, player)