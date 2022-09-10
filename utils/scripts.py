import os
import codecs

script_list = []

def add_script(filename, globals_, locals_):
    global script_list

    if os.path.exists(filename):
        script_list.append(filename)
        exec(codecs.open(filename, encoding="utf-8").read(), globals_, locals_)

def get_scripts():
    return script_list