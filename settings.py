WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

#enemy set up
monster_data = {
    'squid': {'health': 100, 'exp': 100, 'attack_damage': 20, 'attack_type': 'slash', 'attack_sound':'...', 'speed': 3, 'resistance': 3, 'attack_radius':80, 'notice_radius':360},
    'raccoon': {'health': 300, 'exp': 300, 'attack_damage': 40, 'attack_type': 'claw', 'attack_sound':'...', 'speed': 2, 'resistance': 3, 'attack_radius':120, 'notice_radius':400},
    'spirit': {'health': 100, 'exp': 100, 'attack_damage': 8, 'attack_type': 'thunder', 'attack_sound':'...', 'speed': 4, 'resistance': 3, 'attack_radius':60, 'notice_radius':350},
    'bamboo': {'health': 70, 'exp': 70, 'attack_damage': 6, 'attack_type': 'leaf_attack', 'attack_sound':'...',  'speed': 3, 'resistance': 3, 'attack_radius':50, 'notice_radius':300}}