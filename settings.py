WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player': -26,
    'obejct': -40,
    'grass': -10,
    'invisible': 0,}

#UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'


#weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15,'graphics':'graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30,'graphics':'graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20,'graphics':'graphics/weapons/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage': 8,'graphics':'graphics/weapons/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10,'graphics':'graphics/weapons/sai/full.png'}}

#magic
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'graphics/particles/heal/heal.png'}}

#enemy
monster_data = {
    'raccoon': {'health': 300, 'exp': 300, 'attack_damage': 40, 'attack_type': 'claw', 'attack_sound':'...', 'speed': 2, 'resistance': 3, 'attack_radius':120, 'notice_radius':400},
    'spirit': {'health': 100, 'exp': 100, 'attack_damage': 8, 'attack_type': 'thunder', 'attack_sound':'...', 'speed': 4, 'resistance': 3, 'attack_radius':60, 'notice_radius':350},
    'bamboo': {'health': 70, 'exp': 70, 'attack_damage': 6, 'attack_type': 'leaf_attack', 'attack_sound':'...',  'speed': 3, 'resistance': 3, 'attack_radius':50, 'notice_radius':300},
    'squid': {'health': 100, 'exp': 100, 'attack_damage': 20, 'attack_type': 'slash', 'attack_sound':'...', 'speed': 3, 'resistance': 3, 'attack_radius':80, 'notice_radius':360},}

#npc
npc_data = {
    'dietrich': {'attack_damage': 1, 'attack_type': 'slash', 'speed': 3, 'attack_radius':10, 'notice_radius':50},
    'kaya': {'attack_damage': 1, 'attack_type': 'slash', 'speed': 3, 'attack_radius':10, 'notice_radius':50},
    'laura': {'attack_damage': 1, 'attack_type': 'slash', 'speed': 3, 'attack_radius':10, 'notice_radius':50},
    'maya': {'attack_damage': 1, 'attack_type': 'slash', 'speed': 3, 'attack_radius':10, 'notice_radius':50},
    'rin': {'attack_damage': 1, 'attack_type': 'slash', 'speed': 3, 'attack_radius':10, 'notice_radius':50}}

# npc_data = {
#     'dietrich': {'interaction_type': '...', 'interaction_sound':'...', 'speed': 2,'interaction_radius': 50, 'notice_radius': 150},
#     'kaya': {'interaction_type': '...', 'ineraction_sound':'...', 'speed': 2,'interaction_radius': 50, 'notice_radius': 150},
#     'laura': {'interaction_type': '...', 'ineraction_sound':'...', 'speed': 2,'interaction_radius': 50, 'notice_radius': 150},
#     'maya': {'interaction_type': '...', 'ineraction_sound':'...', 'speed': 20,'interaction_radius': 50, 'notice_radius': 150},
#     'rin': {'interaction_type': '...', 'ineraction_sound':'...', 'speed': 2,'interaction_radius': 50, 'notice_radius': 150}}