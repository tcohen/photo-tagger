import os
import os.path
import ConfigParser

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

    source_tag_file = open(source_tag_filename, "r")

    for line in source_tag_file:

        line = line.strip()

        if len(line) == 0 or line[0] == "#":
            continue

        print "  " + line

    source_tag_file.close()

    return True

if __name__ == "__main__":

    if not os.path.isfile("tagger-config.ini"):
        print "Error: tagger-config.ini not found. Exiting."
        exit(1)

    if run():
        print "Done."
    else:
        print "Failed."
