import os
import os.path
import ConfigParser

import sys
import pygame

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
    size = width, height = 800, 600
    speed = [4, 4]
    white = 255, 255, 255
    screen = pygame.display.set_mode(size)

    source_tag_file = open(source_tag_filename, "r")

    for line in source_tag_file:

        line = line.strip()

        if len(line) == 0 or line[0] == "#":
            continue

        photo_filename = os.path.join(root_dir, line)
        print "  " + photo_filename

        ball = pygame.image.load(photo_filename)
        ball = pygame.transform.scale(ball, (100, 100))
        ballrect = ball.get_rect()

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            ballrect = ballrect.move(speed)
            if ballrect.left < 0 or ballrect.right > width:
                speed[0] = -speed[0]
            if ballrect.top < 0 or ballrect.bottom > height:
                speed[1] = -speed[1]

            screen.fill(white)
            screen.blit(ball, ballrect)
            pygame.display.flip()

        break

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
