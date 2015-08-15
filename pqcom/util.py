
import sys
import os
import pkg_resources

VERSION = 0.5

script_path = os.path.dirname(sys.argv[0])

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', script_path)
    full_path = os.path.join(base_path, relative_path)
    if os.path.isfile(full_path):
        return full_path
    else:
        return pkg_resources.resource_filename(__name__, relative_path)
