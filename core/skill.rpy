##############################################################################
# SKILL DEFINITIONS
#

init -2 python:

    class Skill(object):
        def __init__(self, name, skill_type, label, range, tech=0, chakra_cost=0, damage=0, 
                     stun=False, duration=None, exp=0, unlock_exp=0, limbs=[]):
            self.name = name
            self.skill_type = skill_type
            self.label = label
            self.range = range
            self.tech = tech
            self.exp = exp
            self.unlock_exp = unlock_exp
            self.chakra_cost = chakra_cost
            self.damage = damage 
            self.stun = stun
            self.duration = duration
            self.used = 0
            self.active = False
            self.limbs = limbs
            
        def set_to_default(self):
            self.active = False
            self.tech = 0
            self.exp = 0
            
        def unlock(self, player):
            player.assign_skill(self)
            
        def unusable_reason(self, player, enemy):
            if not self.is_chakra_requirement_met(player):
                return 'Not enough MP.'
                
            if not self.is_within_range(player, enemy):
                return "Out of range, must be within {}.".format(self.range)
                
            if not self.is_unlocked():
                return "Skill is learnt but not cannot be used in combat, can be unlocked by training."
                
            if not self.has_quantity(player):
                return "Weapon not in inventory."
            
        def is_usable(self, player, enemy):
            if self.is_chakra_requirement_met(player) and self.is_within_range(player, enemy) and self.is_unlocked() and self.has_quantity(player):
                return True
            return False
            
        def has_quantity(self):
            """
            Applies to weapons only
            """
            if hasattr(self, 'quantity'):
                if self.quantity > 0:
                    return True
            return False
            
        def is_chakra_requirement_met(self, player):
            if player.chakra > self.chakra_cost:
                return True
            return False
            
        def is_within_range(self, player, enemy):
            if self.range >= abs(player.tile.position - enemy.tile.position):
                return True
            return False
            
        def is_unlocked(self):
            if self.exp == self.unlock_exp:
                return True
            return False
            
        def gain_exp(self, exp):
            self.exp += exp
            if self.exp >= self.unlock_exp:
                self.exp = self.unlock_exp
                # assign the skill to player
                self.unlock(current_session.main_player)
            return self.exp
            
        def activate(self):
            self.active = True
            
        def deactivate(self):
            self.active = False
            
        def action(self, player, enemy):
            
            injured_limbs = player.get_injured_limbs()
            severity_scale = [limb.injury_severity for limb in player.injured_limbs()]
            
            if injured_limbs:
                if (sum(severity_scale) / len(severity_scale)) > 2:
                    renpy.say(player.character, "I can't do anymore moves, I am too injured.")
                    return
                else:
                    renpy.say(player.character, "I am injured but I will still use the skill, it will make my injury worse.")
                    player.increase_limbs_severity(injured_limbs)
                
            # this is for enemy moves mainly
            if player.chakra < self.chakra_cost:
                renpy.say(player.character, "I don't have enough chakra")
                return
                
            if self.stun:
                self.stun_enemy(enemy)
            
            if self.hit_successful(player, enemy):
                renpy.say(player.character, "{}".format(self.name))
                self.deal_damage(player, enemy)
                enemy.fix_stats()
                player_bleed(enemy)
            else:
                renpy.say(player.character, "{} dodges my attack.".format(enemy.name))
                
            player.chakra -= self.chakra_cost
            player.fix_stats()
            self.tech += 1
            return
            
        def apply(self):
            self.activate()
            
        def remove(self):
            self.deactivate()
                
        def append_to_skill(self):
            self.used += 1
            
        def deal_damage(self, player, target, dialogue=True):
            
            self.append_to_skill()
            
            damage = (self.damage - target.defence) + self.tech
            
            if check_active_skill(target, "damagereduction"):
                damage = damage - (target.hp * 0.1)
                target.damagereduction.used += 1
                
            if check_active_skill(target, "chakradefence"):
                damage = damage - (target.chakra * 0.1)
                target.chakradefence.used += 1
                            
            if check_active_skill(player, "dampen"):
                damage = damage * 0.5
                target.dampen.used += 1
                
            if check_active_skill(target, "reflect"):
                if dialogue:
                    renpy.say(target.character, "Reflect!".format(target.name))
                    
                damage = int((self.damage - player.defence)) 
                player.hp -= damage
                target.reflect.used += 1
                target.damage_dealt = damage
                return damage
            elif check_active_skill(target, "ignore"):
                if dialogue:
                    renpy.say(target.character, "Your skills won't affect me!".format(target.name))
                damage = 0
                target.ignore.used += 1
            else:
                # only offensive skills
                if self.skill_type in ('ranged', 'melee', 'weapon', 'special', 'attack'):
                    target.hp -= int(damage)
                    player.damage_dealt = int(damage)
                    
            return damage
            
           
        def hit_successful(self, player, enemy):
            hit_rate = player.base_hit_rate + self.tech - (enemy.evasion * enemy.speed)
            #renpy.say(player.character, "Hit rate is {}".format(hit_rate)) # uncomment this to see hit rate
            if renpy.random.randint(1, 100) <= hit_rate:
                return True
            else:
                return False
                
        def stun_enemy(self, enemy):
            enemy.stunned = True
            return 
            
        def __repr__(self):
            return "Skill: {} {}".format(self.skill_type, self.name)
            
    class Weapon(Skill):
        def __init__(self, name, price, range, chakra_cost,  damage=0, stun=False, duration=None, element=None, tech=0, quantity=1, image=None):
            super(self.__class__, self).__init__(name, 'weapon', name.lower(), range, tech, chakra_cost, damage, stun, duration)
            self.price = price
            self.element = element
            self.tech = tech
            self.quantity = quantity # this is set to 1 by default, so if assigned to player they can use once
            self.image = image
            
        def half_price(self):
            self.price = self.price / 2
            
        def double_price(self):
            self.price = self.price * 2
            
        def __repr__(self):
            return "<Weapon: {} {}>".format(self.name, self.quantity)
            
    def check_active_skill(player, skillname):
        try:
            skill = getattr(player, skillname)
            if skill.active:
                return True
            else:
                return False
        except AttributeError as e:
            return False