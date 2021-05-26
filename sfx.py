from pygame import mixer
mixer.init()

alien_hit = mixer.Sound("sounds/alien_hit.mp3")
fire = mixer.Sound("sounds/fire.mp3")
game_over = mixer.Sound("sounds/game_over.mp3")
level_up = mixer.Sound("sounds/levelup.mp3")
load_up = mixer.Sound("sounds/loadup.mp3")
ship_hit = mixer.Sound("sounds/ship_hit.mp3")

def sound_effect(sound):
    mixer.Sound.play(sound)
