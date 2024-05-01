WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

#weapons
# weapon_data = {
#     'sword': {'cooldown': 100, 'damage': 15,'graphics':'graphics/weapons/sword/full.png'},
#     'lance': {'cooldown': 400, 'damage': 30,'graphics':'graphics/weapons/lance/full.png'},
#     'axe': {'cooldown': 300, 'damage': 20,'graphics':'graphics/weapons/axe/full.png'},
#     'rapier': {'cooldown': 50, 'damage': 8,'graphics':'graphics/weapons/rapier/full.png'},
#     'sai': {'cooldown': 80, 'damage': 10,'graphics':'graphics/weapons/sai/full.png'}}
#enemy set up
monster_data = {
    'raccoon': {'health': 300, 'exp': 300, 'attack_damage': 40, 'attack_type': 'claw', 'attack_sound':'...', 'speed': 2, 'resistance': 3, 'attack_radius':120, 'notice_radius':400},
    'spirit': {'health': 100, 'exp': 100, 'attack_damage': 8, 'attack_type': 'thunder', 'attack_sound':'...', 'speed': 4, 'resistance': 3, 'attack_radius':60, 'notice_radius':350},
    'bamboo': {'health': 70, 'exp': 70, 'attack_damage': 6, 'attack_type': 'leaf_attack', 'attack_sound':'...',  'speed': 3, 'resistance': 3, 'attack_radius':50, 'notice_radius':300},
    'squid': {'health': 100, 'exp': 100, 'attack_damage': 20, 'attack_type': 'slash', 'attack_sound':'...', 'speed': 3, 'resistance': 3, 'attack_radius':80, 'notice_radius':360},}

npc_data = {
    'dietrich': {'interaction_type': '...', 'interaction_sound':'...', 'speed': 2,'interaction_radius': 5, 'notice_radius': 15},
    'kaya': {'interaction_type': '...', 'ineraction_sound':'...', 'speed': 2,'interaction_radius': 5, 'notice_radius': 15},
    'laura': {'interaction_type': '...', 'ineraction_sound':'...', 'speed': 2,'interaction_radius': 5, 'notice_radius': 15},
    'maya': {'interaction_type': '...', 'ineraction_sound':'...', 'speed': 2,'interaction_radius': 5, 'notice_radius': 15},
    'rin': {'interaction_type': '...', 'ineraction_sound':'...', 'speed': 2,'interaction_radius': 5, 'notice_radius': 15}}