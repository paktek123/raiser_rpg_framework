##############################################################################
# UTILITY FUNCTIONS AND HELPERS
#

init -1 python:
    
    #### MAPS AND WORLD EVENTS ####
    
    def time_tag_show(image_name):
        """
        Depending on the time show the particular background
        """
        if main_time.hour in (6, 7, 8, 9, 10, 11):
            renpy.show((image_name, 'morning'))
        elif main_time.hour in (12, 13, 14, 15, 16, 17):
            renpy.show((image_name, 'afternoon'))
        elif main_time.hour in (18, 19, 20, 21):
            renpy.show((image_name, 'evening'))
        elif main_time.hour in (21, 22, 23, 0, 1, 2, 3, 4, 5):
            renpy.show((image_name, 'night'))
    
    def show_village_map(village, player):
        # Remove any locations
        current_session.location = None
        
        # Show screens for village
        renpy.show_screen("player_stats")
        renpy.show_screen("stats_screen", player)
        renpy.show_screen("time_screen")
        
        # Upon reload in debug mode village and player are None (solved by going to main menu then reloading)
        renpy.hide(village.map) # remove it first otherwise it does not show the new image on top
        
        # Show the map
        time_tag_show(village.map)
        renpy.call_screen('villagemap', village, player)
        return
    
    def start_world_events(background, follow_on_label):
        renpy.show(background)
        
        # Go through each village and do random event
        for village in ALL_VILLAGES:
            renpy.show_screen('worldevents', village)
            village.random_event()
            renpy.hide_screen('worldevents')
            
        renpy.jump(follow_on_label)
        
    def populate_events():
        """
        Takes the calendar generated days and populates them with events that are 
        in the relevant date range, frequency or chance
        """
        # populate events
        for d in ALL_DAYS:
            for e in ALL_EVENTS:
                if e.start and e.finish:
                    for r in e.date_range(test_main_time):
                        if r.day == d.number and r.month == d.month.number:
                            d.events.append(e)
                elif e.frequency:
                    for day in e.frequency:
                        if d.number == day:
                            d.events.append(e)
                elif e.chance:
                    if (100*e.chance) > random.randint(1, 101):
                        d.events.append(e)
                    
        # only get unique events
        for d in ALL_DAYS:
            d.events = d.events
    
    #### FIGHT HELPERS ####
    
    def highlight_position(player, enemy, stage):
        """
        Used to highlight projected tiles and active tiles
        """
        
        # deactive and deproject all tiles
        for tile in stage.tiles:
            if not tile.trap:
                tile.deactivate()
                tile.deproject()
                
        # incase we are off the grid put the player back in place
        max_limit = player.tile.position + player.speed
        min_limit = player.tile.position - player.speed
        
        if max_limit > 12:
            max_limit = 12
        
        if min_limit < 1:
            min_limit = 1
            
        # Get the low and high ranges
        low_range = range(min_limit, player.tile.position)
        high_range = range(player.tile.position + 1, max_limit + 1)
        
        # remove the current player and enemy positions
        low_range = [x for x in low_range if x != player.tile.position]
        high_range = [x for x in high_range if x != player.tile.position]
        low_range = [x for x in low_range if x != enemy.tile.position]
        high_range = [x for x in high_range if x != enemy.tile.position]
        
        for tile_position in low_range:
            tile = get_tile_from_position(tile_position, stage)
            if not tile.trap:
                tile.project()
            
        for tile_position in high_range:
            tile = get_tile_from_position(tile_position, stage)
            if not tile.trap:
                tile.project()
            
        show_player_at_pos(player, enemy, stage, player.tile)
        show_player_at_pos(enemy, player, stage, enemy.tile)
    
    def show_player_at_pos(player, enemy, stage, tile, initial_movement=False):
        """
        Show tilepic of player / enemy on a tile
        """
        player.tile.deactivate()
        player.tile = tile
        player.tile.activate()
        
        renpy.hide(player.tilepic)
        
        # change the facing of player relative to the enemy
        if player.tile.position < enemy.tile.position:
            player.facing = 'right'
            player.change_direction(player.facing)
        else:
            player.facing = 'left'
            player.change_direction(player.facing)
            
        renpy.show(player.tilepic, [ POSITIONS[tile.position] ])
        
        # Handle traps / BETA do not use
        #if tile.trap:
            # This causes a ui.close() exception, commenting for now
            #renpy.say(player.character, "Oh no there is a trap here!")
        #    player.hp -= 30
        #    remove_trap(tile, stage)
        
    def hide_battle_screen(all=False):
        """
        Usually called during a teardown of the battle to hide all screens
        and return to dialogue
        """
        renpy.hide_screen("battlemenu")
        renpy.hide_screen("skill_actions")
        renpy.hide_screen("item_actions")
        renpy.hide_screen("player_stats")
        renpy.hide_screen("stats_screen")
        renpy.hide_screen("time_screen")
        if all:
            renpy.hide_screen("stats")
            renpy.hide_screen("battlebars")
            renpy.hide_screen("battle_explanation") 
            renpy.hide_screen("location_explanation") 
            renpy.hide_screen("move_explanation") 
            renpy.hide_screen("player_limbs") 
            renpy.hide_screen("enemy_limbs") 
            
    ##### ENEMY FIGHT AI #####
    
    def find_suitable_tag_partner(tag):
        """
        This is used for enemy AI tagging
        Logic:
            If there is only 1 tag partner then if he/she has more than 0 hp
            return them
        
            If there are 2 tag partners then if one has more hp than the other
            return that partner, if the same HP return the first.
        
            If None of the above criteria is met return None
        """
        
        if len(tag) == 1:
            if tag[0].hp > 0:
                return tag[0]
        elif len(tag) == 2:
            if tag[0].hp > tag[1].hp and tag[0].hp > 0:
                return tag[0]
            elif tag[1].hp > tag[0].hp and tag[1].hp > 0:
                return tag[1]
            elif tag[1].hp == tag[0].hp and tag[0].hp > 0:
                return tag[0]
            else:
                return None
        return None
    
    def enemy_tag_move(enemy, player, tag_p, tag_e):
        """
        Enemy tagging AI
        """
        # Tag if chakra or hp below 40%
        if (enemy.hp < (enemy.maxhp*0.4) and tag_e) or (enemy.chakra < (enemy.maxchakra*0.4) and tag_e):
            # only 50% chance of tagging partner
            if random.randint(1, 100) < 50:
                partner = find_suitable_tag_partner(tag_e)
                if partner:
                    partner.main = True
                    enemy.main = False
                    partner.tile = enemy.tile
                    renpy.hide(enemy.tilepic)
                    info = get_tag_info(enemy, tag_e)
        
                    renpy.call('fight', 
                               player, 
                               info['main'],
                               tag_p, 
                               info['tag'],
                               current_session.stage, 
                               current_session.win_label,
                               current_session.lose_label,
                               current_session.draw_label)
    
    def enemy_pattern(enemy):
        """
        This determines the weighting on certain skills
        """
        PATTERN_HASH = {'d': enemy.defensiveskills,
                        'f': enemy.weapons,
                        'a': enemy.meleeskills + enemy.specialskills + enemy.rangedskills,
                        'm': enemy.meleeskills,
                        's': enemy.specialskills,
                        'r': enemy.rangedskills}
        
        try:
            current_skill = random.choice(PATTERN_HASH[random.choice(enemy.battle_ai)])
        except IndexError:
            current_skill = random.choice(enemy.all_skills)
        
        return current_skill
        
    def enemy_move_back(enemy, player, spaces=0):
        """
        This moves enemy back the number of given spaces (tiles) with in the limits
        """
        relative_position = enemy.tile.position - player.tile.position
        enemy_tile_position = enemy.tile.position
        
        if relative_position > 0:
            enemy_tile_position += spaces
            if enemy_tile_position > 12:
                enemy_tile_position = 12
        else:
            enemy_tile_position -= spaces
            if enemy_tile_position < 1:
                enemy_tile_position = 1
                
        new_tile = get_tile_from_position(enemy_tile_position, current_session.stage)
        enemy_tile = new_tile
        show_player_at_pos(enemy, player, current_session.stage, new_tile)
        
    def enemy_use_item(enemy, player):
        """
        If enemy hp below 30% or chakra below 20% use item to heal
        """
        if enemy.hp < (enemy.maxhp*0.3):
            enemy_move_back(enemy, player, 3)
            if random.randint(1, 100) < 40:
                renpy.say(enemy.character, "I heal using health paste.")
                enemy.increase_hp(30)
                Jump("fight")
                
        if enemy.chakra < (enemy.maxchakra*0.2):
            enemy_move_back(enemy, player, 3)
            if random.randint(1, 100) < 60:
                renpy.say(enemy.character, "I am resting now to heal chakra.")
                enemy.increase_chakra(25)
                Jump("fight")
                
    def enemy_move_around(enemy, player):
        """
        This will be deprecated because only 1 move allowed per turn
        """
        move_to = random.randint(1, enemy.speed)
        old_tile = enemy.tile
        if player.tile.position == move_to:
            # warning: this may lead to player going off grid
            enemy_tile = get_tile_from_position(player.tile.position + 1, current_session.stage)
        else:
            enemy_tile = get_tile_from_position(move_to, current_session.stage)
            
        # this is to prevent error where tile is None
        if not enemy.tile:
            enemy_tile = old_tile
            
        show_player_at_pos(enemy, player, None, enemy_tile)
        
    def enemy_move(player, enemy, stage, tag_p, tag_e):
        """
        Master logic on how the enemy AI moves during fight
        """
        hide_battle_screen()
        show_player_at_pos(enemy, player, stage, enemy.tile)
        
        # Only 1 movement, turn this on for multiple movements
        #enemy_move_around(enemy, player)
        
        # enemy only needs to tag if partner has enough hp
        for partner in tag_e:
            if partner.hp > enemy.hp:
                enemy_tag_move(enemy, player, tag_p, tag_e)
        
        # comment this out if enemy can't heal
        enemy_use_item(enemy, player)
        
        current_skill = enemy_pattern(enemy)
        
        # if its a defensive skill check if is already applied 
        # if already applied then do another attacking skill instead
        # if not applied apply it to enemy
        if current_skill.skill_type == 'defence':
            if not enemy.active_defensive_skill():
                enemy.apply_skill(current_skill)
                Jump("fight")
            else:
                current_skill = random.choice(enemy.meleeskills + enemy.specialskills + enemy.weapons + enemy.rangedskills)
                
        # if within range execute the skill
        if current_skill.range >= abs(player.tile.position - enemy.tile.position):
            show_player_at_pos(enemy, player, None, enemy.tile)
            current_skill.action(enemy, player)
        else:
            # move enemy to near player
            old_tile = enemy.tile
            # check distance between enemy and player
            difference = abs(enemy.tile.position - player.tile.position)
            if difference > enemy.speed:
                if enemy.tile.position > player.tile.position:
                    enemy_position = enemy.tile.position - enemy.speed
                else:
                    enemy_position = enemy.tile.position + enemy.speed
            else:
                # must be within range
                if enemy.tile.position > player.tile.position:
                    enemy_position = player.tile.position - current_skill.range
                else:
                    enemy_position = player.tile.position + current_skill.range
                
            enemy_tile = get_tile_from_position(abs(enemy_position), current_session.stage)
            
            # if no tile is return for whatever reason keep enemy on same tile
            if not enemy.tile or not enemy_tile:
                enemy_tile = old_tile
                
            # enemy cannot be on the same tile as player
            if enemy.tile == player.tile or enemy_tile == player.tile:
                enemy_tile = old_tile
                
            show_player_at_pos(enemy, player, None, enemy_tile)
            
            # Do the attack
            current_skill.action(enemy, player)
            
            # take away movement chakra too
            enemy.chakra -= (current_skill.range * stage.pull) 
        
        # bleeding
        player_bleed(player)
        
        # trap (BETA / do not use)
        #if enemy.tile.trap:
            # TODO: some affect similar but not text
        #    enemy.hp -= 30
        #    remove_trap(enemy.tile, stage)
            
        Jump("fight")
        
    def player_bleed(target):
        """
        If targets HP is below 30% there is a 60% chance of injury to a random limb
        """
        if target.hp < (0.3 * target.maxhp):
            if renpy.random.randint(1,3) > 2:
                limb = random.choice(target.get_limbs())
                limb.injure()
                renpy.say(target.character, "No my {} is bleeding".format(limb.name))
                if not limb.bleeding:
                    limb.bleed()
                setattr(target, limb.name, limb)
        
    def drain_blood(target):
        """
        BETA functionality of blood draining, idea is to have a blood meter appear
        if that drains then that player looses conciousness irrelevant of HP
        No tests
        """
        if target.is_bleeding():
            target.blood -= target.bleeding_limbs_count() * (5 + renpy.random.randint(0, 2))
            renpy.say(target.character, "I need to end this soon, I am loosing too much blood.")
        
    def counter_move(player, enemy):
        """
        If player uses a defensive skill that puts them into a counter state
        """
        renpy.say(enemy.character, "You left yourself open.")
        enemy_pos = enemy.tile.position
        
        if enemy_pos < 12:
            player.tile = get_tile_from_position(enemy_pos + 1, current_session.stage)
            player.change_direction(player.facing)
        else:
            player.tile = get_tile_from_position(player.tile.position - 1, current_session.stage)
            
        player.counter_state = False
        renpy.say(player.character, "Got you!")
        renpy.show(player.tilepic, [ POSITIONS[player.tile.position] ])
        Jump("fight")    
        
    def set_trap_at_pos(player, enemy, stage, tile):
        """
        Beta functionality / not used
        """
        if not tile.trap:
            renpy.say(player.character, "I set a trap here.")
            tile.activate_trap()
        else:
            renpy.say(player.character, "A trap is already set there.")
            set_trap_at_pos(player, enemy, stage, tile)
        
    def remove_all_skill_affects(player, enemy):
        """
        Remove any defensive skills applied and fix negative stats
        """
        player.fix_stats()
        enemy.fix_stats()
        
        for skill in player.all_skills:
            s = getattr(player, skill.label)
            if s.used == s.duration:
                s.used = 0
                s.remove()
                setattr(player, s.label, s)
                
        for skill in enemy.all_skills:
            s = getattr(enemy, skill.label)
            if s.used == s.duration:
                s.used = 0
                s.remove()
                setattr(enemy, s.label, s)
                
    def remove_traps_from_all_tiles():
        """
        BETA not in tests
        """
        for tile in current_session.stage.tiles:
            remove_trap(tile, current_session.stage)
            
    def hide_player_pics(player):
        renpy.hide(player.tilepic)
        renpy.hide(player.hudpic)
                
    def end_match_teardown(player, enemy, match_result):
        """
        Teardown all data and setup for next battle 
        """
        player.damage_dealt = 0
        enemy.damage_dealt = 0
        current_session.enemy_tag = None
        current_session.player_tag = None
        current_session.initial_pos = True
        moved = False
        current_session.last_match_result = match_result
        battle_turn = 0
        store.battle_turn = 0
        remove_traps_from_all_tiles()
        hide_player_pics(player)
        hide_player_pics(enemy)
        hide_battle_screen(all=True)
        
    def end_match(player, enemy, tag_p, tag_e, win_label, lose_label, draw_label):
        # if player hp reaches zero force tag to partner with good hp
        if player.hp == 0 and tag_p:
            for partner in tag_p:
                if partner.hp > 0:
                    partner.main = True
                    player.main = False
                    partner.tile = player.tile
                    renpy.jump('tag_partner')
        
        if enemy.hp == 0 and tag_e:
            partner = find_suitable_tag_partner(tag_e)
            if partner:
                partner.main = True
                enemy.main = False
                partner.tile = enemy.tile
                renpy.hide(enemy.tilepic)
                info = get_tag_info(enemy, tag_e)
        
                renpy.call('fight', 
                           player, 
                           info['main'],
                           tag_p, 
                           info['tag'],
                           current_session.stage, 
                           current_session.win_label,
                           current_session.lose_label,
                           current_session.draw_label)
                
        if store.battle_turn == current_session.fight_limit:
            end_match_teardown(player, enemy, 'draw')
            if 'generic' in draw_label:
                renpy.call(draw_label, current_session.main_player)
            else:
                renpy.call(draw_label)
        
        if player.hp == 0:
            end_match_teardown(player, enemy, 'lose')
            if 'generic' in lose_label:
                renpy.call(lose_label, current_session.main_player)
            else:
                renpy.call(lose_label)
        elif enemy.hp == 0:
            end_match_teardown(player, enemy, 'win')
            if 'generic' in win_label:
                renpy.call(win_label, current_session.main_player)
            else:
                renpy.call(win_label)
            
    def get_tag_info(player, tag_p):
        """
        Change the main player depending on the the player.main flag
        """
        one_list = [player] + tag_p
        info = {}
        new_tag_p = []
        
        for p in one_list:
            if not p.main:
                new_tag_p.append(p)
            
        for p in one_list:
            p.tile.deactivate()
            p.tile = player.tile
            if p.main:
                info['main'] = p
            else:
                info['tag'] = new_tag_p
                
        # deactivate tiles
        info['main'].tile.activate()
                
        return info
        
    def get_sensei_skill(sensei, student):
        """
        Get a random skill from Sensei, check if student already has it, if not
        then assign it to student
        """
        sensei_skills = [skill.label for skill in sensei.all_skills]
        student_skills = [skill.label for skill in student.all_skills]
        skills_to_teach = list(set(sensei_skills) - set(student_skills))
        if skills_to_teach:
            new_skill_label = random.choice(skills_to_teach)
            new_skill = copy.deepcopy(getattr(sensei, new_skill_label))
            new_skill.set_to_default()
            learnt_skill = new_skill
            student.assign_skill(learnt_skill)
            return learnt_skill
        else:
            return None
            
    ##### MISC ######
            
    def get_player_by_name(name):
        for player in current_session.team.members:
            if player.name == name:
                return player
                
    def get_battle_by_id(id):
        for battle in current_session.battles:
            if battle.id == id:
                return battle
                
    def is_event_active_today(event, game_time):
        if event.name in [e.name for e in get_today(game_time).events]:
            return True
        return False
        
    def other_villages(village):
        return [v for v in ALL_VILLAGES if v.id != village.id]
                
                
    #### BATTLE DRAG ####
    def player_dragged(drags, drop):
        """
        If player id dragged to a particular battle field they are added
        to the good team
        """

        if not drop:
            return

        player_on_good_team = drags[0].drag_name
        battle_id = drop.drag_name
        
        player = get_player_by_name(player_on_good_team)
        battle = get_battle_by_id(battle_id)
        
        other_battles = [b for b in current_session.battles if b.id != battle.id]
        
        # stop being added to the same battle twice
        if player in battle.good_team:
            return True
        
        # if put in other battles, remove from other battles
        for b in other_battles:
            for p in b.good_team:
                if player == p:
                    b.good_team.remove(p)
        
        battle.add_good_member(player)
       
        return True
        
    def populate_battles(battles, follow_on):
        """
        Populate the follow_on for battles, this allows the battle to jump
        to the next one after a fight ends
        """
        for index, battle in enumerate(battles):
            if battle.id == "last":
                battle.next_battle_label = "battle_choose"
                battle.follow_on = follow_on
            else:
                battle.next_battle_label = battles[index + 1].battle_label
                
    def get_battle_from_label(label):
        for battle in current_session.battles:
            if battle.battle_label == label:
                return battle
                
    def battle_finished(battles):
        """
        If all team members have 0 hp, end battle otherwise
        continue
        """
        result = {'outcome': 'loss', 'is_finished': False}
        
        hps = [m.hp for m in current_session.team.members]
        
        # if the total hps are below 0, end battle
        if sum(hps) < 0:
            result['is_finished'] = True
            return result
        
        for battle in battles:
            if not battle.finished():
                return result
                
        result['is_finished'] = True
        result['outcome'] = 'win'
        
        return result
        
            
    import math

    class Shaker(object):
        
        anchors = {
                'top' : 0.0,
                'center' : 0.5,
                'bottom' : 1.0,
                'left' : 0.0,
                'right' : 1.0,
                }
        
        def __init__(self, start, child, dist):
            if start is None:
                start = child.get_placement()
            #
            self.start = [ self.anchors.get(i, i) for i in start ]  # central position
            self.dist = dist    # maximum distance, in pixels, from the starting point
            self.child = child
                
        def __call__(self, t, sizes):
            # Float to integer... turns floating point numbers to
            # integers.                
            def fti(x, r):
                if x is None:
                    x = 0
                if isinstance(x, float):
                    return int(x * r)
                else:
                    return x

            xpos, ypos, xanchor, yanchor = [ fti(a, b) for a, b in zip(self.start, sizes) ]

            xpos = xpos - xanchor
            ypos = ypos - yanchor
                
            nx = xpos + (1.0-t) * self.dist * (renpy.random.random()*2-1)
            ny = ypos + (1.0-t) * self.dist * (renpy.random.random()*2-1)

            return (int(nx), int(ny), 0, 0)
        
    def _Shake(start, time, child=None, dist=100.0, **properties):

        move = Shaker(start, child, dist=dist)
        
        return renpy.display.layout.Motion(move,
                          time,
                          child,
                          add_sizes=True,
                          **properties)

    Shake = renpy.curry(_Shake)
