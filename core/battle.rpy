##############################################################################
# BATTLE ALLOCATION DEFINITIONS
#

init -6 python:
    
    class Battle:
        def __init__(self, id, good_team=[], bad_team=[], xpos=0, ypos=0, battle_label='', next_battle_label=''):
            self.id = id
            self.good_team = good_team
            self.bad_team = bad_team
            self.xpos = xpos
            self.ypos = ypos
            self.battle_label = battle_label
            self.next_battle_label = next_battle_label
            self.follow_on = None
            
        def add_good_member(self, player):
            if player not in self.good_team:
                self.good_team.append(player)
            
        def remove_good_member(self, player):
            if player in self.good_team:
                self.good_team.remove(player)
            
        def finished(self):
            """
            Return Boolean, if all enemy HPs total to 0 then return True
            """
            hps = [p.hp for p in self.bad_team]
            
            if sum(hps) > 0:
                return False
                    
            return True
            
        def cleanup(self, other_battles):
            """
            This method is required to clean up this race condition 
            where players are being added to other battles
            """
            iterbattle = [b for b in other_battles if b != self]
            for b in iterbattle:
                for p in b.good_team:
                    if p in self.good_team:
                        b.good_team.remove(p)
            
        def clean_dead_members(self):
            self.bad_team = [p for p in self.bad_team if p.hp > 0]
            self.good_team = [p for p in self.good_team if p.hp > 0]
                    
        def fight(self, stage, win_label='generic_win', lose_label='generic_win', draw_label='generic_win', fight_limit=20):
            
            # Sanity checks
            
            # If no good team or bad team, skip the fight for that battle
            if not self.good_team or not self.bad_team:
                renpy.jump(self.next_battle_label)
                
            bad_hps = [m.hp for m in self.bad_team]
            good_hps = [m.hp for m in self.good_team]
            
            # If all enemies in good or bad team is 0 then skip fight for that battle
            if sum(bad_hps) < 1 or sum(good_hps) < 1:
                renpy.jump(self.next_battle_label)
                
            if len(self.good_team) == 1:
                good_tag = []
            elif len(self.good_team) > 1:
                good_tag = self.good_team[1:]
            else:
                # skip the battle
                renpy.jump(self.next_battle_label)
                
            if len(self.bad_team) == 1:
                bad_tag = []
            elif len(self.bad_team) > 1:
                bad_tag = self.bad_team[1:]
            else:
                # skip the battle
                renpy.jump(self.next_battle_label)
                
            renpy.call('fight', self.good_team[0], self.bad_team[0], good_tag, bad_tag, clearing, win_label, lose_label, draw_label, fight_limit)
