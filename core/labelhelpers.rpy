##############################################################################
# HELPER LABELS
#

####### FIGHT / MOVE / TAG ########

label tag_partner:
    $ info = get_tag_info(player, tag_p)
    $ renpy.hide(player.tilepic)
    $ renpy.call('fight', info['main'], enemy, info['tag'], tag_e, stage, win_label, lose_label, draw_label)
    
label fight(player, enemy, tag_p, tag_e, stage=clearing, win_label='generic_win', lose_label='generic_lose', draw_label='generic_draw', fight_limit=20):

    # hide any screens
    $ hide_battle_screen(all=True)
    hide screen movemenu
    hide screen settrap
    
    # set current_session
    $ current_session.enemy_tag = tag_e
    $ current_session.player_tag = tag_p
    $ current_session.stage = stage
    $ current_session.win_label = win_label
    $ current_session.lose_label = lose_label
    $ current_session.draw_label = draw_label
    $ current_session.fight_limit = fight_limit
    
    # initial position of player and enemy
    call remove_projections
    call initial_pos(player, enemy)
        
    $ highlight_position(player, enemy, stage)
    $ end_match(player, enemy, tag_p, tag_e, win_label, lose_label, draw_label)
    $ remove_all_skill_affects(player, enemy)
    
    # show any battle screen
    show screen battlebars(tag_p, tag_e)
    #show screen player_limbs(player=player) # uncomment to show player limbs during battle (warning: screen does not exist)
    call screen battlemenu(player, tag_p)
    
label initial_pos(player, enemy):
    python:
        if current_session.initial_pos:
            player.tile = current_session.stage.tile1
            enemy.tile = current_session.stage.tile12
            show_player_at_pos(enemy, player, current_session.stage, current_session.stage.tile12)
            show_player_at_pos(player, enemy, current_session.stage, current_session.stage.tile1)
            current_session.initial_pos = False
    return
    
label remove_projections:
    python:
        for tile in current_session.stage.tiles:
            tile.deproject()
    return
    
    
# modify generic labels for frequent outcomes to battles because not all can be unique
label generic_win(player):
    
    # some more teardown
    $ hide_battle_screen(all=True)
    $ battle_turn = 0
    $ exp = renpy.random.randint(100,200) + 200
    $ player.gain_exp(exp)
    
    # spar means if the player was training with a partner, this should not be called for 
    # normal fights
    if current_session.spar:
        $ chemistry = renpy.random.randint(10, 15)
        $ player.team.increase_chemistry(chemistry)
        player.character "I gained [chemistry] team chemistry."
        $ current_session.spar = []

    player.character "I won the match and gained [exp] exp."
    player.character "Now to head back to the village."
    player.character "..."
    player.character "..........."
    player.character "......................."
    
    python:
        main_time.advance_time(hours=current_session.time_to_advance.get('hours'),
                               days=current_session.time_to_advance.get('days'),
                               months=current_session.time_to_advance.get('months'),
                               years=current_session.time_to_advance.get('years'))
    
    $ current_session.clear_time_to_advance() # this clears rest too
    
    # checks if a mission was in progress, if it was then get rewards
    call mission_report(player, current_session.mission)
    
    # back to village map
    $ show_village_map(current_session.village, current_session.main_player)

# modify generic labels for frequent outcomes to battles because not all can be unique
label generic_lose(player):
    
    # some more teardown
    $ hide_battle_screen(all=True)
    $ battle_turn = 0
    $ exp = renpy.random.randint(50,100) + 50
    $ player.gain_exp(exp)
    
    # spar means if the player was training with a partner, this should not be called for 
    # normal fights
    if current_session.spar:
        $ chemistry = renpy.random.randint(10, 15)
        $ player.team.increase_chemistry(chemistry)
        player.character "I gained [chemistry] team chemistry."
        $ current_session.spar = []
        
    player.character "I lost the match and gained [exp] exp."
    player.character "Now to head back to the village."
    player.character "..."
    player.character "..........."
    player.character "......................."
    
    python:
        main_time.advance_time(hours=current_session.time_to_advance.get('hours'),
                               days=current_session.time_to_advance.get('days'),
                               months=current_session.time_to_advance.get('months'),
                               years=current_session.time_to_advance.get('years'))
    
    $ current_session.clear_time_to_advance() # this clears rest too
    
    call mission_report(player, current_session.mission)
    
    $ show_village_map(current_session.village, current_session.main_player)
    
# modify generic labels for frequent outcomes to battles because not all can be unique
label generic_draw(player):
    
    # some more teardown
    $ hide_battle_screen(all=True)
    $ battle_turn = 0
    $ exp = renpy.random.randint(100,200) + 100
    $ player.gain_exp(exp)
    
    # spar means if the player was training with a partner, this should not be called for 
    # normal fights
    if current_session.spar:
        $ chemistry = renpy.random.randint(10, 15)
        $ player.team.increase_chemistry(chemistry)
        player.character "I gained [chemistry] team chemistry."
        $ current_session.spar = []
        
    player.character "I draw the match and gained [exp] exp."
    player.character "Now to head back to the village."
    player.character "..."
    player.character "..........."
    player.character "......................."
    
    python:
        main_time.advance_time(hours=current_session.time_to_advance.get('hours'),
                               days=current_session.time_to_advance.get('days'),
                               months=current_session.time_to_advance.get('months'),
                               years=current_session.time_to_advance.get('years'))
    
    $ current_session.clear_time_to_advance() # this clears rest too
    call mission_report(player, current_session.mission)
    $ show_village_map(current_session.village, current_session.main_player)
    
label mission_report(player, mission):
    # change background here if needed use $time_tag_show(image_name)
    python:
        if mission:
            if mission.success:
                renpy.say(player.home_village.leader.character, "Good work {}.".format(player.name))
                reward = mission.reward(player)
                renpy.say(player.home_village.leader.character, "Here is your reward money {} and exp {}.".format(reward['ryo'], reward['exp']))
            else:
                renpy.say(player.home_village.leader.character, "It is unfortunate {} but you failed.".format(player.name))
                reward = mission.reward(player, half=True)
                renpy.say(player.home_village.leader.character, "Here is your reward money {} and exp {} for your trouble.".format(reward['ryo'], reward['exp']))
    $ current_session.mission = None
    return
    
label standby:
    $ player.chakra += player.stamina * 5
    jump enemymove
    
label enemymove:
    $ moved = False
    $ end_match(player, enemy, tag_p, tag_e, win_label, lose_label, draw_label)
    $ remove_all_skill_affects(player, enemy)
    
    python:
        if enemy.stunned:
            renpy.say(player.character, "The enemy is stunned and cannot move.")
            enemy.stunned = False
        else:
            if player.counter_state:
                counter_move(player, enemy)
            else:
                enemy_move(player, enemy, clearing, tag_p, tag_e)

    $ battle_turn += 1
    call fight(player, enemy, tag_p, tag_e, stage, win_label, lose_label, draw_label, fight_limit)

####### CHARACTER CREATION ########

label allocate_points:
    
    if current_session.main_player.allocation_points > 0:
        call screen allocatepoints(current_session.main_player)
    else:
        hide screen explanation
        nar_c "Stats have been set, game is starting now."
        jump prologue1
        
label reset_allocation_points:
    python:
        stats = ['strength', 'speed', 'evasion', 'defence', 'stamina', 'melee', 'special', 'ranged']
        for stat in stats:
            setattr(current_session.main_player, stat, 1)
        current_session.main_player.allocation_points = 10
    jump allocate_points
    
    
####### BATTLES ########

# Battles current only support 3 battles, more to be supported in later versions
label reset_battle:
    python:
        for b in current_session.battles:
            b.good_team = []
    # battle_follow_on is set in battle_prep_screen
    $ renpy.call('battle_choose')
    
label b_battle_2:
    $ second_battle = get_battle_from_label('b_battle_2')
    $ current_session.battle = second_battle
    $ second_battle.fight(stage=clearing, win_label=second_battle.next_battle_label, lose_label=second_battle.next_battle_label, draw_label=second_battle.next_battle_label, fight_limit=10)
    
label b_battle_last:
    $ last_battle = get_battle_from_label('b_battle_last')
    $ current_session.battle = last_battle
    $ last_battle.fight(stage=clearing, win_label='battle_choose', lose_label='battle_choose', draw_label='battle_choose', fight_limit=10)
    
label battle_start:
    
    $ first_battle = current_session.battles[0]
    $ current_session.battle = first_battle
    
    $ first_battle.fight(stage=clearing, win_label=first_battle.next_battle_label, lose_label=first_battle.next_battle_label, draw_label=first_battle.next_battle_label, fight_limit=10)
            
    
label battle_choose:
    # Responsible for showing the battle screen
    # Checks if battle finished, if not continues
    
    hide screen battle_selection_screen
    hide screen battle_prep_screen
    
    python:
        battle_result = battle_finished(current_session.battles)
        if battle_result['is_finished']:
            if battle_result['outcome'] == 'lose':
                # if battle is lost then go to generic lose label, change it here
                renpy.jump('generic_lose')
            else:
                renpy.jump(current_session.battle_follow_on) 
    
    $ populate_battles(current_session.battles, current_session.battle_follow_on)
    show screen battle_prep_screen
    nar_c "Choose battlefield for players."
    jump battle_choose
    
####### REDIRECTS ########

label skill_redirect:
    python:
        # deal with exceptions
        if current_session.skill.skill_type == 'counter':
            player.counter_state = True
        
        if current_session.skill_type == 'attack':
            current_session.skill.action(player,enemy)
        elif current_session.skill_type == 'weapon':
            # decrease the quantity then attack
            current_session.skill.quantity -= 1
            current_session.skill.action(player,enemy)
        elif current_session.skill_type == 'defence':
            getattr(player, current_session.skill.label).apply()
            
    jump enemymove
    
label item_redirect:
    python:
        current_session.item.consume(current_session.main_player)
        
    jump enemymove
    
label village_redirect:
    $ current_session.location = None
    
    python:
        main_time.advance_time(hours=current_session.time_to_advance.get('hours'),
                               days=current_session.time_to_advance.get('days'),
                               months=current_session.time_to_advance.get('months'),
                               years=current_session.time_to_advance.get('years'))
    $ current_session.clear_time_to_advance()
    
    # check for active events, if active go to their label
    python:
        if is_event_active_today(e_jinchurri_attack, main_time) and e_jinchurri_attack.occurrence < 1:
            e_jinchurri_attack.occurrence += 1
            renpy.call(e_jinchurri_attack.label, current_session.main_player, current_session.village)
        else:
            e_jinchurri_attack.occurrence = 0
            
    # put this in a label ideally
    show screen player_stats
    show screen stats_screen(current_session.main_player)
    show screen time_screen
    $ show_village_map(current_session.village, current_session.main_player)
    
    current_session.main_player.character "I need to choose an action."
    jump village_redirect
    
label location_redirect:
    hide screen villagemap 
    python:
        main_time.advance_time(hours=current_session.time_to_advance.get('hours'),
                               days=current_session.time_to_advance.get('days'),
                               months=current_session.time_to_advance.get('months'),
                               years=current_session.time_to_advance.get('years'))
    # advance limb rest
    python:
        if current_session.rest:
            current_session.main_player.hp = current_session.main_player.maxhp
            current_session.main_player.chakra = current_session.main_player.maxchakra
            for limb in current_session.main_player.get_limbs():
                limb.rest(current_session.time_to_advance_in_days())
    
    $ current_session.clear_time_to_advance() # this clears rest too
    python:
        if current_session.location.background:
            renpy.hide(current_session.location.background)
            time_tag_show(current_session.location.background)
            
    $ renpy.call(current_session.location.label, current_session.main_player, current_session.village)
    
label missionselect_redirect:
    hide screen villagemissions
    show screen missionselect(current_session.village, current_session.main_player, current_session.mission_rank)
    current_session.main_player.character "I need to select a mission"
    jump missionselect_redirect
    
label mission_redirect:
    hide screen villagemap
    $ hide_battle_screen(all=True)
    $ import random # I hate myself for this
    $ current_session.mission.do_mission(current_session.main_player, current_session.village, random.choice(ALL_VILLAGES))
    
label purchase_item_redirect:
    $ current_session.main_player.buy_item(current_session.item)
    jump location_redirect
    
label purchase_weapon_redirect:
    $ current_session.main_player.buy_weapon(current_session.item)
    jump location_redirect
    
label statscreen_show_redirect:
    hide screen player_stats
    show screen stats_screen(current_session.main_player)
    jump village_redirect
    
label statscreen_hide_redirect:
    hide screen stats_screen
    jump village_redirect
    
####### LOCATIONS ########

label injury_revert:
    # This label controls if main_player is injured and tries to do an event
    # Example: If player is injured they can't do certain events like training
    
    if current_session.main_player.hp < current_session.main_player.maxhp:
        menu:
            "HP is not full, do you still want to continue?"
            
            "Yes":
                return
            "No":
                "HP/Chakra can be healed either at the hospital or by resting at home."
                $ current_session.clear_time_to_advance()
                jump village_redirect
    
    python:
        if current_session.main_player.get_injured_limbs():
            renpy.say(current_session.main_player.character, "I can't do this, I am injured and have to heal my injuries first by resting or from hospital.")
            current_session.clear_time_to_advance()
            renpy.jump("village_redirect")
            
label time_revert(opening_hour=6, closing_hour=18):
    # This label control if player tries to enter a time restricted location
    # Example: shop opening hours are between 6 to 18, out of hours will run this label
    python:
        if not main_time.hour in range(opening_hour, closing_hour):
            current_session.clear_time_to_advance()
            renpy.say("Guard",  "Sorry this place is only open between [opening_hour]AM and [closing_hour]PM.")
            renpy.jump("village_redirect")
    return
    
label village_travel(player, village):
    show screen villagetravel(village, player)
    player.character "I need to choose a destination"
    $ renpy.call('village_travel', player, village)
    
label village_levelup(player, village):
    show screen levelup(village, player)
    player.character "I need to choose level up stats"
    $ renpy.call('village_levelup', player, village)

label village_training(player, village):
    if player.hp < 50 or player.chakra < 50:
        player.character "I don't have enough hp or chakra to continue, I need to rest before I can train."
        jump village_redirect
    hide train_with_team
    hide train_skills
    show screen training(village, player)
    player.character "What should I do?"
    $ renpy.call('village_training', player, village)
    
label training_sensei:
    $ new_skill = get_sensei_skill(player.sensei, player)
    player.sensei.character "I am about to teach you is [new_skill.name]."
    if new_skill.unlock_exp < 300:
        player.sensei.character "It is a basic skill but fundamental to being a shinobi."
    elif new_skill.unlock_exp < 600:
        player.sensei.character "It is an intermediate skill but fundamental to being a shinobi."
    elif new_skill.unlock_exp < 900:
        player.sensei.character "It is an advanced skill and hard to master."
        
    # Add more text here if required
    player.character "[new_skill.name] added to skill set."
    $ renpy.call(current_session.location.label, current_session.main_player, current_session.village)
    
label train_skill_label:
    python:
        if current_session.main_player.get_injured_limbs():
            renpy.say(current_session.main_player.character, "I can't train, I am injured and have to heal my injuries first.")
            current_session.clear_time_to_advance()
        else:
            # this is hardcoded to be 200 by default, change if another value is required
            exp_gained = 200
            setattr(getattr(current_session.main_player, current_session.skill.label), current_session.skill.label,  current_session.skill.gain_exp(exp_gained))
            renpy.say(current_session.main_player.character, "I have gained {} exp for {}.".format(exp_gained, current_session.skill.name))
    jump location_redirect
    
label train_gain_exp:
    python:
        if current_session.main_player.get_injured_limbs():
            renpy.say(current_session.main_player.character, "I can't train, I am injured and have to heal my injuries first.")
            current_session.clear_time_to_advance()
        else:
            # this is hardcoded to be 10 by default, change if another value is required
            exp_gained = 10
            current_session.main_player.gain_exp(exp_gained)
    jump location_redirect
    
label training_spar:
    # heal the spar partners before the fight
    python:
        for p in current_session.spar:
            p.full_heal()
    
    if len(current_session.spar) == 1:
        current_session.main_player.character "Lets spar [current_session.spar[0].name]."
        current_session.spar[0].character "Lets go."
        call fight(current_session.main_player, current_session.spar[0], [], [], clearing)
    
    if len(current_session.spar) > 1:
        current_session.main_player.character "Lets spar [current_session.spar[0].name] and [current_session.spar[1].name]."
        current_session.spar[0].character "Lets go."
        current_session.spar[1].character "Lets do this."
        call fight(current_session.main_player, current_session.spar[0], [], [current_session.spar[1]], clearing)
    
label village_arena(player, village):
    show screen villagearena(village, player)
    player.character "I need to choose the arena fight."
    $ renpy.call('village_arena', player, village)
    
label village_hospital(player, village):
    # maybe show hospital for each village here
    show screen hospitalshop(village, player)
    player.character "I need to choose items to buy."
    $ renpy.call('village_hospital', player, village)
    
label hospital_injury:
    
    $ injury_bill = player.get_injury_bill()
    "Nurse" "Looks like you are injured."
    "Nurse" "Lets take a look here."
    "Nurse" "....."
    "Nurse" "That will be [injury_bill[0]] Money."
    if current_session.main_player.ryo >= injury_bill[0]:
        current_session.main_player.character "Here."
        $ current_session.main_player.ryo -= injury_bill[0]
        "Nurse" "You can stay here and rest up, we will discharge you once your fully healed."
        $ current_session.main_player.heal_all_injuries()
    else:
        current_session.main_player.character "Sorry, I do not have enough money."
        "Nurse" "I would suggest you heal your minor injuries by resting at home, then once you have enough ryo we can treat you."
        $ current_session.clear_time_to_advance()
    
    jump location_redirect
    
# Example of an active event on a location
label village_jounin_station(player, village):
    
    python:
        if is_event_active_today(e_jounin_training, main_time) and main_time.hour in range(6, 18):
            renpy.jump("event_jounin_training")
            
    "Jounin" "Sorry, no training events today, please come back on the 1st of next month between 6AM and 6PM."
    jump village_redirect
    
label event_jounin_training:
    $ trainer = get_random_jounin(current_session.main_player, current_session.village, exclude_sensei=True)
    $ random_value = renpy.random.randint(1,3)
    if random_value == 1:
        $ new_skill = get_sensei_skill(trainer, current_session.main_player)
        trainer.character "I am about to teach you is [new_skill.name]."
        if new_skill.unlock_exp < 300:
            trainer.character "It is a basic skill but fundamental to being a shinobi."
        elif new_skill.unlock_exp < 600:
            trainer.character "It is an intermediate skill but fundamental to being a shinobi."
        elif new_skill.unlock_exp < 900:
            trainer.character "It is an advanced skill and hard to master."
        # TODO: some sort of explanation
        current_session.main_player.character "[new_skill.name] added to skill set."
    elif random_value == 2:
        trainer.character "This class is about improving general concentration and ninja skills."
        trainer.character "It will take a few hours but I'm sure you will benefit from this greater."
        $ maxhp_increase += renpy.random.randint(5, 10)
        $ maxchakra_increase += renpy.random.randint(5, 10)
        $ exp_increase = renpy.random.randint(10, 30)
        $ current_session.main_player.maxhp += maxhp_increase
        current_session.main_player.character "Max HP increased by [maxhp_increase]."
        $ current_session.main_player.maxchakra += maxchakra_increase
        current_session.main_player.character "Max HP increased by [maxchakra_increase]."
        $ current_session.main_player.gain_exp(exp_increase)
        current_session.main_player.character "Exp increased by [exp_increase]."
    else:
        trainer.character "We will focus on on particular skill today."
        python:
            skill_improve = random.choice(current_session.main_player.all_skills)
            setattr(getattr(current_session.main_player, skill_improve.label), skill_improve.label,  skill_improve.gain_exp(100))
            renpy.say(current_session.main_player.character,  "I have gained 100 exp for {}.".format(skill_improve.name))
        
    $ main_time.advance_time(hours=6)
    jump village_redirect
    
    
label village_police_station(player, village):
    call time_revert
    # maybe show different weapon shop here
    show screen weaponshop(village, player)
    player.character "I need to choose weapons to buy."
    $ renpy.call('village_ninja_tool_facility', player, village)
    
label village_missions(player, village):
    hide screen missionselect
    show screen villagemissions(village, player)
    player.character "I need to choose mission."
    $ renpy.call('village_missions', player, village)
    
label village_home(player, village):
    hide rest_screen
    show screen villagehome(village, player)
    #show screen calendar_screen_toggle
    player.character "I need choose an action."
    $ renpy.call('village_home', player, village)
        
# EXAMPLE of village_arena_label
#label village_arena_level5:
#    call time_revert
#    call injury_revert
#    scene dream_2
#    current_session.main_player.character "Time to fight in the arena."
#    itachi.character "I will be your opponent!"
#    call fight(current_session.main_player, itachi, [], [], clearing)
    
    
####### NPCS / MISSIONS ########
    
            
### NPC LABELS ###

# EXAMPLE OF NPC EVENTS

label sasuke1:
    $ sasuke.npc_event.count += 1
    $ time_tag_show("leaf_1")
    current_session.main_player.character "Hi Sasuke, we are meeting the first time."
    # TODO: character sprites??
    sasuke.character "How is it going."
    " " "We eat ramen at the ramen shop."
    $ bond_increase = renpy.random.randint(10, 15)
    $ sasuke.bond += bond_increase
    current_session.main_player.character "My bond with Sasuke goes up by [bond_increase]."
    jump village_redirect
    
label sasuke2:
    $ sasuke.npc_event.count += 1
    $ time_tag_show("leaf_1")
    $ sasuke.npc_event.stop = True
    current_session.main_player.character "Hi Sasuke, we are meeting the second time."
    sasuke.character "How is it going."
    " " "We eat ramen at the ramen shop."
    $ bond_increase = renpy.random.randint(10, 15)
    $ sasuke.bond += bond_increase
    current_session.main_player.character "My bond with Sasuke goes up by [bond_increase]."
    jump village_redirect