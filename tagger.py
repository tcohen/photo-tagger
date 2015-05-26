#!/usr/bin/python

import os
import os.path
import ConfigParser

import sys
import pygame

#defs
screen_size = screen_width, screen_height = 1600,900
screen_half_width = screen_width / 2
border = 10
black = 0,0,0
white = 255,255,255
font_size = 20

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
        photo = pygame.transform.scale(photo, (200, 200))

        back = forth = False
        mainLoop = True
        while mainLoop:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    mainLoop = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        forth = True
                        break

            if back or forth:
                break

            screen.fill(black)

            #draw images

            temp_image_location = (screen_half_width - 100, screen_size[1] - 200 - border)
            screen.blit(photo, temp_image_location)

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
    sdl2.ext.quit()

    return True

if __name__ == "__main__":

    if not os.path.isfile("tagger-config.ini"):
        print "Error: tagger-config.ini not found. Exiting."
        exit(1)

    if run():
        print "Done."
    else:
        print "Failed."
