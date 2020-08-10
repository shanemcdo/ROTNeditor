import os
import sys
import subprocess

def parse_args(args: list) -> ("relative_path", "gvim_flags", int):
    """ converts args into a more usable format
    :returns: a tuple of the relative path name and the flags for gvim and the number of rotations to encode
    """
    _ = args.pop(0)
    relative_paths = []
    gvim_flags = ""
    next_arg_is_n = False
    n = 0
    for arg in args:
        if arg == '--rotn':
            next_arg_is_n = True
        elif arg.startswith('-'):
            gvim_flags += arg + " "
        elif next_arg_is_n:
            n = int(arg)
            next_arg_is_n = False
        else:
            relative_paths.append(arg)
    length = len(relative_paths)
    if length < 1:
        raise(Exception("Too few arguments"))
    return relative_paths, gvim_flags, n

def open_files(relative_paths, gvim_flags, n) -> None:
    for path in relative_paths:
        if n != 0 and os.path.exists(path):
            os.system("ROTN " + str(-n) + " -f " + path + " -o " + path)
    p = subprocess.Popen(("gvim " + ' '.join(relative_paths) + " " + gvim_flags).split())
    p.wait()
    if n != 0:
        for path in relative_paths:
            os.system("ROTN " + str(n) + " -f " + path + " -o " + path)

def print_command_template() -> None:
    print(
            "ROTNe {file(s)} [gvim flags]\n" +
            "\tTo see flags do vim --help"
            )

def main():
    try:
        paths, gvim_flags, n = parse_args(sys.argv)
        open_files(paths, gvim_flags, n)
    except Exception as e:
        print("Error:", e)
        print_command_template()

if __name__ == "__main__":
    main()
