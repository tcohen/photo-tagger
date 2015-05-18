import sys
import os
import os.path
import shutil

def copy_tagged_files(tag, root_dir, tags_dir, target_dir):

    print "Call: copy_tagged_files(" + tag + ", " + root_dir + ", " + tags_dir + ", " + target_dir + ")"

    if not os.path.isdir(root_dir):
        print "Error: root_dir " + root_dir + " not found. Exiting."
        return False
    else:
        print "Ok: copying from root_dir " + root_dir

    if not os.path.isdir(tags_dir):
        print "Error: tags_dir " + tags_dir + " not found. Exiting."
        return False
    else:
        print "Ok: using tags_dir " + tags_dir

    tag_file_name = os.path.join(tags_dir, tag + ".tag")

    if not os.path.isfile(tag_file_name):
        print "Error: tag file " + tag_file_name + " not found. Exiting."
        return False
    else:
        print "Ok: Using tag_file_name " + tag_file_name

    if not os.path.isdir(target_dir):
        print "Error: target_dir " + target_dir + " not found. Exiting."
        return False
    else:
        print "Ok: copying to target_dir " + target_dir

    tag_file = open(tag_file_name, "r")

    for line in tag_file:

        line = line.strip()

        if len(line) == 0 or line[0] == "#":
            continue

        source_filename = os.path.join(root_dir, line)
        if not os.path.isfile(source_filename):
            print "Warning: " + source_filename + " not found. Skipping it."
            continue

        target_filename = os.path.join(target_dir, line)
        full_target_dir = os.path.dirname(target_filename)

        print "  " + source_filename + " => " + target_filename

        if not os.path.exists(full_target_dir):
            os.makedirs(full_target_dir)

        shutil.copy(source_filename, target_filename)

    return True

if __name__ == "__main__":

    if not len(sys.argv) == 5:
        print "Usage: " + sys.argv[0] + " tag root_dir tags_dir target_dir. Exiting."
        exit(1)

    tag = sys.argv[1]
    root_dir = sys.argv[2]
    tags_dir = sys.argv[3]
    target_dir = sys.argv[4]

    result = copy_tagged_files(tag, root_dir, tags_dir, target_dir)
    
    if result:
        print "Done."
    else:
        print "Failed."
