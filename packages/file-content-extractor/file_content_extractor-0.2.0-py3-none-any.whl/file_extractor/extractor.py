import os
import sys
import logging
from tqdm import tqdm
from datetime import datetime
import mimetypes

VERSION = "1.0.0"

class FileExtractor:
    def __init__(self, target_directory=None, use_absolute_paths=False, ignore_file=".ignorelist", 
                 output_file="output.txt", file_extensions=None, min_size=None, max_size=None, 
                 modified_after=None, split_size=None):
        self.current_directory = target_directory if target_directory else os.getcwd()
        self.output_file_base = output_file
        self.ignore_file = ignore_file
        self.ignore_list = []
        self.use_absolute_paths = use_absolute_paths
        self.file_extensions = file_extensions
        self.min_size = min_size
        self.max_size = max_size
        self.modified_after = modified_after
        self.split_size = split_size
        self._load_ignore_list()
        logging.basicConfig(filename='extractor.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def _load_ignore_list(self):
        if os.path.exists(self.ignore_file):
            with open(self.ignore_file, 'r', encoding='utf-8') as f:
                self.ignore_list = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            logging.info(f"Ignore list loaded from {self.ignore_file}")
        else:
            logging.warning(f"Ignore file {self.ignore_file} not found. Proceeding without ignoring any files.")

    def _is_ignored(self, path, is_directory=False):
        for ignore in self.ignore_list:
            ignore = ignore.rstrip('/')
            
            if ignore.startswith('*.') and path.endswith(ignore.lstrip('*')):
                return True

            if os.path.basename(path) == ignore:
                return True
            
            if ignore.endswith('/*'):
                ignore_dir = ignore.rstrip('/*')
                if os.path.abspath(path).startswith(os.path.abspath(ignore_dir)):
                    return True

            if ignore.endswith('/*') and is_directory:
                ignore_dir = ignore.rstrip('/*')
                if os.path.abspath(path).startswith(os.path.abspath(ignore_dir)):
                    return True

        return False

    def _is_text_file(self, file_path):
        try:
            with open(file_path, 'tr', encoding='utf-8') as check_file:
                check_file.read()
            return True
        except Exception as e:
            logging.warning(f"Failed to read {file_path}: {e}")
            return False

    def _get_path(self, path):
        if self.use_absolute_paths:
            return os.path.abspath(path)
        else:
            return os.path.relpath(path, self.current_directory)

    def _file_matches_filters(self, file_path):
        # 파일 크기 필터링
        file_size = os.path.getsize(file_path)
        if self.min_size and file_size < self.min_size:
            return False
        if self.max_size and file_size > self.max_size:
            return False
        
        # 파일 수정 시간 필터링
        if self.modified_after:
            modified_time = os.path.getmtime(file_path)
            if datetime.fromtimestamp(modified_time) < self.modified_after:
                return False
        
        # 파일 확장자 필터링
        if self.file_extensions:
            _, ext = os.path.splitext(file_path)
            if ext.lower() not in self.file_extensions:
                return False
        
        # MIME 타입 필터링
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and not mime_type.startswith("text"):
            return False

        return True

    def _should_split(self, current_size, additional_size):
        return self.split_size and (current_size + additional_size > self.split_size)

    def extract(self):
        logging.info(f"Starting extraction in {self.current_directory}. Output will be saved to {self.output_file_base}")
        current_output_file = self.output_file_base
        current_size = 0
        file_count = 1

        with open(current_output_file, 'w', encoding='utf-8') as out_file:
            for root, dirs, files in tqdm(os.walk(self.current_directory), desc="Processing directories"):
                dirs[:] = [d for d in dirs if not self._is_ignored(os.path.join(root, d), is_directory=True)]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    if self._is_ignored(file_path) or not self._file_matches_filters(file_path):
                        logging.info(f"Ignored file {file_path}")
                        continue

                    file_size = os.path.getsize(file_path)

                    if self._should_split(current_size, file_size):
                        out_file.close()
                        file_count += 1
                        current_output_file = f"{os.path.splitext(self.output_file_base)[0]}_{file_count}{os.path.splitext(self.output_file_base)[1]}"
                        out_file = open(current_output_file, 'w', encoding='utf-8')
                        current_size = 0
                        logging.info(f"Splitting output to {current_output_file}")

                    if not self._is_text_file(file_path):
                        out_file.write(f"File Path: {self._get_path(file_path)}\n")
                        out_file.write("Content:\n")
                        out_file.write("Skipped binary or non-text file.\n")
                        out_file.write("\n" + "="*80 + "\n\n")
                        logging.info(f"Skipped binary or non-text file {file_path}")
                    else:
                        out_file.write(f"File Path: {self._get_path(file_path)}\n")
                        out_file.write("Content:\n")
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                out_file.write(content)
                            logging.info(f"Extracted content from {file_path}")
                        except Exception as e:
                            out_file.write(f"Could not read file due to: {e}\n")
                            logging.error(f"Failed to read file {file_path}: {e}")
                        out_file.write("\n" + "="*80 + "\n\n")

                    current_size += file_size

        logging.info(f"Extraction completed. All contents written to {current_output_file}")
        print(f"Extraction completed. All contents written to {current_output_file}")
        print(f"Ignore file used: {self.ignore_file if self.ignore_list else 'None detected'}")

def print_usage():
    print("Usage: file_extractor [-a] [-i <ignorefile>] [-o <outputfile>]")
    print("       [-e <ext1,ext2,...>] [-m <min-size>] [-M <max-size>]")
    print("       [-d <YYYY-MM-DD>] [-s <split-size>] [-p <directory>]")
    print("       [-h] [-v]")
    print("Options:")
    print("  -a, --absolute              Use absolute paths in the output.")
    print("  -i, --ignore=<file>         Specify a custom ignore file (default is .ignorelist).")
    print("  -o, --output=<file>         Specify a custom output file (default is output.txt).")
    print("  -e, --extensions=<ext1,ext2,...> Specify file extensions to include (e.g., .txt,.py).")
    print("  -m, --min-size=<bytes>      Specify minimum file size to include.")
    print("  -M, --max-size=<bytes>      Specify maximum file size to include.")
    print("  -d, --modified-after=<YYYY-MM-DD> Specify a date to include files modified after.")
    print("  -s, --split-size=<bytes>    Split output files into chunks of specified size.")
    print("  -p, --path=<directory>      Specify the directory to start extraction from.")
    print("  -h, --help                  Show this help message and exit.")
    print("  -v, --version               Show version information and exit.")

def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        print_usage()
        sys.exit(0)

    if '-v' in sys.argv or '--version' in sys.argv:
        print(f"FileContentExtractor version {VERSION}")
        sys.exit(0)

    # Ask for user confirmation before proceeding
    proceed = input("Are you sure you want to proceed with the extraction? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Extraction cancelled.")
        sys.exit(0)

    use_absolute = False
    ignore_file = ".ignorelist"
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
        else:
            print(f"Unknown argument: {arg}")
            print_usage()
            sys.exit(1)

    extractor = FileExtractor(
        target_directory=target_directory,
        use_absolute_paths=use_absolute,
        ignore_file=ignore_file,
        output_file=output_file,
        file_extensions=file_extensions,
        min_size=min_size,
        max_size=max_size,
        modified_after=modified_after,
        split_size=split_size
    )
    extractor.extract()

if __name__ == "__main__":
    main()