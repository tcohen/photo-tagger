import sys
import os
import os.path

def make_tag_from_dir(tag, root_dir, tags_dir):

    print "Call: make_tag_from_dir(" + tag + ", " + root_dir + ", " + tags_dir + ")"

    if not os.path.isdir(root_dir):
        print "Error: root_dir " + root_dir + " not found. Exiting."
        return False
    else:
        print "Ok: populating from root_dir " + root_dir

    if not os.path.isdir(tags_dir):
        print "Error: tags_dir " + tags_dir + " not found. Exiting."
        return False
    else:
        print "Ok: using tags_dir " + tags_dir

    tag_file_name = os.path.join(tags_dir, tag + ".tag")

    if os.path.isfile(tag_file_name):
        print "Error: tag file " + tag_file_name + " alreay exists. Exiting."
        return False
    else:
        print "Ok: Using tag_file_name " + tag_file_name

    tag_file = open(tag_file_name, "w")
    tag_file.write("# tag file for use with photo-tagger, https://github.com/tcohen/photo-tagger\n\n")

    root_dir_len = len(root_dir)

    abs_root_path = os.path.abspath(root_dir)
    abs_root_path_len = len(abs_root_path)

    for root, dirs, files in os.walk(abs_root_path):
        for filename in files:
            full_filename = os.path.join(root, filename)
            line = full_filename[abs_root_path_len+1:] + "\n"
            tag_file.write(line)
            print "  " + full_filename + " => " + line[:-1]

    tag_file.close()

    return True

if __name__ == "__main__":

    if not len(sys.argv) == 4:
        print "Usage: " + sys.argv[0] + " tag root_dir tags_dir. Exiting."
        exit(1)

    tag = sys.argv[1]
    root_dir = sys.argv[2]
    tags_dir = sys.argv[3]

    result = make_tag_from_dir(tag, root_dir, tags_dir)
    
    if result:
        print "Done."
    else:
        print "Failed."
