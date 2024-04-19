from csv import reader
from os import walk     #allows to walk throught the file sys
import pygame

def import_csv_layout(path):  # sourcery skip: for-append-to-extend
    
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',') #delimiter = what seperates the data
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map

def import_folder(path):  # sourcery skip: use-fstring-for-concatenation
    sufrace_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            sufrace_list.append(image_surface)

    return sufrace_list