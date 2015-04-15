# This file is in the public domain. Feel free to modify it as a basis
# for your own screens.

##############################################################################
# CHARACTER CREATION
#

screen allocatepoints(player):
    add "hero_hud" xpos 0.15 ypos 0.30
    
    $ STATS = ['strength', 'speed', 'evasion', 'defence', 'stamina', 'melee', 'special', 'ranged']
    $ counter = 0
    text "Allocation Points: [player.allocation_points]" xpos 0.35 ypos 0.20
    
    if player.allocation_points:
        for stat in STATS:
            $ player_stat = getattr(player, stat)
            $ cap_stat = stat.capitalize()
            textbutton "[cap_stat] [player_stat] (+1)" hovered Show('explanation', stat=stat) unhovered Hide('explanation') action [SetField(player, stat, getattr(player, stat) + 1), 
                                                                                                                                    SetField(player, 'allocation_points', getattr(player, 'allocation_points') - 1), 
                                                                                                                                    SetField(current_session, 'main_player', player), 
                                                                                                                                    Jump('allocate_points')] xpos (grid_place[counter][0] + 0.1) ypos grid_place[counter][1]
            $ counter +=1
            
        textbutton "Reset stats" action Jump('reset_allocation_points') xpos (grid_place[counter][0] + 0.1) ypos grid_place[counter][1]
            
screen explanation(stat):
    
    $ stat_dict = {'strength': "Damage dealt with attacks do.",
                   'speed': "Distance the player can cover per move.",
                   'evasion': "Chance of dodging the opponents attack.",
                   'defence': "Resistance against all types of attacks.",
                   'stamina': "Rate of recovering and endurance.",
                   'melee': "Proficiency in close combat.",
                   'special': "Proficiency in mana skills.",
                   'ranged': "Proficiency in ranged combat."}
    
    $ message = stat_dict[stat]
    
    text "[message]" xpos 0.15 ypos 0.75
    

##############################################################################
# VILLAGE / LOCATION SCREENS
#
screen villagearena(village, player):
    $ counter = 0
    textbutton "Level 5" action [SetField(current_session, 'village', village), 
                                 SetField(current_session, 'main_player', player),
                                 SetField(current_session, 'time_to_advance', {'hours': 8}),
                                 Hide("villagearena"),
                                 Jump('village_arena_level5')] xpos grid_place[0][0] ypos grid_place[0][1]
    
    textbutton "Level 10" action [SetField(current_session, 'village', village), 
                                  SetField(current_session, 'main_player', player),
                                  SetField(current_session, 'time_to_advance', {'hours': 8}),
                                  Hide("villagearena"),
                                  Jump('village_arena_level10')] xpos grid_place[1][0] ypos grid_place[1][1]
    
    textbutton "Back" action [SetField(current_session, 'village', village), 
                              SetField(current_session, 'main_player', player),
                              Hide("villagearena"),
                              Jump('village_redirect')] xpos grid_place[2][0] ypos grid_place[2][1]
            
screen hospitalshop(village, player):
    $ counter = 1
    $ injury_bill = player.get_injury_bill()
    $ sorted_items = sorted(hospital_shop.items)
    text "Money: [player.ryo]" xpos 0.05
    
    imagebutton idle "black_fade_inventory" hover "black_fade_inventory" xpos 0.68 ypos 0.28
    vbox xpos 0.7 ypos 0.3:
        for item in sorted_items:
            text "[item.name] [item.quantity]"
    
    python:
        if is_event_active_today(e_hospital_discount) and not hospital_shop.price_halved:
            hospital_shop.half_prices()
        elif not is_event_active_today(e_hospital_discount) and hospital_shop.price_halved:
            hospital_shop.double_prices()
    
    if injury_bill[0]:
        textbutton "Heal all injuries ([injury_bill[0]]) ([injury_bill[1]] days rest)" action [SetField(current_session, 'village', village), 
                                                                                               SetField(current_session, 'main_player', player),
                                                                                               SetField(current_session, 'time_to_advance', {'days': injury_bill[1]}),
                                                                                               SetField(current_session, 'rest', True),
                                                                                               Hide("hospitalshop"),
                                                                                               Jump('hospital_injury')] xpos (grid_place[0][0] - 0.1) ypos grid_place[0][1]
    else:
        $ counter = 0
    
    for item in hospital_shop.items:
        textbutton "[item.name] ([item.price])" action [SetField(current_session, 'village', village), 
                                                        SetField(current_session, 'main_player', player),
                                                        SetField(current_session, 'item', item),
                                                        SetField(current_session, 'time_to_advance', {'hours': 2}),
                                                        Jump("purchase_item_redirect")] xpos (grid_place[counter][0] - 0.1) ypos grid_place[counter][1]
        $ counter += 1
                                         
    textbutton "Back to Location select" action [SetField(current_session, 'village', village), 
                                                 SetField(current_session, 'main_player', player), 
                                                 Hide("hospitalshop"),
                                                 Jump('village_redirect')] xpos (grid_place[counter][0] - 0.1) ypos grid_place[counter][1]
    
screen weaponshop(village, player):
    $ counter = 0
    text "Money: [player.ryo]" xpos 0.05
    $ sort_weapons = sorted(player.weapons)
    
    imagebutton idle "black_fade_inventory" hover "black_fade_inventory" xpos 0.68 ypos 0.28
    vbox xpos 0.7 ypos 0.3:
        for weapon in sort_weapons:
            text "[weapon.name] [weapon.quantity]"
    
    python:
        if is_event_active_today(e_weapon_discount) and not weapon_shop.price_halved:
            weapon_shop.half_prices()
        elif not is_event_active_today(e_weapon_discount) and weapon_shop.price_halved:
            weapon_shop.double_prices()
    
    for weapon in weapon_shop.items:
        textbutton "[weapon.name] ([weapon.price])" action [SetField(current_session, 'village', village), 
                                                            SetField(current_session, 'main_player', player),
                                                            SetField(current_session, 'item', weapon),
                                                            SetField(current_session, 'time_to_advance', {'hours': 2}),
                                                            Jump("purchase_weapon_redirect")] xpos grid_place[counter][0] ypos grid_place[counter][1]
        $ counter += 1
                                         
    textbutton "Back to Location select" action [SetField(current_session, 'village', village), 
                                                 SetField(current_session, 'main_player', player), 
                                                 Hide("weaponshop"),
                                                 Jump('village_redirect')] xpos grid_place[counter][0] ypos grid_place[counter][1]
            
screen villagemissions(village, player):
    $ counter = 0
    $ village_time = 0
    $ mission_levels = [('D', 1), ('C', 1), ('B', 30), ('A', 40), ('S', 50)]
    #$ player.level = 40
    $ avaliable_missions = [mission[0] for mission in mission_levels if player.level >= mission[1]]
    
    for rank in avaliable_missions:
        textbutton "[rank]" action [SetField(current_session, 'village', village), 
                                    SetField(current_session, 'main_player', player), 
                                    SetField(current_session, 'mission_rank', rank),
                                    Hide("villagemissions"),
                                    Jump("missionselect_redirect")] xpos grid_place[counter][0] ypos grid_place[counter][1]
        $ counter += 1
        
    textbutton "Back to Location select" action [SetField(current_session, 'village', village), 
                                                 SetField(current_session, 'main_player', player), 
                                                 Hide("villagemissions"),
                                                 Jump('village_redirect')] xpos grid_place[counter][0] ypos grid_place[counter][1]
    
screen missionselect(village, player, rank):
    $ counter = 0
    $ missions = [mission for mission in ALL_MISSIONS if mission.rank == rank]
    
    for mission in missions:
        if not mission.success:
            textbutton "[mission.name]" action [SetField(current_session, 'village', village), 
                                                SetField(current_session, 'main_player', player), 
                                                SetField(current_session, 'mission', mission),
                                                Hide("missionselect"),
                                                Jump("mission_redirect")] xpos grid_place[counter][0] ypos grid_place[counter][1]
        $ counter += 1
    
    textbutton "Back" action [SetField(current_session, 'village', village), 
                              SetField(current_session, 'main_player', player),
                              Hide("missionselect"),
                              Jump('location_redirect')] xpos grid_place[counter][0] ypos grid_place[counter][1]
    

screen training(village, player):
    textbutton "Train skills" action [Hide("training"), Show("train_skills", village=village, player=player)] xpos grid_place[0][0] ypos grid_place[0][1]
    if player.team:
        # maybe add formation, TODO
        text "Team Chemistry: [player.team.chemistry]" xpos 0.4 ypos 0.1
        textbutton "Train with team" action [SetField(current_session, 'village', village), 
                                             SetField(current_session, 'main_player', player), 
                                             Hide("training"), 
                                             Show("train_with_team", village=village, player=player)] xpos grid_place[2][0] ypos grid_place[2][1]
    if player.sensei:
        textbutton "Learn skills" action [SetField(current_session, 'village', village), 
                                          SetField(current_session, 'main_player', player), 
                                          Hide("training"), 
                                          Jump("training_sensei")] xpos grid_place[3][0] ypos grid_place[3][1]
                                      
    textbutton "Train (+ exp)" action [SetField(current_session, 'time_to_advance', {'hours': 4}),
                                       SetField(current_session, 'village', village), 
                                       SetField(current_session, 'main_player', player), 
                                       Hide("training"), 
                                       Jump('train_gain_exp')] xpos grid_place[1][0] ypos grid_place[1][1]
    
    textbutton "Back to Location select" action [SetField(current_session, 'village', village), 
                                                 SetField(current_session, 'main_player', player), 
                                                 Hide('training'), 
                                                 Jump('village_redirect')] xpos grid_place[4][0] ypos grid_place[4][1]
    
screen train_with_team(village, player):
    $ team_length = len(player.team.members)
    # TODO: maybe add player + team member vs others (drag and drop?)
    if team_length > 0:
        textbutton "Spar with [player.team.members[0].name]" action [SetField(current_session, 'time_to_advance', {'hours': 4}),
                                                                     SetField(current_session, 'village', village), 
                                                                     SetField(current_session, 'main_player', player), 
                                                                     SetField(current_session, 'spar', [player.team.members[0]]),
                                                                     Hide("train_with_team"), 
                                                                     Jump("training_spar")] xpos grid_place[0][0] ypos grid_place[0][1]
    if team_length > 1:
        textbutton "Spar with [player.team.members[0].name] and [player.team.members[1].name] (1 on 2)" action [SetField(current_session, 'time_to_advance', {'hours': 4}),
                                                                     SetField(current_session, 'village', village), 
                                                                     SetField(current_session, 'main_player', player), 
                                                                     SetField(current_session, 'spar', player.team.members),
                                                                     Hide("train_with_team"), 
                                                                     Jump("training_spar")] xpos grid_place[1][0] ypos grid_place[1][1]  
    if player.sensei:
        textbutton "Spar with [player.sensei.name]" action [SetField(current_session, 'time_to_advance', {'hours': 4}),
                                                                     SetField(current_session, 'village', village), 
                                                                     SetField(current_session, 'main_player', player), 
                                                                     SetField(current_session, 'spar', [player.sensei]),
                                                                     Hide("train_with_team"), 
                                                                     Jump("training_spar")] xpos grid_place[2][0] ypos grid_place[2][1]
        
    textbutton "Back" action [SetField(current_session, 'village', village), 
                              SetField(current_session, 'main_player', player),
                              Hide("train_with_team"),
                              Jump('location_redirect')] xpos grid_place[3][0] ypos grid_place[3][1]
    
    
screen train_skills(village, player):
    $ counter = 0
    #text "[player.all_skills[0]]" xpos 0.5 ypos 0.5
    for skill in player.all_skills:
        if skill.exp < skill.unlock_exp:
            textbutton "[skill.name] [skill.exp]/[skill.unlock_exp]" action [SetField(current_session, 'village', village), 
                                                                             SetField(current_session, 'main_player', player), 
                                                                             SetField(current_session, 'skill', skill),
                                                                             SetField(current_session, 'time_to_advance', {'hours': 4}),
                                                                             Hide("train_skills"),
                                                                             Jump("train_skill_label")] xpos grid_place[counter][0] ypos grid_place[counter][1]
            $ counter += 1
            
    textbutton "Back" action [SetField(current_session, 'village', village), 
                              SetField(current_session, 'main_player', player),
                              Hide("train_skills"),
                              Jump('location_redirect')] xpos grid_place[counter][0] ypos grid_place[counter][1]

screen levelup(village, player):
    $ STATS = ['strength', 'speed', 'evasion', 'defence', 'stamina', 'melee', 'special', 'ranged']
    $ counter = 0
    
    if player.allocation_points:
        for stat in STATS:
            textbutton "[stat] +1" action [SetField(player, stat, getattr(player, stat) + 1), 
                                           SetField(player, 'allocation_points', getattr(player, 'allocation_points') - 1), 
                                           SetField(current_session, 'village', village), 
                                           SetField(current_session, 'main_player', player), 
                                           Jump('location_redirect')] xpos grid_place[counter][0] ypos grid_place[counter][1]
            $ counter +=1 
    else:
        text "No allocation points" xpos 0.5 ypos 0.5
    textbutton "Back to Location select" action [SetField(current_session, 'village', village), 
                                                 SetField(current_session, 'main_player', player), 
                                                 Hide('levelup'), 
                                                 Jump('village_redirect')] xpos grid_place[counter][0] ypos grid_place[counter][1]

screen villagetravel(village, player):
    $ counter = 0
    $ village_time = 0
    
    for v in other_villages(village):
        $ village_time = time_between_village(v, village)
        textbutton "[v.name] [village_time]" action [SetField(current_session, 'village', v), 
                                                     SetField(current_session, 'main_player', player), 
                                                     SetField(current_session, 'time_to_advance', {'days': village_time}),
                                                     Hide('villagetravel'),
                                                     Jump('village_redirect')] xpos grid_place[counter][0] ypos grid_place[counter][1]
        $ counter += 1
        
    textbutton "Back to Location select" action [SetField(current_session, 'village', village), 
                                                 SetField(current_session, 'main_player', player), 
                                                 Hide('villagetravel'),
                                                 Jump('village_redirect')] xpos grid_place[counter][0] ypos grid_place[counter][1]

screen villagehome(village, player):
    $ counter = 0
    
    textbutton "Show Calendar" action [SetField(current_session, 'village', village), 
                                       SetField(current_session, 'main_player', player), 
                                       Hide('villagehome'),
                                       Show('calendar_screen', player=player, village=village, current_month=get_current_month())] xpos grid_place[0][0] ypos grid_place[0][1]
    
    textbutton "Rest" action [SetField(current_session, 'village', village), 
                              SetField(current_session, 'main_player', player), 
                              Hide('villagehome'),
                              Show('rest_screen', player=player, village=village)] xpos grid_place[1][0] ypos grid_place[1][1]
        
    textbutton "Back to Location select" action [SetField(current_session, 'village', village), 
                                                 SetField(current_session, 'main_player', player), 
                                                 Hide('villagehome'),
                                                 Jump('village_redirect')] xpos grid_place[2][0] ypos grid_place[2][1]
    
screen rest_screen(village, player):
    
    textbutton "1 Hour" action [SetField(current_session, 'village', village), 
                                SetField(current_session, 'main_player', player),
                                SetField(current_session, 'time_to_advance', {'hours': 1}),
                                SetField(current_session, 'rest', True),
                                Hide("rest_screen"),
                                Jump('location_redirect')] xpos grid_place[0][0] ypos grid_place[0][1]
    
    textbutton "2 Hours" action [SetField(current_session, 'village', village), 
                                 SetField(current_session, 'main_player', player),
                                 SetField(current_session, 'time_to_advance', {'hours': 2}),
                                 SetField(current_session, 'rest', True),
                                 Hide("rest_screen"),
                                 Jump('location_redirect')] xpos grid_place[1][0] ypos grid_place[1][1]
    
    textbutton "12 Hours" action [SetField(current_session, 'village', village), 
                                  SetField(current_session, 'main_player', player),
                                  SetField(current_session, 'time_to_advance', {'hours': 12}),
                                  SetField(current_session, 'rest', True),
                                  Hide("rest_screen"),
                                  Jump('location_redirect')] xpos grid_place[2][0] ypos grid_place[2][1]
    
    textbutton "1 Day" action [SetField(current_session, 'village', village), 
                               SetField(current_session, 'main_player', player),
                               SetField(current_session, 'time_to_advance', {'days': 1}),
                               SetField(current_session, 'rest', True),
                               Hide("rest_screen"),
                               Jump('location_redirect')] xpos grid_place[3][0] ypos grid_place[3][1]
    
    textbutton "1 Week" action [SetField(current_session, 'village', village), 
                                SetField(current_session, 'main_player', player),
                                SetField(current_session, 'time_to_advance', {'days': 7}),
                                SetField(current_session, 'rest', True),
                                Hide("rest_screen"),
                                Jump('location_redirect')] xpos grid_place[4][0] ypos grid_place[4][1]
    
    textbutton "1 Month" action [SetField(current_session, 'village', village), 
                                 SetField(current_session, 'main_player', player),
                                 SetField(current_session, 'time_to_advance', {'months': 1}),
                                 SetField(current_session, 'rest', True),
                                 Hide("rest_screen"),
                                 Jump('location_redirect')] xpos grid_place[5][0] ypos grid_place[5][1]
    
    textbutton "Back" action [SetField(current_session, 'village', village), 
                              SetField(current_session, 'main_player', player),
                              Hide("rest_screen"),
                              Jump('location_redirect')] xpos grid_place[6][0] ypos grid_place[6][1]

screen villagemap(village, player):
    # show player time details here
    $ counter = 0
    $ npc_counter = 0
    $ x_adj = 0.05
    $ npc_x_adj = 0.2
    
    for today_e in get_today().events:
        if today_e.npc and not today_e.stop:
            textbutton today_e.npc.name action [SetField(current_session, 'main_player', player), 
                                                SetField(current_session, 'village', village), 
                                                SetField(current_session, 'time_to_advance', {'hours': 4}),
                                                Hide("villagemap"), 
                                                Jump(today_e.label.format(today_e.count))] xpos (grid_place[npc_counter][0]-npc_x_adj) ypos grid_place[npc_counter][1]
            $ npc_counter += 1
    
    for location in village.locations:
        if location.unlocked:
            textbutton "[location.name]" hovered Show('location_explanation', stat=location.label) unhovered Hide('location_explanation') action [SetField(current_session, 'main_player', player), 
                                                                                                                                    SetField(current_session, 'village', village), 
                                                                                                                                    SetField(current_session, 'location', location),
                                                                                                                                    Hide("location_explanation"),
                                                                                                                                    Hide("villagemap"), 
                                                                                                                                    Jump('location_redirect')] xpos grid_place[counter][0] ypos grid_place[counter][1]
        
        # show events next to buttons
        if location.events:
            for e in location.events:
                for today_e in get_today().events:
                    if e.small_name == today_e.small_name and counter < 5:
                        text "[e.small_name]" xpos (grid_place[counter][0]-x_adj) ypos grid_place[counter][1]
                    elif e.small_name == today_e.small_name and counter >= 5:
                        text "[e.small_name]" xpos (grid_place[counter][0]-x_adj) ypos grid_place[counter][1]
            
        $ counter += 1 
                
screen location_explanation(stat):
    $ expl_dict = {'village_hospital': 'Heal injuries and buy healing items.', 
                   'village_police_station': ' '*60 + 'Buy weapons for combat.', 
                   'village_levelup': 'Spend points to increase stats like strength, speed, evasion etc.',
                   'village_training': 'Train with team members, learn new skills, unlock new skills.', 
                   'village_missions': ' '*65 + 'Perform missions.', 
                   'village_home': 'Rest to heal injuries, skip time or view calendar for upcoming events.'}
    $ expl = expl_dict[stat]
    
    imagebutton idle "black_fade_text" hover "black_fade_text" xpos 0.15 ypos 0.65
    hbox xmaximum 500 yminimum 200 xpos 0.10 ypos 0.6:
        text "[expl]" ypos 0.8 xpos 0.1
        
screen time_screen:
    imagebutton idle "black_fade_time" hover "black_fade_time" xpos 0 ypos 0.0
    text "[main_time.current_time]" xpos 0 ypos 0.04
        
screen stats_screen(player):
    
    if screen_on:
        imagebutton idle "stats_idle" hover "stats_idle" xpos 0.38 ypos 0.0
        imagebutton idle "body" hover "body" xpos 0.62 ypos 0.00
    
        if player.head.injury:
            imagebutton idle "head_injured" hover "head_injured" xpos 0.655 ypos 0.01
        
        if player.torso.injury:
            imagebutton idle "torso_injured" hover "torso_injured" xpos 0.662 ypos 0.055
        
        if player.left_arm.injury:
            imagebutton idle "left_arm_injured" hover "left_arm_injured" xpos 0.634 ypos 0.05
        
        if player.right_arm.injury:
            imagebutton idle "right_arm_injured" hover "right_arm_injured" xpos 0.701 ypos 0.05
        
        if player.left_leg.injury:
            imagebutton idle "left_leg_injured" hover "left_leg_injured" xpos 0.645 ypos 0.145
        
        if player.right_leg.injury:
            imagebutton idle "right_leg_injured" hover "right_leg_injured" xpos 0.685 ypos 0.145
    
        text "{size=-10}Ryo: [player.ryo]{/size}" xpos 0.73 ypos 0.023
        text "{size=-10}HP: [player.hp]/[player.maxhp]{/size}" xpos 0.85 ypos 0.024
        text "{size=-10}[player.name]{/size}" xpos 0.73 ypos 0.05
        text "{size=-10}Lv.[player.level]{/size}" xpos 0.83 ypos 0.05
        $ next_level_exp = LEVELS[player.level + 1]
        text "{size=-10}Exp [player.exp]/[next_level_exp]{/size}" xpos 0.73 ypos 0.08
        text "{size=-10}CP: [player.chakra]/[player.maxchakra]{/size}" xpos 0.87 ypos 0.08
        text "{size=-10}Str: [player.strength]{/size}" xpos 0.735 ypos 0.12
        text "{size=-10}Def: [player.defence]{/size}" xpos 0.735 ypos 0.16
        text "{size=-10}Eva: [player.evasion]{/size}" xpos 0.735 ypos 0.20
        text "{size=-10}Sta: [player.stamina]{/size}" xpos 0.83 ypos 0.12
        text "{size=-10}Spd: [player.speed]{/size}" xpos 0.83 ypos 0.16
        text "{size=-10}Hit: [player.base_hit_rate]{size=-5}" xpos 0.83 ypos 0.20
        text "{size=-10}Mel: [player.melee]{/size}" xpos 0.915 ypos 0.12
        text "{size=-10}Spe: [player.special]{/size}" xpos 0.915 ypos 0.16
        text "{size=-10}Ran: [player.ranged]{/size}" xpos 0.915 ypos 0.20
    
        textbutton "Hide Stats" action [Hide("stats_screen"), Jump("toggle_screen_off")] xpos 0.4 ypos 0.0
    
screen player_stats:
    if not screen_on:
        textbutton "Show Stats" action [Show("stats_screen", player=current_session.main_player), Jump("toggle_screen_on")] xpos 0.4 ypos 0.0
        
screen calendar_screen_toggle:
    if not calendar_on:
        textbutton "Show Calendar" action Jump("toggle_calendar_on") xpos 0.2 ypos 0.0
        
screen calendar_screen(village, player, current_month):
    $ stuff = [(d.day, d.month) for d in e_chunin_exams.date_range()]

    imagebutton idle "black_fade" hover "black_fade"
    
    textbutton "Last month" action [Hide('calendar_screen'), 
                                    Show('calendar_screen', village=village, player=player, current_month=get_month(current_month.number - 1))] xpos 0.15 ypos 0.1
    text "[current_month]" xpos 0.43 ypos 0.11
    textbutton "Next month" action [Hide('calendar_screen'), 
                                    Show('calendar_screen', village=village, player=player, current_month=get_month(current_month.number + 1))] xpos 0.65 ypos 0.1
    
    grid 6 5 spacing -200 ypos 0.2 xpos 0.15 xfill True yfill True:
        for day in current_month.days:
            $ how_many = day.parse_events()
            
            if main_time.day == day.number and current_month.number == main_time.month:
                text "[day.number]\n([how_many])" color "#F00"
            else:
                text "[day.number]\n([how_many])" 
                    
    textbutton "Hide Calendar" action [Hide('calendar_screen'), Show("villagehome", player=player, village=village)] xpos 0.2 ypos 0.0

label toggle_screen_on:
    $ screen_on = True
    python:
        if current_session.location:
            renpy.jump("location_redirect")
        else:
            renpy.jump("village_redirect")
    
label toggle_screen_off:
    $ screen_on = False
    python:
        if current_session.location:
            renpy.jump("location_redirect")
        else:
            renpy.jump("village_redirect")
            
label toggle_calendar_on:
    $ calendar_on = True
    hide screen villagemap
    python:
        renpy.jump("village_redirect")
    
label toggle_calendar_off:
    $ calendar_on = False
    python:
        renpy.jump("village_redirect")

#############################################################################
# MISC
#
screen announce(message):
    text "{color=#000}{font=domai.ttf}{size=60}[message]{/size}{/font}{/color}" xpos 0.13 ypos 0.4


##############################################################################
# WORLD EVENTS
#
screen worldevents(village):
    add village.leader.picname xpos 0.01 ypos 0.1 
        

##############################################################################
# BATTLE SCREENS
#
screen battle_selection_screen(battles):
    for battle in battles:
        text "[battle.good_team]" xpos battle.xpos ypos battle.ypos
    

screen battle_prep_screen:

    $ start = 50
    $ counter = 1
    $ battle_c = 1
    $ drag_c = 1
    $ team = current_session.team.members
    $ battles = current_session.battles
    
    for battle in battles:
        imagebutton idle "black_fade_battle" hover "black_fade_battle" xpos (170*battle_c) ypos 0.1
        vbox xmaximum 100 ymaximum 200 xpos (170*battle_c) ypos 0.1:
            for p in battle.bad_team:
                text "[p.name] [p.hp]/[p.maxhp]"
                
        imagebutton idle "black_fade_battle" hover "black_fade_battle" xpos (170*battle_c) ypos 0.5 
        vbox xmaximum 100 ymaximum 200 xpos (170*battle_c) ypos 0.5:
            for p in battle.good_team:
                text "[p.name] [p.hp]/[p.maxhp]"
                
        $ battle_c += 1
    
    textbutton "Reset" action [Hide('battle_prep_screen'), 
                               Jump('reset_battle')] xpos 0.8
    textbutton "Done" action [Hide('battle_prep_screen'), Jump('battle_start')] xpos 0.7

    draggroup:
        for p in current_session.team.members:
            drag:
                drag_name p.name
                child p.tilepic
                droppable False
                dragged player_dragged
                xpos (50*counter) ypos 200
                
            $ counter += 1
                
        for battle in current_session.battles:
            drag:
                drag_name battle.id
                child "marker.png"
                draggable False
                xpos (200*drag_c) ypos 260
                
            $ drag_c += 1


screen skill_actions(action_type):
    $ initial_pos = 0.8
    $ interval = 0.1
    $ counter = 1
    $ start = 300
    $ x_pos = 118
    
    vbox:
        for skill in getattr(player, action_type):
            
            $ skill_display_name = "{}".format(skill.name)
            if skill.skill_type == 'weapon':
                $ skill_display_name += " {}".format(skill.quantity)
            
            if skill.is_usable(player, enemy):
                textbutton "[skill_display_name]" action [SetField(current_session, 'skill', skill), 
                                                          SetField(current_session, 'skill_type', skill.skill_type),
                                                          Jump('skill_redirect')] xpos (x_pos*counter) ypos (start - (counter*41))
                    
            else:
                $ reason = skill.unusable_reason(player, enemy)
                # show another type of imagebutton here
                textbutton "[skill_display_name]" hovered Show('move_explanation', reason=reason) unhovered Hide('move_explanation') action [[]] xpos (x_pos*(counter*2))  ypos (start - (counter*41))
            

            $ counter += 1
            
        textbutton "Back" action [Hide('skill_actions'), Show('battlemenu', player=player, tag_p=tag_p)] xpos (x_pos*1) ypos (350 - (counter*41))
        
screen item_actions:
    $ initial_pos = 0.8
    $ interval = 0.1
    $ counter = 1
    $ start = 300
    $ x_pos = 118
    
    vbox:
        for item in player.items:
            
            if item.quantity > 0:
                textbutton "[item.name] [item.quantity]" action [SetField(current_session, 'item', item), 
                                                                 SetField(current_session, 'main_player', player),
                                                                 Jump('item_redirect')] xpos (x_pos*counter*2) ypos (start - (counter*41))
                    
            else:
                textbutton "[item.name] [item.quantity]" action [[]] xpos (x_pos*(counter*2)) ypos (start - (counter*41))
            
            $ counter += 1
            
        textbutton "Back" action [Hide('item_actions'), Show('battlemenu', player=player, tag_p=tag_p)] xpos (x_pos*1) ypos (350 - (counter*41))

screen battlemenu(player, tag_p):
    $ move_types = ["melee", "special", "ranged", "weapons", "defensive"]
    $ counter = 1
    $ start = 300
    $ x_pos = 118
    vbox:
        for move_type in move_types:
            $ capital = move_type.capitalize()
            if move_type == "weapons":
                $ player_atr = "weapons"
                $ capital = "Weapon"
            else:
                $ player_atr = move_type + "skills"
                
            if getattr(player, player_atr):
                textbutton "[capital]" hovered Show('battle_explanation', stat=move_type) unhovered Hide('battle_explanation') action [Hide('battlemenu'), Hide("battle_explanation"), Show("skill_actions", action_type=player_atr)] xpos (counter*x_pos) ypos  (start - (counter*41))
            else:
                textbutton "[capital]" xpos (x_pos*counter) ypos (start - (counter*41))

            $ counter += 1
       
        if not moved:
            textbutton "Move" hovered Show('battle_explanation', stat='move') unhovered Hide('battle_explanation') action [Hide("skill_actions"), Show("movemenu")] xpos 355 ypos 100
        else:
            textbutton "Move" xpos 355 ypos 100
            
        textbutton "Standby" hovered Show('battle_explanation', stat='standby') unhovered Hide('battle_explanation') action Jump("standby") xpos 236 ypos 59
        
        if player.items:
            textbutton "Items" hovered Show('battle_explanation', stat='items') unhovered Hide('battle_explanation') action [Hide('battlemenu'), Hide("battle_explanation"), Show("item_actions")]  xpos 471 ypos 18
        else:
            textbutton "Items" xpos 471 ypos 18
        
        for partner in tag_p:
            textbutton "Tag [partner.name]" action [SetField(partner, 'main', True), SetField(partner, 'tile', player.tile), SetField(player, 'main', False), Jump('tag_partner')] ypos -6.5
        
screen move_explanation(reason):
    text "[reason]" ypos 0.85 xpos 0.2
        
screen battle_explanation(stat):
    $ expl_dict = {'melee': 'Close ranged attacks.', 
                   'special': 'Attacks that use magic.', 
                   'ranged': 'Attacks from distance.',
                   'move': 'Move across the battle area.', 
                   'move_once': 'Can only move once per turn',
                   'weapons': 'Fixed damage attacks limited by quantity.', 
                   'items': 'Heal HP or MP', 
                   'defensive': 'Reduce enemy damage for a limited amount of time.',
                   'standby': 'Regain magic, slightly heal health.'}
    $ expl = expl_dict[stat]
    
    text "[expl]" ypos 0.85 xpos 0.2
        
screen stats:
    text "Str: [player.strength] Def: [player.defence] Eva: [player.evasion]" xpos 0.30
    text "Sta: [player.stamina] Hit: [player.base_hit_rate]" xpos 0.30 ypos 0.05
    text "Str: [enemy.strength] Def: [enemy.defence] Eva: [enemy.evasion]" xpos 0.65
    text "Sta: [enemy.stamina] Hit: [enemy.base_hit_rate]" xpos 0.65 ypos 0.05
        
screen battlebars(tag_p, tag_e):
    
    $ rel_pos = abs(player.tile.position - enemy.tile.position)
    $ player_centered = player.name.center(10, ' ')
    $ enemy_centered = enemy.name.center(10, ' ')
    
    # Show middle text / battle info
    text "{color=#FFF}Round [battle_turn]{/color}" xpos 0.43 ypos 0.05
    text "{size=-5}{color=#FFF}[player_centered]{/color}{/size}" xpos 0.43 ypos 0.10
    text "{size=-5}{color=#FFF}vs{/color}{/size}" xpos 0.47 ypos 0.15
    text "{size=-5}{color=#FFF}[enemy_centered]{/color}{/size}" xpos 0.43 ypos 0.20
    
    # Player HUD
    imagebutton idle player.hudpic hover player.hudpic xpos 0.16 ypos 0.06 #action NullAction()
    text "{size=-5}{color=#FFF}HP{/color}{/size}" xpos 0.10 ypos 0.3
    text "{size=-5}{color=#FFF}MP{/color}{/size}" xpos 0.10 ypos 0.35
    bar value player.hp range player.maxhp xpos 0.15 ypos 0.30 xmaximum 150 #ymaximum 30 left_bar "blue_bar"
    text "{size=-5}{color=#FFF}[player.hp]/[player.maxhp]{/color}{/size}" xpos 0.35 ypos 0.3
    text "{size=-5}{color=#FFF}[player.chakra]/[player.maxchakra]{/color}{/size}" xpos 0.35 ypos 0.35
    bar value player.chakra range player.maxchakra xpos 0.15 ypos 0.35 xmaximum 150
    
    # If skills active show (these will overlap warning)
    if player.check_active_skill(damage_reduction):
        text "DR" xpos 0.3 ypos 0.15
        
    if player.check_active_skill(chakra_defence):
        text "CD" xpos 0.3 ypos 0.15
        
    if player.check_active_skill(reflect):
        text "Ref" xpos 0.3 ypos 0.15
        
    if player.check_active_skill(dampen):
        text "Dam" xpos 0.3 ypos 0.15
        
    if player.check_active_skill(yata_mirror):
        text "Yata" xpos 0.3 ypos 0.15
    
    # Enemy HUD
    imagebutton idle enemy.hudpic hover enemy.hudpic xpos 0.66 ypos 0.06
    text "{size=-5}{color=#FFF}HP{/color}{/size}" xpos 0.60 ypos 0.3
    text "{size=-5}{color=#FFF}MP{/color}{/size}" xpos 0.60 ypos 0.35
    text "{size=-5}{color=#FFF}[enemy.hp]/[enemy.maxhp]{/color}{/size}" xpos 0.85 ypos 0.3
    text "{size=-5}{color=#FFF}[enemy.chakra]/[enemy.maxchakra]{/color}{/size}" xpos 0.85 ypos 0.35
    bar value enemy.hp range enemy.maxhp xpos 0.65 ypos 0.30 xmaximum 150
    bar value enemy.chakra range enemy.maxchakra xpos 0.65 ypos 0.35 xmaximum 150
        
    # If skills active show (these will overlap warning)
    if enemy.check_active_skill(damage_reduction):
        text "DR" xpos 0.75 ypos 0.15
        
    if enemy.check_active_skill(chakra_defence):
        text "CD" xpos 0.75 ypos 0.15

    
    # Show tiles
    $ highlight_position(player, enemy, clearing)
    
    for tile in current_session.stage.tiles:
        imagebutton idle current_session.stage.base_texture hover current_session.stage.base_texture xpos (tile.pos.xpos - 25) ypos (tile.pos.ypos - 0.05)
        
    # show tag partners health here (player)
    for position, partner in enumerate(tag_p):
        if position == 0:
            text "{size=-5}[partner.name]{/size}" xpos 0.02 ypos 0.80
            text "{size=-5}[partner.hp]/[partner.maxhp]{/size}" xpos 0.02 ypos 0.84
            #vbar value partner.hp range partner.maxhp xpos 0.05 ypos 0.80 ymaximum 100
            #bar value partner.chakra range partner.maxchakra xpos 0.25 ypos 0.8 xmaximum 100 
        else:
            text "{size=-5}[partner.name]{/size}" xpos 0.02 ypos 0.90
            text "{size=-5}[partner.hp]/[partner.maxhp]{/size}" xpos 0.02 ypos 0.94
            #bar value partner.hp range partner.maxhp xpos 0.2 ypos 0.95 xmaximum 100 
            #bar value partner.chakra range partner.maxchakra xpos 0.35 ypos 0.8 xmaximum 100 
        
    # show tag partners health here (enemy)
    for position, partner in enumerate(tag_e):
        if position == 0:
            text "{size=-5}[partner.name]{/size}" xpos 0.87 ypos 0.80
            text "{size=-5}[partner.hp]/[partner.maxhp]{/size}" xpos 0.87 ypos 0.84
            #bar value partner.hp range partner.maxhp xpos 0.7 ypos 0.95 xmaximum 100 #xmaximum 20
            #bar value partner.chakra range partner.maxchakra xpos 0.65 ypos 0.8 ymaximum 100 xmaximum 20
        else:
            text "{size=-5}[partner.name]{/size}" xpos 0.87 ypos 0.90
            text "{size=-5}[partner.hp]/[partner.maxhp]{/size}" xpos 0.87 ypos 0.94
            #bar value partner.chakra range partner.maxchakra xpos 0.75 ypos 0.8 ymaximum 100 xmaximum 20

label movemenu:
    show screen movemenu
    
screen movemenu:
    
    $ highlight_position(player, enemy, clearing)
    
    for tile in current_session.stage.tiles:
        if tile.potential:
            imagebutton idle tile.idle hover tile.hover xpos (tile.pos.xpos - 25) ypos (tile.pos.ypos - 0.05) action [SetField(current_session, 'tile', tile),
                                                                                                                      Jump("move_redirect")]
        elif tile.trap:
            imagebutton idle tile.TRAP_TEXTURE hover tile.TRAP_TEXTURE xpos (tile.pos.xpos - 25) ypos (tile.pos.ypos - 0.05)
        else:
            imagebutton idle tile.idle hover tile.idle xpos (tile.pos.xpos - 25) ypos (tile.pos.ypos - 0.05)
    
# These are so tightly coupled with tiles, leaving these here
label move_redirect:
    $ show_player_at_pos(player, enemy, clearing, current_session.tile)
    jump move_continue
    
label move_continue:
    $ moved = True
    call fight(player, enemy, tag_p, tag_e, clearing, win_label, lose_label, draw_label, fight_limit)
    
    
# Tap functionality is in BETA (untested, do not use)
label settrap:
    hide screen movemenu
    show screen settrap
    player.character "Where should I place the trap?"

label trap:
    jump settrap    

screen settrap:
    $ highlight_position(player, enemy, clearing)
    
    for tile in current_session.stage.tiles:
        if tile.potential:
            imagebutton idle tile.idle hover tile.TRAP_TEXTURE xpos (tile.pos.xpos - 25) ypos (tile.pos.ypos - 0.05) action [SetField(current_session, 'tile', tile),
                                                                                                                             Jump("trap_redirect")]
        else:
            imagebutton idle tile.idle hover tile.idle xpos (tile.pos.xpos - 25) ypos (tile.pos.ypos - 0.05)

label trap_redirect:
    $ set_trap_at_pos(player, enemy, clearing, current_session.tile)
    jump enemymove

##### TESTS #####

screen test_results(entity, results):
    add "space"
    vbox xmaximum 600 yminimum 200 xpos 0.10 ypos 0.06:
        text "[entity] Tests"
        for entry in results:
            for description, result in entry.iteritems():
                if result:
                    $ r = 'OK'
                    text "{size=-5}[description]....{color=0f0}[r]{/color}{/size}"
                else:
                    $ r = 'FAIL'
                    text "{size=-5}[description]....{color=f00}[r]{/color}{/size}"

##############################################################################
# Say
#
# Screen that's used to display adv-mode dialogue.
# http://www.renpy.org/doc/html/screen_special.html#say
screen say:

    # Defaults for side_image and two_window
    default side_image = None
    default two_window = False

    # Decide if we want to use the one-window or two-window varaint.
    if not two_window:

        # The one window variant.        
        window:
            id "window"

            has vbox:
                style "say_vbox"

            if who:
                text who id "who"

            # force the color here :(
            text what id "what" color "#fff"

    else:

        # The two window variant.
        vbox:
            style "say_two_window_vbox"

            if who:            
                window:
                    style "say_who_window"

                    text who:
                        id "who"
                        
            window:
                id "window"

                has vbox:
                    style "say_vbox"

                text what id "what"
              
    # If there's a side image, display it above the text.
    if side_image:
        add side_image
    else:
        add SideImage() xalign 0.0 yalign 1.0

    # Use the quick menu.
    use quick_menu


##############################################################################
# Choice
#
# Screen that's used to display in-game menus.
# http://www.renpy.org/doc/html/screen_special.html#choice

screen choice:

    window: 
        style "menu_window"        
        xalign 0.5
        yalign 0.5
        
        vbox:
            style "menu"
            spacing 2
            
            for caption, action, chosen in items:
                
                if action:  
                    
                    button:
                        action action
                        style "menu_choice_button"                        

                        text caption style "menu_choice"
                    
                else:
                    text caption style "menu_caption"

init -2 python:
    config.narrator_menu = True
    
    style.menu_window.set_parent(style.default)
    style.menu_choice.set_parent(style.button_text)
    style.menu_choice.clear()
    style.menu_choice_button.set_parent(style.button)
    style.menu_choice_button.xminimum = int(config.screen_width * 0.75)
    style.menu_choice_button.xmaximum = int(config.screen_width * 0.75)


##############################################################################
# Input
#
# Screen that's used to display renpy.input()
# http://www.renpy.org/doc/html/screen_special.html#input

screen input:

    window style "input_window":
        has vbox

        text prompt style "input_prompt"
        input id "input" style "input_text"

    use quick_menu
        
##############################################################################
# Nvl
#
# Screen used for nvl-mode dialogue and menus.
# http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl:

    window:
        style "nvl_window"

        has vbox:
            style "nvl_vbox"

        # Display dialogue.
        for who, what, who_id, what_id, window_id in dialogue:
            window:
                id window_id

                has hbox:
                    spacing 10

                if who is not None:
                    text who id who_id

                text what id what_id

        # Display a menu, if given.
        if items:

            vbox:
                id "menu"

                for caption, action, chosen in items:

                    if action:

                        button:
                            style "nvl_menu_choice_button"
                            action action

                            text caption style "nvl_menu_choice"

                    else:

                        text caption style "nvl_dialogue"

    add SideImage() xalign 0.0 yalign 1.0
    
    use quick_menu
        
##############################################################################
# Main Menu 
#
# Screen that's used to display the main menu, when Ren'Py first starts
# http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu:

    # This ensures that any other menu screen is replaced.
    tag menu

    # The background of the main menu.
    window:
        style "mm_root"

    # The main menu buttons.
    frame:
        style_group "mm"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Start Game") action Start()
        textbutton _("Run Tests") action Start('run_tests')
        textbutton _("Load Game") action ShowMenu("load")
        textbutton _("Preferences") action ShowMenu("preferences")
        textbutton _("Help") action Help()
        textbutton _("Quit") action Quit(confirm=False)

init -2 python:

    # Make all the main menu buttons be the same size.
    style.mm_button.size_group = "mm"


##############################################################################
# Navigation
#
# Screen that's included in other screens to display the game menu
# navigation and background.
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen navigation:

    # The background of the game menu.
    window:
        style "gm_root"

    # The various buttons.
    frame:
        style_group "gm_nav"
        xalign .98
        yalign .98
        
        has vbox

        textbutton _("Return") action Return()
        textbutton _("Preferences") action ShowMenu("preferences")
        textbutton _("Save Game") action ShowMenu("save")
        textbutton _("Load Game") action ShowMenu("load")
        textbutton _("Main Menu") action MainMenu()
        textbutton _("Help") action Help()
        textbutton _("Quit") action Quit()

init -2 python:
    style.gm_nav_button.size_group = "gm_nav"
    

##############################################################################
# Save, Load
#
# Screens that allow the user to save and load the game.
# http://www.renpy.org/doc/html/screen_special.html#save
# http://www.renpy.org/doc/html/screen_special.html#load

# Since saving and loading are so similar, we combine them into
# a single screen, file_picker. We then use the file_picker screen
# from simple load and save screens.
    
screen file_picker:

    frame:
        style "file_picker_frame"

        has vbox

        # The buttons at the top allow the user to pick a
        # page of files.
        hbox:
            style_group "file_picker_nav"
            
            textbutton _("Previous"):
                action FilePagePrevious()

            textbutton _("Auto"):
                action FilePage("auto")

            textbutton _("Quick"):
                action FilePage("quick")

            for i in range(1, 9):
                textbutton str(i):
                    action FilePage(i)
                    
            textbutton _("Next"):
                action FilePageNext()

        $ columns = 2
        $ rows = 3
                
        # Display a grid of file slots.
        grid columns rows:
            transpose True
            xfill True
            style_group "file_picker"
            
            # Display ten file slots, numbered 1 - 10.
            for i in range(1, columns * rows + 1):

                # Each file slot is a button.
                button:
                    action FileAction(i)
                    xfill True

                    has hbox

                    # Add the screenshot.
                    add FileScreenshot(i)
                    
                    $ file_name = FileSlotName(i, columns * rows)
                    $ file_time = FileTime(i, empty=_("Empty Slot."))
                    $ save_name = FileSaveName(i)

                    text "[file_name]. [file_time!t]\n[save_name!t]"

                    key "save_delete" action FileDelete(i)
                    
                    
screen save:

    # This ensures that any other menu screen is replaced.
    tag menu

    use navigation
    use file_picker

screen load:

    # This ensures that any other menu screen is replaced.
    tag menu

    use navigation
    use file_picker

init -2 python:
    style.file_picker_frame = Style(style.menu_frame)

    style.file_picker_nav_button = Style(style.small_button)
    style.file_picker_nav_button_text = Style(style.small_button_text)

    style.file_picker_button = Style(style.large_button)
    style.file_picker_text = Style(style.large_button_text)

    

##############################################################################
# Preferences
#
# Screen that allows the user to change the preferences.
# http://www.renpy.org/doc/html/screen_special.html#prefereces
    
screen preferences:

    tag menu

    # Include the navigation.
    use navigation

    # Put the navigation columns in a three-wide grid.
    grid 3 1:
        style_group "prefs"
        xfill True

        # The left column.
        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Display")
                textbutton _("Window") action Preference("display", "window")
                textbutton _("Fullscreen") action Preference("display", "fullscreen")

            frame:
                style_group "pref"
                has vbox

                label _("Transitions")
                textbutton _("All") action Preference("transitions", "all")
                textbutton _("None") action Preference("transitions", "none")

            frame:
                style_group "pref"
                has vbox

                label _("Text Speed")
                bar value Preference("text speed")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Joystick...") action Preference("joystick")


        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Skip")
                textbutton _("Seen Messages") action Preference("skip", "seen")
                textbutton _("All Messages") action Preference("skip", "all")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Begin Skipping") action Skip()

            frame:
                style_group "pref"
                has vbox

                label _("After Choices")
                textbutton _("Stop Skipping") action Preference("after choices", "stop")
                textbutton _("Keep Skipping") action Preference("after choices", "skip")

            frame:
                style_group "pref"
                has vbox

                label _("Auto-Forward Time")
                bar value Preference("auto-forward time")

        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Music Volume")
                bar value Preference("music volume")

            frame:
                style_group "pref"
                has vbox

                label _("Sound Volume")
                bar value Preference("sound volume")

                if config.sample_sound:
                    textbutton _("Test"):
                        action Play("sound", config.sample_sound)
                        style "soundtest_button"

            frame:
                style_group "pref"
                has vbox

                label _("Voice Volume")
                bar value Preference("voice volume")

                if config.sample_voice:
                    textbutton "Test":
                        action Play("voice", config.sample_voice)
                        style "soundtest_button"

init -2 python:
    style.pref_frame.xfill = True
    style.pref_frame.xmargin = 5
    style.pref_frame.top_margin = 5

    style.pref_vbox.xfill = True

    style.pref_button.size_group = "pref"
    style.pref_button.xalign = 1.0

    style.pref_slider.xmaximum = 192
    style.pref_slider.xalign = 1.0

    style.soundtest_button.xalign = 1.0


##############################################################################
# Yes/No Prompt
#
# Screen that asks the user a yes or no question.
# http://www.renpy.org/doc/html/screen_special.html#yesno-prompt
    
screen yesno_prompt:

    modal True

    window:
        style "gm_root"

    frame:
        style_group "yesno"

        xfill True
        xmargin .05
        ypos .1
        yanchor 0
        ypadding .05
        
        has vbox:
            xalign .5
            yalign .5
            spacing 30
            
        label _(message):
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100
            
            textbutton _("Yes") action yes_action
            textbutton _("No") action no_action


init -2 python:    
    style.yesno_button.size_group = "yesno"
    style.yesno_label_text.text_align = 0.5


##############################################################################
# Quick Menu
#
# A screen that's included by the default say screen, and adds quick access to
# several useful functions.
screen quick_menu:

    # Add an in-game quick menu.
    hbox:
        style_group "quick"
    
        xalign 1.0
        yalign 1.0

        textbutton _("Q.Save") action QuickSave()
        textbutton _("Q.Load") action QuickLoad()
        textbutton _("Save") action ShowMenu('save')
        textbutton _("Skip") action Skip()
        textbutton _("Auto") action Preference("auto-forward", "toggle")
        textbutton _("Prefs") action ShowMenu('preferences')
        
init -2 python:
    style.quick_button.set_parent('default')
    style.quick_button.background = None
    style.quick_button.xpadding = 5

    style.quick_button_text.set_parent('default')
    style.quick_button_text.size = 12
    style.quick_button_text.idle_color = "#8888"
    style.quick_button_text.hover_color = "#ccc"
    style.quick_button_text.selected_idle_color = "#cc08"
    style.quick_button_text.selected_hover_color = "#cc0"
    style.quick_button_text.insensitive_color = "#4448"
    
    # Set a default value for the auto-forward time, and note that AFM is
    # turned off by default.
    config.default_afm_time = 10
    config.default_afm_enable = False
    
screen button: 
    if variable:    
        vbox xalign 0.1 yalign 0.1:
            textbutton "Show affection points" action ui.callsinnewcontext("aff_screen_label")
            # you can also use an image button:
            #imagebutton:
            #    idle "button_idle.png"
            #    hover "button_hover.png"
            #    action ui.callsinnewcontext("aff_screen_label")
                
screen aff_screen:
    frame:
        has vbox
        text "Bob: [bob_points] points"
        text "Larry: [larry_points] points"
        textbutton "Return" action Return()

label aff_screen_label:
    call screen aff_screen
    return
    
screen hello_world:
     tag example
     zorder 1
     modal False

     text "Hello, World."



    
    
