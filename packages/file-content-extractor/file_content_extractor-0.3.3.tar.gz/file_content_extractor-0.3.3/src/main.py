import sys
from datetime import datetime
from src.extractor import FileExtractor
from src.version import get_version, check_for_updates, upgrade_package


def print_usage():
    print("Usage: fce [-a] [-i <ignorefile>] [-o <outputfile>]")
    print("       [-e <ext1,ext2,...>] [-m <min-size>] [-M <max-size>]")
    print("       [-d <YYYY-MM-DD>] [-s <split-size>] [-p <directory>] [--tree] [--include-ignored]")
    print("       [-h] [-v]")
    print("Options:")
    print("  -a, --absolute              Use absolute paths in the output.")
    print("  -i, --ignore=<file>         Specify a custom ignore file (default is ignore.conf).")
    print("  -o, --output=<file>         Specify a custom output file (default is output.txt).")
    print("  -e, --extensions=<ext1,ext2,...> Specify file extensions to include (e.g., .txt,.py).")
    print("  -m, --min-size=<bytes>      Specify minimum file size to include.")
    print("  -M, --max-size=<bytes>      Specify maximum file size to include.")
    print("  -d, --modified-after=<YYYY-MM-DD> Specify a date to include files modified after.")
    print("  -s, --split-size=<bytes>    Split output files into chunks of specified size.")
    print("  -p, --path=<directory>      Specify the directory to start extraction from.")
    print("  --tree                      Print the directory tree of the current path and add it to the output file.")
    print("  --include-ignored           Include files and directories listed in the ignore.conf when printing the directory tree.")
    print("  -h, --help                  Show this help message and exit.")
    print("  -v, --version               Show version information and exit.")


def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        print_usage()
        sys.exit(0)

    if '-v' in sys.argv or '--version' in sys.argv:
        version = get_version()
        print(f"FileContentExtractor version {version}")
        sys.exit(0)

    # Check for updates
    is_update_available, latest_version = check_for_updates()
    if is_update_available:
        print(f"A new version ({latest_version}) is available.")
        upgrade = input("Would you like to upgrade now? [y]/n: ").strip().lower()
        if upgrade == 'n':
            sys.exit(0)
        upgrade_package()
        sys.exit(0)

    include_tree = '--tree' in sys.argv

    # Ask for user confirmation before proceeding
    proceed = input("Are you sure you want to proceed with the extraction? [y]/n: ").strip().lower()
    if proceed == 'n':
        print("Extraction cancelled.")
        sys.exit(0)

    use_absolute = False
    ignore_file = "ignore.conf"
    output_file = "output.txt"
    file_extensions = None
    min_size = None
    max_size = None
    modified_after = None
    split_size = None
    target_directory = None

    for arg in sys.argv[1:]:
        if arg in ['-a', '--absolute']:
            use_absolute = True
        elif arg.startswith(('-i=', '--ignore=')):
            ignore_file = arg.split('=', 1)[1]
        elif arg.startswith(('-o=', '--output=')):
            output_file = arg.split('=', 1)[1]
        elif arg.startswith(('-e=', '--extensions=')):
            file_extensions = arg.split('=', 1)[1].split(',')
            file_extensions = [ext.strip().lower() for ext in file_extensions]
        elif arg.startswith(('-m=', '--min-size=')):
            min_size = int(arg.split('=', 1)[1])
        elif arg.startswith(('-M=', '--max-size=')):
            max_size = int(arg.split('=', 1)[1])
        elif arg.startswith(('-d=', '--modified-after=')):
            modified_after = datetime.strptime(arg.split('=', 1)[1], '%Y-%m-%d')
        elif arg.startswith(('-s=', '--split-size=')):
            split_size = int(arg.split('=', 1)[1])
        elif arg.startswith(('-p=', '--path=')):
            target_directory = arg.split('=', 1)[1]
        elif arg == '--tree':
            include_tree = True
        else:
            print(f"Unknown argument: {arg}")
            print_usage()
            sys.exit(1)

    extractor = FileExtractor(
        target_directory=target_directory,
        ignore_file=ignore_file,
        output_file=output_file,
        include_tree=include_tree,
        use_absolute_paths=use_absolute,
        file_extensions=file_extensions,
        min_size=min_size,
        max_size=max_size,
        modified_after=modified_after,
        split_size=split_size
    )
    extractor.run()


if __name__ == "__main__":
    main()
