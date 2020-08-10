import os
import sys
import subprocess

def parse_args(args: list) -> ("relative_path", "gvim_flags", int):
    """ converts args into a more usable format
    :returns: a tuple of the relative path name and the flags for gvim and the number of rotations to encode
    """
    _ = args.pop(0)
    if len(args) < 1:
        raise(Exception("Too few arguments"))
    elif len(args) == 1:
        return args, "", 1
    relative_paths = []
    gvim_flags = ""
    n = int(args.pop(0))
    for arg in args:
        if arg.startswith('-'):
            gvim_flags += arg + " "
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
            "Usage of command:\n" +
            "\tROTNe {n; spaces to rotate} {file(s)} [gvim flags]\n" +
            "\t\tsee vim --help for info on flags\n"
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
