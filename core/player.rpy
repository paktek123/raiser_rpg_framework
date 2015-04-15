##############################################################################
# PLAYER, TEAM AND LIMB DEFINITIONS
#

init -4:
    image body = im.Scale("misc/body.png", 100, 150)
    image left_arm_normal = "misc/arm.png"
    image right_arm_normal = im.Flip("misc/arm.png", horizontal=True)
    image left_leg_normal = "misc/leg.png"
    image right_leg_normal = im.Flip("misc/leg.png", horizontal=True)
    image torso_normal = "misc/torso.png"
    image head_normal = "misc/head.png"
    image left_arm_injured = LiveComposite((25, 55), (0, 0), anim.Blink(im.Scale("misc/arm.png", 25, 55)))
    image right_arm_injured = LiveComposite((25, 55), (0, 0), anim.Blink(im.Flip(im.Scale("misc/arm.png", 25, 55), horizontal=True)))
    image left_leg_injured = LiveComposite((30, 60), (0, 0), anim.Blink(im.Scale("misc/leg.png", 30, 60)))
    image right_leg_injured = LiveComposite((30, 60), (0, 0), anim.Blink(im.Flip(im.Scale("misc/leg.png", 30, 60), horizontal=True)))
    image torso_injured = LiveComposite((35, 55), (0, 0), anim.Blink(im.Scale("misc/torso.png", 35, 55)))
    image head_injured = LiveComposite((45, 30), (0, 0), anim.Blink(im.Scale("misc/head.png", 45, 30)))

init -4 python:
    import random
    import copy
    
    INJURY_LEVELS = {1: "minor", 
                     2: "significant", 
                     3: "major",
                     4: "crippled",
                     5: "crippled",
                     6: "crippled",
                     7: "crippled",
                     0: "none"}
    
    # in days
    INJURY_LENGTH = {1: 3, 2: 7, 3: 30, 4: 90, 5: 360}
    
    class Limb:
        def __init__(self, name):
            self.name = name
            self.bleeding = False
            self.crippled = False
            self.cripple_count = 0
            self.injury = False
            self.injury_severity = 0
            self.injury_count = 0
            self.injury_length = 0
            self.days_rested = 0
            
        def bleed(self):
            self.bleeding = True
            self.cripple_count += 1
            
        def stop_bleeding(self):
            self.bleeding = False
            
        def cripple(self):
            if self.cripple_count > 5:
                self.crippled = True
                
        def injure(self):
            self.injury_severity += 1
            self.injury = True
            # it can't go above 5
            if self.injury_severity > 5:
                self.injury_severity = 5
            self.injury_length = INJURY_LENGTH[self.injury_severity]
            
        def rest(self, days):
            if self.injury:
                self.days_rested += days
                if self.days_rested >= self.injury_length:
                    self.heal_injury(full=True)
            
        def heal_injury(self, full=True):
            if full:
                self.injury_severity = 0
                self.injury = False
                self.injury_length = 0
                self.days_rested = 0
                self.bleeding = False
                self.cripple_count = 0
            else:
                self.injury_severity -= 1
                self.injury_length = INJURY_LENGTH[self.injury_severity]
            
            if self.injury_severity < 1:
                self.injury = False
                
        def heal_percentage(self):
            return (self.days_rested / self.injury_length) * 100 
            
    limb_head = Limb('head')
    limb_torso = Limb('torso')
    limb_left_arm = Limb('left_arm')
    limb_right_arm = Limb('right_arm')
    limb_left_leg = Limb('left_leg')
    limb_right_leg = Limb('right_leg')
    
    LIMBS = [limb_head, limb_torso, limb_left_arm, limb_right_arm, limb_left_leg, limb_right_leg]
    
    class Team:
        def __init__(self, name, sensei=None, members=[], chemistry=0):
            self.name = name
            self.sensei = name
            self.members = members
            self.chemistry = chemistry
            
        def add_member(self, new_member):
            self.members.append(new_member)
            
        def remove_member(self, old_member):
            self.members.remove(old_member)
            
        def increase_chemistry(self, exp):
            self.chemistry += exp
            return self.chemistry
            
        def decrease_chemistry(self, exp):
            # this can go negative
            self.chemistry -= exp
            
            
    # D - Level 1 - 10 
    # C - Level 11 - 20
    # B - Level 21 - 30
    # A - Level 31 - 40
    # S - Level 41 +
    LEVELS = {level: level*100 for level in range(1,100)}
    MAX_BOND = 100

    class Player(object):
        def __init__(self, name, picname, character, tilepic, hudpic, hp, maxhp, chakra, maxchakra, 
                     strength, speed, evasion, defence, stamina, base_hit_rate, tile=None, facing='left',
                     meleeskills=[], specialskills=[], rangedskills=[], items=[], defensiveskills=[], bloodlineskills=[],
                     leader_pic=None, melee=1, special=1, ranged=1, weapons=[], battle_ai=[], home_village=None, level=1,
                     interaction={}):
            
            self.name = name
            self.picname = picname
            self.character = character
            self.tilepic = tilepic
            self.hudpic = hudpic
            self.hp = hp
            self.maxhp = maxhp
            self.chakra = chakra
            self.maxchakra = maxchakra
            self.strength = strength
            self.speed = speed
            self.evasion = evasion
            self.defence = defence
            self.stamina = stamina
            self.base_hit_rate = base_hit_rate
            self.melee = melee
            self.special = special
            self.ranged = ranged
            self.tile = tile # position 
            self.facing = facing
            self.meleeskills = meleeskills
            self.specialskills = specialskills
            self.rangedskills = rangedskills
            self.items = items
            self.weapons = weapons
            self.defensiveskills = defensiveskills
            self.bloodlineskills = bloodlineskills
            self.all_skills = self.meleeskills + self.specialskills + self.rangedskills + self.items + self.defensiveskills + self.bloodlineskills + self.weapons
            self.action_counter = 0
            self.battlescreen = None
            self.stunned = False
            self.counter_state = False
            self.head = copy.deepcopy(limb_head)
            self.torso = copy.deepcopy(limb_torso)
            self.left_arm = copy.deepcopy(limb_left_arm)
            self.right_arm = copy.deepcopy(limb_right_arm)
            self.left_leg = copy.deepcopy(limb_left_leg)
            self.right_leg = copy.deepcopy(limb_right_leg)
            self.blood = 100
            self.max_blood = 100
            self.damage_dealt = 0
            self.main = False
            self.exp = 0
            self.level = level
            self.allocation_points = 0
            self.leader_pic = leader_pic
            self.team = None
            self.sensei = None
            self.bond = 0
            self.ryo = 2000
            self.battle_ai = battle_ai
            self.home_village = home_village
            self.interaction = interaction
            self.npc_event = None
            
            self.assign_all_skills()
            self.set_sensei()
            self.generate_events_for_interaction()
            
        def full_heal(self):
            self.hp = self.maxhp
            self.chakra = self.maxchakra
            self.heal_all_injuries()
            
        def generate_events_for_interaction(self):
            # this will jump to label called for Sasuke Uchiha sasuke_uchiha1, 1 is number of visits
            data = {'name': self.name, 
                    'small_name': "NPC", 
                    'start': None, 
                    'finish': None, 
                    'frequency': None, 
                    'chance': None,
                    'label': self.name.replace(' ', '_').lower() + "{}",
                    'occurrence': None,
                    'npc': self,
                    'npc_icon': None}
            data.update(self.interaction)
            new_event = Event(**data)
            self.npc_event = new_event
            ALL_EVENTS.append(new_event)
            
        def heal_all_injuries(self):
            for limb in self.get_limbs():
                limb.heal_injury(full=True)
            
        def get_injury_bill(self):
            price = 0
            stay_days = 0
            for limb in self.get_limbs():
                if limb.injury_severity == 1:
                    price += 1000
                    stay_days += 3
                elif limb.injury_severity == 2:
                    price += 2000
                    stay_days += 7
                elif limb.injury_severity == 3:
                    price += 4000
                    stay_days += 14
                elif limb.injury_severity > 4:
                    price += 10000
                    stay_days += 30
                    
            return (price, stay_days) # this has to be tuple so renpy string interpolation can pick up
            
        def injure_limb(self, limb):
            bad_limb = [l for l in self.get_limbs() if l.name == limb.name][0]
            bad_limb.injure()
            setattr(self, bad_limb.name, bad_limb)
            
        def increase_limbs_severity(self, injured_limbs):
            for limb in injured_limbs:
                l = getattr(self, limb.name)
                l.injure()
                setattr(self, limb.name, l)
            
        def get_limbs(self):
            return [self.head, self.torso, self.left_arm, self.right_arm, self.left_leg, self.right_leg]
            
        def get_injured_limbs(self):
            return [limb for limb in self.get_limbs() if limb.injury]
            
        def buy_item(self, item):
            if self.ryo >= item.price:
                self.ryo -= item.price
                if self.has_item(item):
                    current_inventory_item = self.get_item(item)
                    current_inventory_item.quantity += 1
                    self.remove_item(item)
                    self.items.append(current_inventory_item)
                    return self.items
                else:
                    item.quantity += 1
                    self.items.append(copy.deepcopy(item))
                    return self.items
                
            else:
                return self.items
                
        def remove_item(self, item):
            self.items = [i for i in self.items if i.name != item.name]
                
        def get_item(self, item):
            for i in self.items:
                if i.name == item.name:
                    return i
            
        def has_item(self, item):
            if item.name in [i.name for i in self.items]:
                return True
            return False
            
        def buy_weapon(self, weapon):
            if self.ryo >= weapon.price:
                self.ryo -= weapon.price
                if self.has_weapon(weapon):
                    current_inventory_weapon = self.get_weapon(weapon)
                    current_inventory_weapon.quantity += 1
                    self.remove_weapon(weapon)
                    self.weapons.append(current_inventory_weapon)
                    return self.weapons
                else:
                    weapon.quantity += 1
                    self.weapons.append(copy.deepcopy(weapon))
                    return self.weapons
                
            else:
                return self.weapons
                
        def remove_weapon(self, weapon):
            self.weapons = [w for w in self.weapons if w.name != weapon.name]
                
        def get_weapon(self, weapon):
            for w in self.weapons:
                if w.name == weapon.name:
                    return w
            
        def has_weapon(self, weapon):
            if weapon.name in [w.name for w in self.weapons]:
                return True
            return False
            
        def set_sensei(self):
            if self.team:
                self.sensei = self.team.sensei
            
        def is_injured(self):
            for limb in self.get_limbs():
                if limb.injury:
                    return True
            return False
            
        def injured_limbs(self):
            injured = [limb for limb in self.get_limbs() if limb.injury]
            return injured
            
        def injury_chance(self, chance=0.00):
            percent = chance * 100
            if random.randint(1,101) < percent:
                random.choice(self.get_limbs()).injure()
                
        def increase_hp(self, health):
            self.hp += health
            if self.hp > self.maxhp:
                self.hp = self.maxhp
                
        def increase_chakra(self, chakra):
            self.chakra += chakra
            if self.chakra > self.maxchakra:
                self.chakra = self.maxchakra
            
        def increase_bond(self, bond):
            self.bond += bond
            if self.bond > MAX_BOND:
                self.bond = MAX_BOND
            
        def level_up(self):
            difference = self.exp - LEVELS[self.level + 1]
            if difference < 0:
                return
            else:
                self.level +=1
                self.allocation_points += 3
                self.maxhp += renpy.random.randint(20, 30)
                self.maxchakra += renpy.random.randint(10, 20)
                self.exp = 0
                self.gain_exp(difference)
                
        def gain_exp(self, exp):
            # add randomness in exp when passing param
            self.exp += exp
            self.level_up()
            return self.exp
        
        def change_direction(self, direction):
            if direction == 'left':
                self.tilepic = self.tilepic.replace("_r", "_l")
            else:
                self.tilepic = self.tilepic.replace("_l", "_r")
            
        def is_bleeding(self):
            for limb in self.get_limbs():
                if limb.bleeding:
                    return True
            return False
            
        def bleeding_limbs_count(self):
            bad_limbs = [limb for limb in self.get_limbs() if limb.bleeding]
            return len(bad_limbs)
            
        def get_skill(self, name):
            for skill in self.all_skills:
                if skill.name == name:
                    return skill
                    
        def remove_skill_by_name(self, name):
            for skill in self.all_skills:
                if skill.name == name:
                    self.remove_skill(skill)
                    delattr(self, skill.label)
                    
        def assign_all_skills(self):
            for skill in self.all_skills:
                skill.limbs = self.get_limbs()
                setattr(self, skill.label, copy.deepcopy(skill))
                
        def remove_skill(self, skill):
            delattr(self, skill.label)
            self.all_skills = [s for s in self.all_skills if s.name != skill.name]
            
        def assign_skill(self, skill):
            setattr(self, skill.label, skill)
            skill.limbs = self.get_limbs()
            self.all_skills.append(skill)
            
        def apply_skill(self, skill):
            skill.apply()
            setattr(self, skill.label, skill)
            setattr(getattr(self, skill.label), 'active', True)
            
        def check_active_skill(self, skill):
            s = getattr(self, skill.label, None)
            if s:
                if s.active:
                    return True
                else:
                    return False 
            else:
                return False
            
        def active_defensive_skill(self):
            defensive_skills = [self.check_active_skill(skill) for skill in self.defensiveskills]
            if True in defensive_skills:
                return True
            else:
                return False
            
        def fix_stats(self):
            if self.hp < 0:
                self.hp = 0
                
            if self.hp > self.maxhp:
                self.hp = self.maxhp
            
            if self.chakra < 0:
                self.chakra = 0
                
            if self.chakra > self.maxchakra:
                self.chakra = self.maxchakra
                
        def __repr__(self):
            return "<Player>: {} {}/{}".format(self.name, self.hp, self.maxhp)
            
    class LevelledPlayer(Player):
        def __init__(self, lvl, name='Thug', picname="thug_tile_r", character=None, tilepic="thug_tile_r", hudpic='thug_hud', 
                     skill_pool=[], special_tags=[], home_village=None, tile=None, battle_ai=[], interaction={}, weapons=[]):
            self.level = lvl
            self.name = name
            self.picname = picname
            self.character = character
            self.tilepic = tilepic
            self.hudpic = hudpic
            self.tile = tile
            self.battle_ai = battle_ai
            self.interaction = interaction
            
            self.maxhp = 50 + (10 * self.level)
            self.maxchakra = 30 + (5 * self.level)
            self.strength = 1.5 * self.level
            self.speed = self.level / 2
            if self.speed > 10:
                self.speed = 10
            elif self.speed < 1:
                self.speed = 1
                
            self.evasion = self.level * 0.8
            self.defence = self.level * 0.6
            self.stamina = self.level * 0.5
            self.base_hit_rate = 60 + self.level
            
            self.meleeskills = []
            self.specialskills = []
            self.rangedskills = []
            self.defensiveskills = []
            self.weapons = weapons
            
            for skill in skill_pool:
                if skill.skill_type == 'melee':
                    self.meleeskills.append(skill)
                elif skill.skill_type == 'special':
                    self.specialskills.append(skill)
                elif skill.skill_type == 'ranged':
                    self.rangedskills.append(skill)
                elif skill.skill_type == 'defence':
                    self.defensiveskills.append(skill)
                elif skill.skill_type == 'weapon':
                    self.weapons.append(skill)
                    
            for tag in special_tags:
                ability = getattr(self, tag)
                if tag == 'speed':
                    ability = 10
                else:
                    ability += random.randint(6,10)
                setattr(self, tag, ability)
                
            super(self.__class__, self).__init__(name=self.name, 
                                                 picname=self.picname, 
                                                 character=self.character, 
                                                 tilepic=self.tilepic, 
                                                 hudpic=self.hudpic, 
                                                 hp=self.maxhp, 
                                                 maxhp=self.maxhp, 
                                                 chakra=self.maxchakra, 
                                                 maxchakra=self.maxchakra, 
                                                 tile=self.tile,
                                                 battle_ai=self.battle_ai,
                                                 strength=self.strength, 
                                                 speed=self.speed, 
                                                 evasion=self.evasion, 
                                                 defence=self.defence, 
                                                 stamina=self.stamina, 
                                                 base_hit_rate=self.base_hit_rate, 
                                                 meleeskills=self.meleeskills, 
                                                 specialskills=self.specialskills, 
                                                 rangedskills=self.rangedskills, 
                                                 items=[], 
                                                 defensiveskills=self.defensiveskills, 
                                                 bloodlineskills=[], 
                                                 weapons=self.weapons, 
                                                 interaction=self.interaction,
                                                 level=self.level)
                                                 
            