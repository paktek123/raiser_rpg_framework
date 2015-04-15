##############################################################################
# FUNCTIONAL TESTS
#

# All the test objects can go in the init block because we don't care about saving in the tests

init python:
    
    import copy
    import datetime
    
    ### TEST DATA ###
    test_player_character = Character('Test Player',color="#FFFFFF")
    test_enemy_character = Character('Test Enemy',color="#FFFFFF")
    test_stage = Stage('Test Stage', 10, 10)
    test_heal_paste = ShopItem("Test Heal Paste", 300, 30, health=30)
    test_chakra_paste = ShopItem("Test Chakra Paste", 300, 40, chakra=30)
    test_potion_shop = Shop("Hospital", 'test_1', items=[test_heal_paste, test_chakra_paste])
    test_battle1 = Battle(id="1", good_team=[], bad_team=[], xpos=100, ypos=100, battle_label="b_battle_1")
    test_main_time = GameTime(9, 1, 1, 2015)
    current_session = CurrentSession()
    #e_weapon_discount = Event("Weapon Discount", "WD", frequency=(random.randint(2,30),)) 
    #e_hospital_discount = Event("Hospital Discount", "HD", frequency=(random.randint(2,30),)) 
    
    # Skills
    test_melee_skill = Skill(name='Punching Flurry', skill_type='melee', label="punching_flurry", range=2, damage=20)
    test_special_skill = Skill(name="Blast Kick", skill_type="special", label="blast_kick", range=3, chakra_cost=30, damage=60, unlock_exp=300)
    test_sensei_skill = Skill(name="Rise Punch", skill_type="special", label="rise_punch", range=2, chakra_cost=40, damage=35)
    test_stun_skill = Skill('Substitution', 'ranged', "substitution", 8, 20, 15, 0, stun=True)
    test_damage_reduction = Skill('Focus', 'defence', 'damagereduction', 12, 1, 10, duration=2, unlock_exp=300)
    test_chakra_defence = Skill('Chakra Defence', 'defence', 'chakradefence', 12, 2, 15, duration=3, unlock_exp=500)
    test_reflect = Skill('Reflect', 'defence', 'reflect', 12, 20, 20, duration=2, unlock_exp=1500)
    test_dampen = Skill('Dampen', 'defence', 'dampen', 6, 30, 30, duration=3, unlock_exp=2000)
    test_yata_mirror = Skill('Yata Mirror', 'defence', 'ignore', 12, 50, 50, duration=2, unlock_exp=2500)
    test_knife = Weapon(name='Knife', price=30, range=2, chakra_cost=5, damage=25)
    test_bat = Weapon(name='Bat', price=50, range=3, chakra_cost=10, damage=30)
    
    # AI Skill pool
    TEST_SKILL_SET = [test_melee_skill, test_special_skill, test_stun_skill, 
                      test_damage_reduction, test_chakra_defence, test_reflect, test_dampen, test_yata_mirror]
    
    # Players
    test_player_1 = LevelledPlayer(lvl=8, name="Test Player 1", skill_pool=TEST_SKILL_SET, character=test_player_character, 
                                   hudpic="test_player_hud", tilepic="hero_1_tile_r")
    test_player_2 = LevelledPlayer(lvl=8, name="Test Player", skill_pool=TEST_SKILL_SET, character=test_player_character, 
                                   hudpic="test_player_hud", tilepic="hero_1_tile_r")
    test_player_3 = LevelledPlayer(lvl=8, name="Test Player", skill_pool=TEST_SKILL_SET, character=test_player_character, 
                                   hudpic="test_player_hud", tilepic="hero_1_tile_r")
    test_player_sensei = LevelledPlayer(lvl=8, name="Test Sensei", skill_pool=TEST_SKILL_SET + [test_sensei_skill], character=test_player_character, 
                                   hudpic="test_player_hud", tilepic="hero_1_tile_r")
    test_enemy_1 = LevelledPlayer(lvl=8, name="Test Enemy", skill_pool=TEST_SKILL_SET, character=test_enemy_character, 
                                  hudpic="test_enemy_hud", tilepic="thug_1_tile_l")
    test_enemy_2 = LevelledPlayer(lvl=8, name="Test Enemy", skill_pool=TEST_SKILL_SET, character=test_enemy_character, 
                                  hudpic="test_enemy_hud", tilepic="thug_1_tile_l")
    test_enemy_3 = LevelledPlayer(lvl=8, name="Test Enemy", skill_pool=TEST_SKILL_SET, character=test_enemy_character, 
                                  hudpic="test_enemy_hud", tilepic="thug_1_tile_l")
    
    test_team_first = Team("Test Team", test_player_sensei, [test_player_1, test_player_2, test_player_3])
    test_player_1.sensei = test_player_sensei
    
    # locations
    # Commented out because test_frequency event does not exist
    test_location = None #Location('Test', 'test_label', 'test_background', events=[test_frequency_event])
    
    BASE_LOCATIONS = [test_location]
    
    test_village_1 = Village(1, "Test Village 1", test_player_sensei, marker_xpos=0.40, marker_ypos=0.25, map="test_map", 
                             locations=BASE_LOCATIONS, village_tag="middle_town", mission_locations=2, wealth=50)
    
    test_village_2 = Village(2, "Test Village 2", test_player_sensei, marker_xpos=0.40, marker_ypos=0.25, map="test_map", 
                             locations=BASE_LOCATIONS, village_tag="middle_town", mission_locations=2, wealth=50)
    
    ALL_VILLAGES = [test_village_1, test_village_2]
        
    # Test helpers
    def record_test(description, result, expected_result, accumulated_results):
        test_entry = {description: ( result == expected_result) }
        accumulated_results.append(test_entry)
    
    
label run_tests:
    call battle_tests
    call event_tests
    call gametime_tests
    call helper_tests
    call mission_tests
    call player_part1_tests
    call player_part2_tests
    call player_part3_tests
    call shop_tests
    call skill_tests
    call stage_tile_tests
    #call village_location_tests
    
    hide screen test_results
    show screen test_results("Stage / Tile", stage_tile_tests_results)
    
    $ renpy.pause(360.0)
    
    hide screen test_results
    show screen test_results("Skill", skill_tests_results)
    
    $ renpy.pause(360.0)
    
    hide screen test_results
    show screen test_results("Shop", shop_tests_results)
    
    $ renpy.pause(360.0)
    
    hide screen test_results
    show screen test_results("Player Part 1", player_part1_tests_results)
    
    $ renpy.pause(360.0)
    
    hide screen test_results
    show screen test_results("Player Part 2", player_part2_tests_results)
    
    $ renpy.pause(360.0)
    
    hide screen test_results
    show screen test_results("Player Part 3", player_part3_tests_results)
    
    $ renpy.pause(360.0)
    
    hide screen test_results
    show screen test_results("Mission", mission_tests_results)
    
    $ renpy.pause(360.0)
    
    hide screen test_results
    show screen test_results("Helper", helper_tests_results)
    
    $ renpy.pause(360.0)
    
    hide screen test_results
    show screen test_results("GameTime", gametime_tests_results)
    
    $ renpy.pause(360.0)
    
    hide screen test_results
    show screen test_results("Event", event_tests_results)
    
    $ renpy.pause(360.0)
    
    hide screen test_results
    show screen test_results("Battle", battle_tests_results)
    
    $ renpy.pause(360.0)
    
    
label battle_tests:
    
    # functional testing
    python:
        battle_tests_results = []
        
        test_battle1 = Battle(id="1", good_team=[test_player_2], bad_team=[test_enemy_1, test_enemy_2], xpos=100, ypos=100, battle_label="b_battle_1")
        test_battle2 = Battle(id="2", good_team=[test_player_2], bad_team=[], xpos=300, ypos=100, battle_label="b_battle_2")
        
        test_battle1.add_good_member(test_player_1)
        record_test('Add Good Member', test_battle1.good_team, [test_player_2, test_player_1], battle_tests_results)
        
        test_battle1.add_good_member(test_player_1)
        record_test('Add Duplicate Member', test_battle1.good_team, [test_player_2, test_player_1], battle_tests_results)
        
        test_battle1.remove_good_member(test_player_1)
        record_test('Remove Good Member', test_battle1.good_team, [test_player_2], battle_tests_results)
        
        test_battle1.remove_good_member(test_player_1)
        record_test('Cannot remove non-existant member', test_battle1.good_team, [test_player_2], battle_tests_results)
        
        false_result = test_battle1.finished()
        record_test('Battle Not finished', false_result, False, battle_tests_results)
        
        # set hp to zero for bad team
        # covers tests for battle_finished helper
        zero_hp_enemy_1 = copy.deepcopy(test_enemy_1)
        zero_hp_enemy_1.hp = 0
        zero_hp_enemy_2 = copy.deepcopy(test_enemy_1)
        zero_hp_enemy_2.hp = 0
        test_battle1.bad_team = [zero_hp_enemy_1, zero_hp_enemy_2]
        
        true_result = test_battle1.finished()
        record_test('Battle finished', true_result, True, battle_tests_results)
        
        other_battles = [test_battle1, test_battle2]
        
        test_battle1.cleanup(other_battles)
        record_test('Cleanup duplicate good team members', test_battle2.good_team, [], battle_tests_results)
        
        test_battle1.clean_dead_members()
        record_test('Cleanup dead good members', test_battle1.good_team, [test_player_2], battle_tests_results)
        record_test('Cleanup dead bad members', test_battle1.bad_team, [], battle_tests_results)
        
    return
    
label event_tests:
    
    # functional testing
    python:
        event_tests_results = []
        
        test_ranged_event = Event("Ranged Event", "CE", start=(15, 5), finish=(14, 7), label="ranged_event")
        test_frequency_event = Event("Frequency Event", "JT", frequency=(1, ))
        test_probability_event = Event("Probability Event", "???", chance=0.02, label="probability_event", occurrence=0)
        
        ALL_EVENTS += [test_ranged_event, test_frequency_event, test_probability_event]
        
        # populate events
        populate_events()
        
        test_date_range = test_ranged_event.date_range(test_main_time)
        # should generate 61 days (2 months)
        record_test('Check correct number of date range', len(test_date_range), 61, event_tests_results)
        
        # fast forward to ranged event month and day
        test_main_time.month, test_main_time.day = 6, 15
        result = is_event_active_today(test_ranged_event, test_main_time)
        record_test('Check if ranged event active on date', result, True, event_tests_results)
        
        # fast forward to ranged event month and day
        test_main_time.month, test_main_time.day = 8, 16
        result = is_event_active_today(test_ranged_event, test_main_time)
        record_test('Check if ranged event is inactive out of range', result, False, event_tests_results)
        
        # check freqency event should happen every 1st
        test_main_time.month, test_main_time.day = 8, 1
        result = is_event_active_today(test_frequency_event, test_main_time)
        record_test('Check if frequency event happens every first of month', result, True, event_tests_results)
        
        # check freqency event should happen every 1st
        test_main_time.month, test_main_time.day = 9, 1
        result = is_event_active_today(test_frequency_event, test_main_time)
        record_test('Check if frequency event happens every first of month', result, True, event_tests_results)
        
        # check freqency event should happen every 2nd
        test_main_time.month, test_main_time.day = 8, 2
        result = is_event_active_today(test_frequency_event, test_main_time)
        record_test('Check if frequency event does not happen every second of month', result, False, event_tests_results)
        
        # how do I test probability events?
        
    return
        
label gametime_tests:
    python:
        gametime_tests_results = []
        
        # remember this refers to gametime now REAL time
        test_main_time = GameTime(9, 1, 1, 2015)
        time_now = test_main_time.now()
        result = (test_main_time.hour, test_main_time.day, test_main_time.month, test_main_time.year)
        record_test('Check if hour, day, minute and year work for now', result, (9, 1, 1, 2015), gametime_tests_results)
        
        time_dawn = test_main_time.dawn()
        result = [(test_main_time.minute in range(0, 60)), (test_main_time.hour in range(1,6))]
        record_test('Check if hour and minute for dawn', result, [True, True], gametime_tests_results)
        
        time_morning = test_main_time.morning()
        result = [(test_main_time.minute in range(0, 60)), (test_main_time.hour in range(6,12))]
        record_test('Check if hour and minute for morning', result, [True, True], gametime_tests_results)
        
        time_afternoon = test_main_time.afternoon()
        result = [(test_main_time.minute in range(0, 60)), (test_main_time.hour in range(12,18))]
        record_test('Check if hour and minute for afternoon', result, [True, True], gametime_tests_results)
        
        time_evening = test_main_time.evening()
        result = [(test_main_time.minute in range(0, 60)), (test_main_time.hour in range(18,21))]
        record_test('Check if hour and minute for evening', result, [True, True], gametime_tests_results)
        
        time_night = test_main_time.night()
        result = [(test_main_time.minute in range(0, 60)), (test_main_time.hour in range(21,24))]
        record_test('Check if hour and minute for night', result, [True, True], gametime_tests_results)
        
        test_main_time.next_month()
        record_test('Check if month appends', test_main_time.month, 2, gametime_tests_results)
        
        test_main_time.month = 12
        test_main_time.next_month()
        record_test('Check if month appends and goes to next year', (test_main_time.month, test_main_time.year), (1, 2016), gametime_tests_results)
        
        test_main_time.next_day()
        record_test('Check if day appends', test_main_time.day, 2, gametime_tests_results)
        
        test_main_time.day = 30
        test_main_time.next_day()
        record_test('Check if day appends and goes to next month', (test_main_time.day, test_main_time.month), (1, 2), gametime_tests_results)
        
        test_main_time.hour = 9
        test_main_time.next_hour()
        record_test('Check if hour appends', test_main_time.hour, 10, gametime_tests_results)
        
        test_main_time.hour = 24
        test_main_time.next_hour()
        record_test('Check if hour appends and goes to next day', (test_main_time.hour, test_main_time.day), (1, 2), gametime_tests_results)
        
        test_main_time.minute = 1
        test_main_time.next_minute()
        record_test('Check if minute appends', test_main_time.minute, 2, gametime_tests_results)
        
        test_main_time.minute = 60
        test_main_time.next_minute()
        record_test('Check if minute appends and goes to hour day', (test_main_time.minute, test_main_time.hour), (1, 2), gametime_tests_results)
        
        test_main_time.minute, test_main_time.hour, test_main_time.day, test_main_time.month, test_main_time.year = 1, 9, 1, 1, 2015
        test_main_time.advance_time(minutes=30, hours=5, days=10, months=6)
        result = (test_main_time.minute, test_main_time.hour, test_main_time.day, test_main_time.month, test_main_time.year)
        record_test('Check if advance time works', result, (32, 14, 11, 7, 2015), gametime_tests_results)
        
    return
        
label helper_tests:
    
    # functional testing
    python:
        helper_tests_results = []
        
        # Tag logic tests
        test_player_1.tile, test_player_2.tile, test_player_3.tile = test_stage.tile1, test_stage.tile2, test_stage.tile3
        test_tag_1 = [test_player_1]
        test_tag_2 = [test_player_2, test_player_3]
        
        zero_hp_enemy_1 = copy.deepcopy(test_enemy_1)
        zero_hp_enemy_1.hp = 0
        zero_hp_enemy_2 = copy.deepcopy(test_enemy_1)
        zero_hp_enemy_2.hp = 0
        
        test_zero_tag_1 = [zero_hp_enemy_1]
        test_zero_tag_2 = [zero_hp_enemy_1, zero_hp_enemy_2]
        test_zero_tag_3 = [test_player_1, zero_hp_enemy_1]
        
        result = find_suitable_tag_partner(test_tag_1)
        record_test('Return good partner when 1 tag partner', result, test_player_1, helper_tests_results)
        
        result = find_suitable_tag_partner(test_tag_2)
        record_test('Return good partner when 2 tag partner', result, test_player_2, helper_tests_results)
        
        result = find_suitable_tag_partner(test_zero_tag_1)
        record_test('Return no partner when 1 zero hp tag partner', result, None, helper_tests_results)
        
        result = find_suitable_tag_partner(test_zero_tag_2)
        record_test('Return no partner when 2 tag partner', result, None, helper_tests_results)
        
        result = find_suitable_tag_partner(test_zero_tag_3)
        record_test('Return good partner when 2 tag partner', result, test_player_1, helper_tests_results)
        
        # Enemy move weighting
        test_battle_ai = ['d', 'f', 'a', 'm', 's', 'r']
        
        # AI Skill pool
        TEST_SKILL_SET = [test_melee_skill, test_special_skill, test_stun_skill, 
                          test_damage_reduction, test_chakra_defence, test_reflect, test_dampen, test_yata_mirror]
        
        STUDENT_SKILL_SET = [test_melee_skill]
    
        # Player
        test_player_1 = LevelledPlayer(lvl=8, name="Test Player 1", skill_pool=TEST_SKILL_SET, character=test_player_character, 
                                       hudpic="test_player_hud", tilepic="hero_1_tile_r", battle_ai=test_battle_ai)
        
        test_student_1 = LevelledPlayer(lvl=8, name="Test Player", skill_pool=STUDENT_SKILL_SET, character=test_player_character, 
                                        hudpic="test_player_hud", tilepic="hero_1_tile_r", battle_ai=test_battle_ai)
        
        test_student_2 = LevelledPlayer(lvl=8, name="Test Player", skill_pool=TEST_SKILL_SET, character=test_player_character, 
                                        hudpic="test_player_hud", tilepic="hero_1_tile_r", battle_ai=test_battle_ai)
        
        pattern_skill = enemy_pattern(test_player_1)
        result = (pattern_skill in test_player_1.all_skills)
        record_test('Check if skill is within moveset', result, True, helper_tests_results)
        
        # remove all skill affects
        test_player_1.hp = -10
        test_player_1.chakra = -200
        test_player_2.hp = 3000
        test_player_2.chakra = 3000
        
        test_player_1.damagereduction.apply()
        test_player_1.damagereduction.used = 2
        
        remove_all_skill_affects(test_player_1, test_player_2)
        record_test('Fix hp works as expected for negative values', test_player_1.hp, 0, helper_tests_results)
        record_test('Fix chakra works as expected for negative values', test_player_1.chakra, 0, helper_tests_results)
        record_test('Fix hp works as expected for very high values', test_player_2.hp, test_player_2.maxhp, helper_tests_results)
        record_test('Fix chakra works as expected for very high values', test_player_2.chakra, test_player_2.maxchakra, helper_tests_results)
        record_test('Make sure skill is cleared', test_player_1.damagereduction.active, False, helper_tests_results)
        
        # get tag info
        test_player_1.tile, test_player_2.tile, test_player_3.tile = test_stage.tile1, test_stage.tile2, test_stage.tile3
        test_player_1.main = True
        test_tag = [test_player_2, test_player_3]
        
        data = get_tag_info(test_player_1, [test_player_2, test_player_3])
        result = [(data['main'] == test_player_1), (data['tag'] == [test_player_2, test_player_3])]
        record_test('Make sure main and tag are seperate in tag logic', result, [True, True], helper_tests_results)
        
        # test sensei skill
        student_1_skill = get_sensei_skill(test_player_1, test_student_1)
        student_2_skill = get_sensei_skill(test_player_1, test_student_2)
        result = (student_1_skill.name in [s.name for s in test_player_1.all_skills])
        record_test('Student should get sensei skill', result, True, helper_tests_results)
        record_test('Student should not get sensei skill because nothing to teach', student_2_skill, None, helper_tests_results)
        
        # misc 
        test_team_first = Team("Test Team", test_player_sensei, [test_player_1, test_player_2, test_player_3])
        current_session.team = test_team_first
        result = get_player_by_name('Test Player 1')
        record_test('Return first match in team', result, test_player_1, helper_tests_results)
        
        current_session.battles = [test_battle1, test_battle2]
        result = get_battle_by_id("1")
        label_result = get_battle_from_label("b_battle_2")
        record_test('Return first match in battles by id', result, test_battle1, helper_tests_results)
        record_test('Return first match in battles by label', label_result, test_battle2, helper_tests_results)
        
        ALL_VILLAGES = [test_village_1, test_village_2]
        result = other_villages(test_village_1)
        record_test('Check if other villages are returned', result, [test_village_2], helper_tests_results)
        
    return
    
label mission_tests:
    
    # functional testing
    python:
        mission_tests_results = []
        
        test_label_mission = LabelMission('Test Label Mission', 'mission_test_label', hours=6, rank='C')
        
        old_money, old_exp = test_player_1.ryo, test_player_1.exp
        result = test_label_mission.reward(test_player_1)
        result = [(test_player_1.ryo > old_money), (test_player_1.exp > old_exp)]
        record_test('Check if reward adds to players exp and money', result, [True, True], mission_tests_results)
        
    return
        
label player_part1_tests:
    
    # functional testing
    python:
        player_part1_tests_results = []
        
        # Limbs
        test_limb = test_player_1.left_leg
        
        test_limb.bleed()
        result = [test_limb.bleeding, (test_limb.cripple_count == 1)]
        record_test('Bleed causes bleeding to occur and cripple count to go up', result, [True, True], player_part1_tests_results)
        
        test_limb.stop_bleeding()
        result = test_limb.bleeding
        record_test('Stop bleeding stops bleeding', result, False, player_part1_tests_results)
        
        test_limb.cripple_count = 6
        test_limb.cripple()
        record_test('Limb cripple works', test_limb.crippled, True, player_part1_tests_results)
        
        test_limb.injure()
        result = [test_limb.injury, (test_limb.injury_severity == 1)]
        # injury length won't be checked it is configurable
        record_test('Injury causes injury to occur and injury severity count to go up', result, [True, True], player_part1_tests_results)
        
        test_limb.injury_severity = 6
        test_limb.injure()
        record_test('Make sure severity only goes up to 5', test_limb.injury_severity, 5, player_part1_tests_results)
        
        test_limb.rest(365)
        result = [test_limb.injury_severity, test_limb.injury, test_limb.injury_length, test_limb.days_rested, test_limb.bleeding, test_limb.cripple_count]
        record_test('Make sure rest heals all', result, [0, False, 0, 0, False, 0], player_part1_tests_results)
        
        # Team tests
        test_team_first = Team("Test Team", test_player_sensei, [test_player_1, test_player_2])
        test_team_first.add_member(test_player_3)
        result = (test_player_3 in test_team_first.members)
        record_test('Make members can be added', result, True, player_part1_tests_results)
        
        test_team_first.remove_member(test_player_3)
        result = (test_player_3 in test_team_first.members)
        record_test('Make members can be removed', result, False, player_part1_tests_results)
        
        test_team_first.increase_chemistry(10)
        record_test('Increase team chemistry', test_team_first.chemistry, 10, player_part1_tests_results)
        
        test_team_first.decrease_chemistry(10)
        record_test('Increase team chemistry', test_team_first.chemistry, 0, player_part1_tests_results)
        
        # Player tests
        test_player_1.head.injure()
        test_player_1.left_leg.injure()
        test_player_1.hp = 10
        test_player_1.chakra = 10
        test_player_1.full_heal()
        result = [test_player_1.head.injury, test_player_1.left_leg.injury, test_player_1.hp, test_player_1.chakra]
        record_test('Make sure full heal', result, [False, False, test_player_1.maxhp, test_player_1.maxchakra], player_part1_tests_results)
        
        # check if NPC labels work
        interaction_data = {'frequency': (3, 8)}
        test_player_events = LevelledPlayer(lvl=8, name="Test Player 1", skill_pool=TEST_SKILL_SET, character=test_player_character, 
                                            hudpic="test_player_hud", tilepic="hero_1_tile_r", battle_ai=test_battle_ai,
                                            interaction=interaction_data)
        populate_events()
        # should be active on 3 and 8 of every month
        test_main_time.month, test_main_time.day = 1, 3
        result = is_event_active_today(test_player_events.npc_event, test_main_time)
        record_test('Check if event is active on the third', result, True, player_part1_tests_results)
        test_main_time.day = 8
        result = is_event_active_today(test_player_events.npc_event, test_main_time)
        record_test('Check if event is active on the eight of month', result, True, player_part1_tests_results)
        
    return

label player_part2_tests:
    
    # functional testing
    python:
        player_part2_tests_results = []
        
        test_player_1.hp = 20
        test_player_1.increase_hp(30)
        record_test('Increase hp works', test_player_1.hp, 50, player_part2_tests_results)
        
        test_player_1.hp = 20
        test_player_1.increase_hp(10000)
        record_test('Increase hp limits', test_player_1.hp, test_player_1.maxhp, player_part2_tests_results)
        
        test_player_1.chakra = 20
        test_player_1.increase_chakra(30)
        record_test('Increase chakra works', test_player_1.chakra, 50, player_part2_tests_results)
        
        test_player_1.chakra = 20
        test_player_1.increase_chakra(10000)
        record_test('Increase chakra limits', test_player_1.chakra, test_player_1.maxchakra, player_part2_tests_results)
        
        test_player_1.bond = 20
        test_player_1.increase_bond(30)
        record_test('Increase bond works', test_player_1.bond, 50, player_part2_tests_results)
        
        test_player_1.bond = 20
        test_player_1.increase_bond(10000)
        record_test('Increase bond limits', test_player_1.bond, 100, player_part2_tests_results)
        
        # this should go to level 3 and have exp 50 left over, 6 allocation points
        test_player_1.level, test_player_1.exp = 1, 0
        test_player_1.gain_exp(550)
        result = [test_player_1.level, test_player_1.exp, test_player_1.allocation_points]
        record_test('Check levelling up works', result, [3, 50, 6], player_part2_tests_results)
        
        # change direction
        test_player_1.change_direction('left')
        record_test('Change direction left', test_player_1.tilepic, "hero_1_tile_l", player_part2_tests_results)
        test_player_1.change_direction('right')
        record_test('Change direction right', test_player_1.tilepic, "hero_1_tile_r", player_part2_tests_results)
        
        data = test_player_1.get_skill(test_melee_skill)
        result = (test_melee_skill.name in [s.name for s in test_player_1.all_skills])
        record_test('Skill is returned', result, True, player_part2_tests_results)
        
        test_player_1.remove_skill(test_melee_skill)
        record_test('Remove skill', hasattr(test_player_1, test_melee_skill.label), False, player_part2_tests_results)
        
        test_player_1.assign_skill(test_melee_skill)
        record_test('Assign skill', hasattr(test_player_1, test_melee_skill.label), True, player_part2_tests_results)
        
        test_player_1.apply_skill(test_damage_reduction)
        result = test_player_1.check_active_skill(test_damage_reduction)
        record_test('Defensive skill is applied', result, True, player_part2_tests_results)
        
        result = test_player_1.active_defensive_skill()
        record_test('Defensive skill is already applied', result, True, player_part2_tests_results)
        
        # fix stats tested in helper
        
    return
    
label player_part3_tests:
    
    python:
        player_part3_tests_results = []
        
        test_player_1.head.injure()
        test_player_1.head.injury_severity = 2
        result = test_player_1.get_injury_bill()
        record_test('Check if injury bill works', result, (2000, 7), player_part3_tests_results)
        
        # heal all injuries
        test_player_1.full_heal()
        test_player_1.injure_limb(test_player_1.right_leg)
        record_test('Player injure limb works', test_player_1.right_leg.injury, True, player_part3_tests_results)
        
        result = test_player_1.get_injured_limbs()
        record_test('Get injured limb works', result, [test_player_1.right_leg], player_part3_tests_results)
        
        # Item tests
        test_item = ShopItem("Test Heal Paste", 300, 30, health=30)
        # by default player has 1000 money
        test_player_1.buy_item(test_item)
        result = test_player_1.has_item(test_item)
        record_test('Buying item works', result, True, player_part3_tests_results)
        
        test_player_1.buy_item(test_item)
        result = test_player_1.get_item(test_item)
        record_test('Multiple buy will append item', result.quantity, 2, player_part3_tests_results)
        
        test_player_1.remove_item(test_item)
        result = test_player_1.has_item(test_item)
        record_test('Remove item works', result, False, player_part3_tests_results)
        
        # Weapon tests
        # Set quantity to 0 for test weapon
        test_weapon = Weapon(name='Bat', price=50, range=3, chakra_cost=10, damage=30, quantity=0)
        # by default player has 1000 money
        test_player_1.buy_weapon(test_weapon)
        result = test_player_1.has_weapon(test_weapon)
        record_test('Buying weapon works', result, True, player_part3_tests_results)
        
        test_player_1.buy_weapon(test_weapon)
        result = test_player_1.get_weapon(test_weapon)
        record_test('Multiple buy will append weapon', result.quantity, 2, player_part3_tests_results)
        
        get_test_weapon = test_player_1.get_weapon(test_weapon)
        result = get_test_weapon.has_quantity()
        record_test('Weapon is usable if quantity', result, True, player_part3_tests_results)
        get_test_weapon.quantity = 0
        result = get_test_weapon.has_quantity()
        record_test('Weapon is usable if no quantity', result, False, player_part3_tests_results)
        
        test_player_1.remove_weapon(test_weapon)
        result = test_player_1.has_weapon(test_weapon)
        record_test('Remove weapon works', result, False, player_part3_tests_results)
        
        test_player_1.team = test_team_first
        test_player_1.set_sensei()
        record_test('Setting sensei works', test_player_1.sensei, test_team_first.sensei, player_part3_tests_results)
        
    return
    
label shop_tests:
    
    python:
        shop_tests_results = []
        
        # Item tests
        test_item = ShopItem("Test Heal Paste", price=300, health=30)
        
        test_player_1.buy_item(test_item)
        test_player_1.hp = 30
        test_item = test_player_1.get_item(test_item)
        test_item.consume(test_player_1)
        record_test('Consume item works', [test_player_1.hp, test_item.quantity], [60, 0], shop_tests_results)
        
        test_item.half_price()
        record_test('Half price works', test_item.price, 150, shop_tests_results)
        
        test_item.double_price()
        record_test('Double price works', test_item.price, 300, shop_tests_results)
        
        test_shop = Shop("Hospital", 'test_1', items=[test_item, copy.deepcopy(test_item)])
        
        test_shop.half_prices()
        result = [i.price for i in test_shop.items]
        record_test('Shop half price works', result, [150, 150], shop_tests_results)
        
        test_shop.double_prices()
        result = [i.price for i in test_shop.items]
        record_test('Shop double price works', result, [300, 300], shop_tests_results)
        
        test_weapon = Weapon(name='Knife', price=30, range=2, chakra_cost=5, damage=25)
        
        test_weapon.half_price()
        record_test('Half price weapon works', test_weapon.price, 15, shop_tests_results)
        
        test_weapon.double_price()
        record_test('Double price weapon works', test_weapon.price, 30, shop_tests_results)
        
    return
    
label skill_tests:
    python:
        skill_tests_results = []
        
        # Skills
        test_melee_skill_new = Skill(name='Test New Skill', skill_type='melee', label="new_skill", range=2, damage=20, exp=10)
        test_special_skill = Skill(name="Blast Kick", skill_type="special", label="blast_kick", range=3, chakra_cost=30, damage=60, unlock_exp=300)
        test_stun_skill = Skill('Substitution', 'ranged', "stun_skill", 8, 20, 15, 0, stun=True)
        test_damage_reduction = Skill('Focus', 'defence', 'damagereduction', 12, 1, 10, duration=2, unlock_exp=300)
        test_chakra_defence = Skill('Chakra Defence', 'defence', 'chakradefence', 12, 2, 15, duration=3, unlock_exp=500)
        test_reflect = Skill('Reflect', 'defence', 'reflect', 12, 20, 20, duration=2, unlock_exp=1500)
        test_dampen = Skill('Dampen', 'defence', 'dampen', 6, 30, 30, duration=3, unlock_exp=2000)
        test_yata_mirror = Skill('Yata Mirror', 'defence', 'ignore', 12, 50, 50, duration=2, unlock_exp=2500)
        
        test_melee_skill_new.set_to_default()
        result = [test_melee_skill_new.exp, test_melee_skill_new.tech, test_melee_skill_new.active]
        record_test('Set to default works', result, [0, 0, False], skill_tests_results)
        
        test_melee_skill_new.unlock(test_player_1)
        result = hasattr(test_player_1, test_melee_skill_new.label)
        record_test('Unlock skill works', result, True, skill_tests_results)
        
        test_player_1.chakra = 20
        result = test_player_1.blast_kick.is_chakra_requirement_met(test_player_1)
        record_test('Chakra requirement not met', result, False, skill_tests_results)
        
        test_player_1.chakra = 40
        result = test_player_1.blast_kick.is_chakra_requirement_met(test_player_1)
        record_test('Chakra requirement met', result, True, skill_tests_results)
        
        test_player_1.tile = test_stage.tile1
        test_player_2.tile = test_stage.tile12
        result = test_player_1.blast_kick.is_within_range(test_player_1, test_player_2)
        record_test('Range requirement met', result, False, skill_tests_results)
        
        test_player_2.tile = test_stage.tile3
        result = test_player_1.blast_kick.is_within_range(test_player_1, test_player_2)
        record_test('Range requirement not met', result, True, skill_tests_results)
        
        result = test_player_1.blast_kick.is_unlocked()
        record_test('Unlock requirement not met', result, False, skill_tests_results)
        
        current_session.main_player = test_player_1
        test_player_1.blast_kick.gain_exp(1000)
        result = test_player_1.blast_kick.is_unlocked()
        record_test('Unlock requirement is met', result, True, skill_tests_results)
        
        test_player_1.blast_kick.activate()
        record_test('Skill activation works', test_player_1.blast_kick.active, True, skill_tests_results)
        
        test_player_1.blast_kick.deactivate()
        record_test('Skill deactivation works', test_player_1.blast_kick.active, False, skill_tests_results)
        
        test_player_1.blast_kick.append_to_skill()
        record_test('Append to skill works', test_player_1.blast_kick.used, 1, skill_tests_results)
        
        result = test_player_1.blast_kick.deal_damage(test_player_1, test_player_2)
        record_test('Special attacks direct damage, no affects', result, (test_player_1.blast_kick.damage - test_player_2.defence), skill_tests_results)
        
        # this covers range attacks too (same logic)
        result = test_player_1.new_skill.deal_damage(test_player_1, test_player_2)
        record_test('Melee attacks direct damage, no affects', result, (test_player_1.new_skill.damage - test_player_2.defence), skill_tests_results)
        
        test_player_2.damagereduction.activate()
        # tests check_active_skill too
        result = ( test_player_1.new_skill.deal_damage(test_player_1, test_player_2) < (test_player_1.new_skill.damage - test_player_2.defence) )
        record_test('Damage reduction works', result, True, skill_tests_results)
        
        test_player_2.damagereduction.deactivate()
        test_player_2.chakradefence.activate()
        result = ( test_player_1.new_skill.deal_damage(test_player_1, test_player_2) < (test_player_1.new_skill.damage - test_player_2.defence) )
        record_test('Chakra reduction works', result, True, skill_tests_results)
        
        test_player_2.chakradefence.deactivate()
        test_player_1.dampen.activate()
        result = ( test_player_1.new_skill.deal_damage(test_player_1, test_player_2) == (test_player_1.new_skill.damage - test_player_2.defence) / 2 )
        record_test('Dampen works', result, True, skill_tests_results)
        
        test_player_1.dampen.deactivate()
        test_player_2.reflect.activate()
        result = test_player_1.new_skill.deal_damage(test_player_1, test_player_2, dialogue=False)
        record_test('Reflect works', result, test_player_2.damage_dealt, skill_tests_results)
        
        test_player_2.reflect.deactivate()
        test_player_2.ignore.activate()
        result = ( test_player_1.new_skill.deal_damage(test_player_1, test_player_2, dialogue=False) == 0 )
        record_test('Ignore works', result, True, skill_tests_results)
        
        test_player_1.assign_skill(test_stun_skill)
        test_player_1.stun_skill.stun_enemy(test_player_2)
        record_test('Stunning works', test_player_2.stunned, True, skill_tests_results)
        
    return
        
label stage_tile_tests:
    python:
        stage_tile_tests_results = []
        
        test_player_1.hp = 50
        test_player_1.hp -= test_stage.remove_chakra()
        result = ( test_player_1.hp < 50)
        record_test('Stage pull works', result, True, stage_tile_tests_results)
        
        test_tile = test_stage.tile1
        test_tile.project()
        result = [test_tile.idle, test_tile.potential]
        record_test('Tile projection works', result, [test_stage.project_texture, True], stage_tile_tests_results)
        
        test_tile.deproject()
        result = [test_tile.hover, test_tile.potential]
        record_test('Tile deprojection works', result, [test_stage.base_texture, False], stage_tile_tests_results)
        
        test_tile.activate()
        result = [test_tile.idle, test_tile.active]
        record_test('Tile activation works', result, [test_stage.active_texture, True], stage_tile_tests_results)
        
        test_tile.deactivate()
        result = [test_tile.idle, test_tile.active]
        record_test('Tile deactivation works', result, [test_stage.base_texture, False], stage_tile_tests_results)
        
        test_tile.activate_trap()
        result = [test_tile.idle, test_tile.trap]
        record_test('Trap activation works', result, [test_stage.trap_texture, True], stage_tile_tests_results)
        
        remove_trap(test_tile, test_stage)
        result = [test_tile.idle, test_tile.trap]
        record_test('Trap deactivation works', result, [test_stage.base_texture, False], stage_tile_tests_results)
        
        result = get_tile_from_position(2, test_stage)
        record_test('Get tile from position works', result.position, 2, stage_tile_tests_results)
        
    return
        
label village_location_tests:
    python:
        village_location_tests_results = []
        
        # No real logical tests here because they need dialogue to be effectively tested
        # Hopefully in the future there are more stuff to enter
        
        pass
        
    return