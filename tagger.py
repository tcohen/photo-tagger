#!/usr/bin/python

import os
import os.path
import ConfigParser

import sys
import pygame

#defs

screen_size = screen_width, screen_height = 1920,1080
focal_image_size = 900
back_fore_image_size = 200

#screen_size = screen_width, screen_height = 800,600
#focal_image_size = 400
#back_fore_image_size = 50

screen_x_spots = [screen_width * 0.15, screen_width * 0.5, screen_width * 0.85]
border = 10
black = 0,0,0
white = 255,255,255
font_size = 20

focal_image_half_size = focal_image_size / 2
num_back_images = 4
num_fore_images = 4
back_fore_half_image_size = back_fore_image_size / 2

config = ConfigParser.ConfigParser()
config_general_section = "General"

tags_dir = None
tag_names = []
tags = [[],[],[],[],[],[],[],[],[],[]]

current_entry = None

def populate_tags():

    global config
    global config_general_section

    global tags
    global tags_dir

    for digit in range(10):

        tag_name = "Tag" + str(digit)

        try:
            tag_names.append(config.get(config_general_section, tag_name))

        except ConfigParser.NoOptionError:
            tag_names.append(None)

        tag_filename = os.path.expanduser(os.path.join(tags_dir, tag_name + ".tag"))
        if os.path.isfile(tag_filename):
            tag_file = open(tag_filename)
            for line in tag_file:
                line = line.strip()
                if len(line) == 0 or line[0] == "#":
                    continue

                tags[digit].append(line)

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

def tag_current(tag_index):

    global tags
    global tags_dir

    current_image_name = current_entry[1]
    if current_image_name in tags[tag_index]:
        return #already tagged

    tag_filename = os.path.expanduser(os.path.join(tags_dir, tag_names[tag_index] + ".tag"))
    tag_file = open(tag_filename, "a")
    tag_file.write(current_image_name + "\n")
    tag_file.close()

    tags[tag_index].append(current_image_name)

def run():

    global config
    global config_general_section

    global tags_dir
    global current_entry

    #configure

    config.read("tagger-config.ini")

    tags_dir = config.get(config_general_section, "TagsDir")
    source_tag = config.get(config_general_section, "SourceTag")
    print "Ok: using tags_dir " + tags_dir + ", source_tag " + source_tag

    source_tag_filename = os.path.expanduser(os.path.join(tags_dir, source_tag + ".tag"))
    if os.path.isfile(source_tag_filename):
        print "Ok: using source_tag_filename " + source_tag_filename
    else:
        print "Error: source_tag_filename " + source_tag_filename + " not found. Exiting."
        return False

    root_dir = os.path.expanduser(config.get(config_general_section, "RootDir"))
    if not os.path.isdir(root_dir):
        print "Error: root_dir " + root_dir + " not found. Exiting."
        return False
    else:
        print "Ok: using root_dir " + root_dir

    populate_tags()

    #pygame
    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    pygame.font.init()
    font_filename = pygame.font.get_default_font()
    font = pygame.font.Font(font_filename, font_size)
    help_text = font.render("<-/->, G# Go, 1..0 Tag", True, white, black)

    source_tag_file = open(source_tag_filename, "r")

    back_images = []
    fore_images = []

    file_line_number = 0

    while True:

        line = None

        #main loop

        mainLoop = True
        while mainLoop:

            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                mainLoop = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    mainLoop = False
                    break

                if event.key == pygame.K_RIGHT:

                    if len(fore_images) == 0 and current_entry == None:
                        break;  #no fore from end

                    if len(back_images) == num_back_images:
                        back_images.pop(num_back_images-1)
                    back_images.insert(0, current_entry)
                    current_entry = fore_images.pop(0)

                    break

                if event.key == pygame.K_LEFT:

                    if len(back_images) == 0 and current_entry == None:
                        break;  #no back from start

                    if len(fore_images) == num_fore_images:
                        fore_images.pop(num_fore_images-1)
                    fore_images.insert(0, current_entry)
                    current_entry = back_images.pop(0)

                    break;

                if event.key == pygame.K_0:
                    tag_current(0)
                    break
                if event.key == pygame.K_1:
                    tag_current(1)
                    break
                if event.key == pygame.K_2:
                    tag_current(2)
                    break
                if event.key == pygame.K_3:
                    tag_current(3)
                    break
                if event.key == pygame.K_4:
                    tag_current(4)
                    break
                if event.key == pygame.K_5:
                    tag_current(5)
                    break
                if event.key == pygame.K_6:
                    tag_current(6)
                    break
                if event.key == pygame.K_7:
                    tag_current(7)
                    break
                if event.key == pygame.K_8:
                    tag_current(8)
                    break
                if event.key == pygame.K_9:
                    tag_current(9)
                    break

            #fill-up fore images
            while len(fore_images) < num_fore_images:

                line = source_tag_file.readline()
                file_line_number += 1

                if line == None:
                    break

                line = line.strip()

                if len(line) == 0 or line[0] == "#":
                    continue

                image_filename = os.path.join(root_dir, line)
                print "  " + image_filename

                try:
                    image = pygame.image.load(image_filename)

                    entry = (file_line_number, line, image)
                    fore_images.append(entry)

                except:
                    continue

            if current_entry == None:
                current_entry = fore_images.pop(0)

            #draw images

            screen.fill(black)

            #   back images

            back_center_x_left = screen_x_spots[0] - back_fore_half_image_size
            back_current_y_bottom = screen_height - border

            for entry in back_images:
                
                back_image = entry[2]
                back_image = constrain_image_to_square(back_image, back_fore_image_size)
                back_image_location = (back_center_x_left, back_current_y_bottom - back_fore_image_size)
                back_current_y_bottom -= back_fore_image_size + border
                screen.blit(back_image, back_image_location)

            #   fore images

            fore_center_x_left = screen_x_spots[2] - back_fore_half_image_size
            fore_current_y_bottom = screen_height - border

            for entry in fore_images:
                
                fore_image = entry[2]
                fore_image = constrain_image_to_square(fore_image, back_fore_image_size)
                fore_image_location = (fore_center_x_left, fore_current_y_bottom - back_fore_image_size)
                fore_current_y_bottom -= back_fore_image_size + border
                screen.blit(fore_image, fore_image_location)

            #   focal image

            focal_image = current_entry[2]
            focal_image = constrain_image_to_square(focal_image, focal_image_size)
            focal_image_location = (screen_x_spots[1] - focal_image_size * 0.5, screen_size[1] - focal_image_size - border)
            screen.blit(focal_image, focal_image_location)

            #draw text

            help_text_location = ((screen_size[0] - help_text.get_width() - border),    border * 1 + font_size * 0)
            screen.blit(help_text, help_text_location)

            line_number_text = font.render("Line " + str(current_entry[0]) + ": " + current_entry[1], False, white, black)
            line_number_location = ((screen_size[0] - help_text.get_width() - border),  border * 2 + font_size * 1)
            screen.blit(line_number_text, line_number_location)

            help_tag_list_y = border
            for tag_list_index in range(10):
                tag_list = tags[tag_list_index]
                if current_entry[1] in tag_list:
                    help_tag_text = font.render(tag_names[tag_list_index], False, white, black)
                    help_tag_location = (border, help_tag_list_y)
                    screen.blit(help_tag_text, help_tag_location)
                    help_tag_list_y += font_size + border


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
