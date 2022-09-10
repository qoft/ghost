import sys
import os

def compile_mac():
    os.system("pyinstaller --onefile --name=Ghost ghost.py")

def compile_other():
    os.system("pyinstaller --onefile --name=Ghost ghost.py")

def main():
    args = sys.argv[1:]

    if len(args) == 0:
        compile_other()

    elif len(args) == 1:
        if args[0].lower() in ["mac", "macos", "darwin", "osx"]:
            compile_mac()
        else:
            compile_other()

if __name__ == "__main__":
    main()