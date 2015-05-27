#!/usr/bin/python

import os
import os.path
import ConfigParser

import sys
import pygame

#defs
screen_size = screen_width, screen_height = 1920,1080
screen_half_width = screen_width / 2
border = 10
black = 0,0,0
white = 255,255,255
font_size = 20

focal_image_size = 600
num_back_images = 6
num_fore_images = 6

def constrain_image_to_square(image, square_dim):

    size = image.get_size()

    n = 0
    new_size = (0,0)
    if size[0] > size[1]:   #width is the greater dimension
        
        # w/h = square_dim/n, n = square_dim * h / w

        n = square_dim * size[1] / size[0]
        new_size = (square_dim, n)

    else:                   #height is the greater dimension

        # w/h = n/square_dim, n = square_dim * w / h
        n = square_dim * size[0] / size[1]
        new_size = (n, square_dim)

    return pygame.transform.scale(image, new_size)

def run():

    config = ConfigParser.ConfigParser()
    config.read("tagger-config.ini")
    general_section = "General"

    tags_dir = config.get(general_section, "TagsDir")
    source_tag = config.get(general_section, "SourceTag")
    print "Ok: using tags_dir " + tags_dir + ", source_tag " + source_tag

    source_tag_filename = os.path.expanduser(os.path.join(tags_dir, source_tag + ".tag"))
    if os.path.isfile(source_tag_filename):
        print "Ok: using source_tag_filename " + source_tag_filename
    else:
        print "Error: source_tag_filename " + source_tag_filename + " not found. Exiting."
        return False

    root_dir = os.path.expanduser(config.get(general_section, "RootDir"))
    if not os.path.isdir(root_dir):
        print "Error: root_dir " + root_dir + " not found. Exiting."
        return False
    else:
        print "Ok: using root_dir " + root_dir

    #pygame
    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    pygame.font.init()
    font_filename = pygame.font.get_default_font()
    font = pygame.font.Font(font_filename, font_size)
    help_text = font.render("J/K Back & Forth, G# Go, 1..0 Tag", True, white, black)

    source_tag_file = open(source_tag_filename, "r")

    line_number = 0
    for line in source_tag_file:

        line_number = line_number + 1

        line = line.strip()

        if len(line) == 0 or line[0] == "#":
            continue

        photo_filename = os.path.join(root_dir, line)
        print "  " + photo_filename

        photo = pygame.image.load(photo_filename)
        photo = constrain_image_to_square(photo, focal_image_size)

        #main loop

        back_images = []
        forth_images = []

        back = forth = False
        mainLoop = True
        while mainLoop:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    mainLoop = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        mainLoop = False
                        break

                    if event.key == pygame.K_k:
                        forth = True
                        break

            if back or forth:
                break

            screen.fill(black)

            #draw images

            focal_image_location = (screen_half_width - focal_image_size * 0.5, screen_size[1] - focal_image_size - border)
            screen.blit(photo, focal_image_location)

            #draw text

            help_text_location = ((screen_size[0] - help_text.get_width() - border),    border * 1 + font_size * 0)
            screen.blit(help_text, help_text_location)

            line_number_text = font.render("Line " + str(line_number) + ": " + line, False, white, black)
            line_number_location = ((screen_size[0] - help_text.get_width() - border),  border * 2 + font_size * 1)
            screen.blit(line_number_text, line_number_location)

            pygame.display.flip()

        if not mainLoop:
            break;

    source_tag_file.close()

    pygame.quit()

    return True

if __name__ == "__main__":

    if not os.path.isfile("tagger-config.ini"):
        print "Error: tagger-config.ini not found. Exiting."
        exit(1)

    if run():
        print "Done."
    else:
        print "Failed."
