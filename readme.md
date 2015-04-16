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

### So whats in those files I just copied over?

The rpy files contain all the python Classes and Functions for players, skills and basically all the hardwork done for creating an RPG.

## Quick Start

Lets create our own RPG adventure and introduce many of the concepts in Raiser RPG System.

Lets open up script.rpy with a text editor. Lets start off with declaring some resources. Remove everything from script.rpy and put the following inside:



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
    $ show_village_map(middle_town, hero)`
```

Lets go through what we have done here. The script starts off with an init block in which we will define all of our 'static' resources like images. Next comes the load_resources label. Here we will put all the meat of our RPG. We define the time, characters and a stage. Lets go through each one:

```
$ main_time = GameTime(hour=9, day=1, month=1, year=2015)
```

Here we define the in-game time. This is when our clock starts when we start the game. We will go into more into this later (GameTime section TODO). Character definitions are same the Ren'py API (http://www.renpy.org/doc/html/quickstart.html#characters). 

```
$ e_weapon_discount = Event(name="Weapon Discount", small_name="WD", frequency=(2, 30)) 
.....

$ ALL_EVENTS += [e_weapon_discount, e_hospital_discount]
$ populate_events()
```

Here we define an 'Event' object, it takes 3 parameters, name, small_name (this will display in the calendar) and frequency. Frequency means the event will occur on every 2nd or 30th of every month, there are more options, see Events section (TODO). We then add our new events into ALL_EVENTS (holds all events) and run populate_events function. This function will populate our calendar with the events we just defined.

```
$ l_hospital = Location(name='Hospital', label='village_hospital', events=[e_hospital_discount])
```

Here we define the hospital location. The Location object (see Location section TODO) is used to define locations that characters can visit whilst in a Village (see Village section TODO). We also bind the hospital event defined earlier to it.

```
 $ middle_town = Village(id=1, name="Middle Town", leader=None, marker_xpos=0.40, marker_ypos=0.25, map="town_map_1", locations=BASE_LOCATIONS, village_tag="middle_town", mission_locations=2, wealth=50)
```

A Village (see Village section TODO) contains locations. All 3 villages defined have the same 3 locations in this case. We also put the villages inside ALL_VILLAGES variable.

We then go on to define shop items (see ShopItem section), shops (see Shop section), player (see Player section), skills (se Skill section) and a stage (see Stage section).



