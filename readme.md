# Raiser RPG Framework for Ren'Py

An RPG framework for Ren'py gaming engine (http://www.renpy.org/). The purpose of this framework is to provide a way of creating visual RPGs with little understanding of programming and spend less time creating your own RPG systems.

## Features
- Includes built in battle system (supports up to 3 v 3 fights)
- Dynamic battle fields for strategic gameplay
- In-depth skills, character development, experience, levelling and fight mechianics
- Character creation / skill assignment screen included 
- Open world design, travel to locations and villages
- Buy weapons and equipment in shops
- In-game time and calendar events included
- Create your own planned events, interactions with NPCs / PCs
- Team and teacher system
- Create political movements and micro management
- Fully customisable, customise everything mentioned above!

## Installation

1. Download Ren'py from here: http://www.renpy.org/latest.html (Ren'py 6.15+)
2. Download zip or clone this repo
3. Create new Ren'py project
4. Copy the contents of /core into the /game folder of your new project

For existing projects:

1. Upgrade renpy to atleast 6.15
2. Copy files in /core into /game folder of existing project (WARNING: This will overwrite screens.rpy)
3. It is possible to customise all of the screens used in the framework.

### So whats in those files I just copied over?

The rpy files contain all the Python classes and functions for players, skills and basically all the hardwork done for creating an RPG.

## Quick Start

Lets create our own RPG adventure and introduce many of the concepts in Raiser RPG System.

Lets open up `script.rpy` with a text editor. Remove everything from script.rpy and put the following inside:


```
### STATIC RESOURCES ###
init:
    ### SPRITES ### 
    image sam_1 = im.Scale("sprites/sam_1.png", 270, 500)
    
### DYNAMIC RESOURCES ###
label load_resources:
    ### TIME ###
    $ main_time = GameTime(hour=9, day=1, month=1, year=2015)
    
    ### EVENTS ###
    $ e_weapon_discount = Event(name="Weapon Discount", small_name="WD", frequency=(2, 30)) 
    $ e_hospital_discount = Event(name="Hospital Discount", small_name="HD", frequency=(6, 20)) 
    
    $ ALL_EVENTS += [e_weapon_discount, e_hospital_discount]
    $ populate_events()
    
    ### LOCATIONS ###
    $ l_hospital = Location(name='Hospital', label='village_hospital', events=[e_hospital_discount])
    $ l_weapon_shop = Location(name='Weapon', label='village_weapon_shop', events=[e_weapon_discount]) # weapon shop
    $ l_level_up = Location(name='Level Up', label='village_levelup')
    $ l_training_ground = Location(name='Training', label='village_training')
    $ l_town_mission = Location(name='Mission', label='village_missions', events=[],)
    $ l_apartment = Location(name='Apartment', label='village_home')
    $ l_travel = Location('Travel', 'village_travel')
    
    $ BASE_LOCATIONS = [l_hospital, l_weapon_shop, l_level_up, l_training_ground, l_town_mission, l_apartment, l_travel]
    
    ### VILLAGES ###
    $ middle_town = Village(id=1, name="Middle Town", leader=None, marker_xpos=0.40, marker_ypos=0.25, map="town_map_1", locations=BASE_LOCATIONS, village_tag="middle_town", mission_locations=2, wealth=50)
    $ east_town = Village(id=2, name="East Town", leader=None, marker_xpos=0.60, marker_ypos=0.25, map="town_map_1", locations=BASE_LOCATIONS, village_tag="east_town", mission_locations=2)    
    $ south_town = Village(id=3, name="South Town", leader=None, marker_xpos=0.45, marker_ypos=0.65, map="town_map_1", locations=BASE_LOCATIONS, village_tag="south_town", mission_locations=2)

	$ ALL_VILLAGES = [middle_town, east_town, south_town]

    ### SHOP ITEMS ###
    $ i_heal_paste = ShopItem("Heal Paste", price=300, health=30)
    $ i_chakra_paste = ShopItem("Chakra Paste", price=300, chakra=30)
    $ w_kunai = Weapon(name='Kunai', price=50, range=3, chakra_cost=10, damage=30)

    ### SHOPS ###
    $ hospital_shop = Shop(name="Hospital", items=[i_heal_paste, i_chakra_paste])
    $ weapon_shop = Shop(name="Weapons", items=[w_kunai])
    
    ### CHARACTERS ###
    $ c_hero = Character('Hero', color="#c8ffc8")
    $ c_sam = Character('Sam', color="#c8ffc8")
    
    ### SKILLS ###
    # melee skills
    $ punching_flurry = Skill(name='Punching Flurry', skill_type='melee', label="punchingflurry", range=2, damage=20)
    $ onetwocombo = Skill(name='One Two Combo', skill_type='melee', label="onetwocombo", range=3, damage=30)
    # special skills
    $ blasting_kick = Skill(name="Blast Kick", skill_type="special", label="blast_kick", range=3, chakra_cost=30, damage=60)
    # ranged skills
    $ distance_hit = Skill(name="Distance Hit", skill_type="ranged", label="distance_hit", range=8, chakra_cost=20, damage=20)
    # defensive skills
    $ damage_reduction = Skill(name='Focus', skill_type='defence', label='damagereduction', range=12, duration=3, chakra_cost=10, unlock_exp=300)
    
    $ SKILL_SET_1 = [punching_flurry, onetwocombo, blasting_kick, distance_hit, damage_reduction]
    
    ### PLAYERS ###
    $ hero = LevelledPlayer(lvl=1, name="Hero", skill_pool=SKILL_SET_1, character=c_hero, hudpic="hero_hud")
    $ sam = LevelledPlayer(lvl=1, name="Sam", skill_pool=SKILL_SET_1, character=c_sam, hudpic="sam_hud")
    
    ### STAGES ###
    $ clearing = Stage('Clearing', 1, 1)
    
    ### MISSIONS ###
    # TBC
    
    return

# The game starts here.
label start:
    
    call load_resources
    
    # Lets unlock some locations
    $ l_hospital.unlocked = True
    $ l_apartment.unlocked = True
    $ l_level_up.unlocked = True
    $ l_training_ground.unlocked = True
    $ l_town_mission.unlocked = True
    
    # set main_player
    $ current_session.main_player = hero
    $ current_session.village = middle_town
    $ show_village_map(middle_town, hero)
```

Save and Run the game!

### What just happened!?

Running the `$ show_village_map(middle_town, hero)` shows the player in middle town. Here you can visit different locations, do missions, train to increase your stats (click Show Stats button to see stats), visit your apartment etc, have a play around. This is showing the `villagemap` screen is fully customisable in `screens.rpy`. Please visit the wiki for documentation, https://github.com/paktek123/raiser_rpg_framework/wiki for more.

## Documentation (in progress)

https://github.com/paktek123/raiser_rpg_framework/wiki

## Usage

Raiser RPG Framework is free to be used for commercial or non-commercial projects as long as credit is given even if you use parts of the code (or at least link to this repo).

## Bugs

Please report bugs by opening a new github issue, will do my best to response.

## Contributing

Contributing is highly encouraged and Raiser comes with its own tests. This is currently in early stages at the moment, there are bound to be bugs and features missing. To contribute follow these steps:
- Fork this repo
- Make your changes
- TDD is highly encouraged, please add any tests for NON-GRAPHICAL CODE ONLY changes. Sorry we can't test screens or user interactions at the moment :(
- Make sure tests pass, you can run them when you start the game, go to 'Run Tests' instead of start game.
- Make pull request
- Pull request will be reviewed and merged
- Your name will added to the contributor list :)
