from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from pyclsload import load_cls, load_dir


def main():
    ap = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    ap.add_argument("-f", "--file", help="target python file path", type=str)
    ap.add_argument("-d", "--directory", help="load all files in directory", type=str)
    ap.add_argument("-c", "--cls", help="class to load", type=str, required=True)
    ap.add_argument("-m", "--method", help="method to call", type=str, required=True)
    ap.add_argument("-ca", "--class-arguments", help="arguments to pass to the class", nargs='+')
    ap.add_argument("-fa", "--function-arguments", help="Arguments to pass to the function", nargs='+')
    a = ap.parse_args()

    if a.file:
        print(f"Loading and initializing class '{a.cls}' from '{a.file}'.")
        cls = load_cls(a.file, a.cls, a.class_arguments)

        print(f"Executing method '{a.method}'.")
        if a.function_arguments:
            cls.call(a.method, a.function_arguments)
        else:
            cls.call(a.method)
    elif a.directory:
        for cls in load_dir(a.directory, {}):
            cls()


if __name__ == '__main__':
    main()
