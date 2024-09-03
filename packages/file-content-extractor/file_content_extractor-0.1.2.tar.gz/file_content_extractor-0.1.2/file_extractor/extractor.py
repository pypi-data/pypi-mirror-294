import os
import sys

class FileExtractor:
    def __init__(self, use_absolute_paths=False):
        self.current_directory = os.getcwd()
        self.output_file = "output.txt"
        self.ignore_file = ".ignorelist"
        self.ignore_list = []
        self.use_absolute_paths = use_absolute_paths
        self._load_ignore_list()

    def _load_ignore_list(self):
        if os.path.exists(self.ignore_file):
            with open(self.ignore_file, 'r', encoding='utf-8') as f:
                self.ignore_list = [line.strip() for line in f if line.strip() and not line.startswith("#")]

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
        except:
            return False

    def _get_path(self, path):
        if self.use_absolute_paths:
            return os.path.abspath(path)
        else:
            return os.path.relpath(path, self.current_directory)

    def extract(self):
        with open(self.output_file, 'w', encoding='utf-8') as out_file:
            for root, dirs, files in os.walk(self.current_directory):
                dirs[:] = [d for d in dirs if not self._is_ignored(os.path.join(root, d), is_directory=True)]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    if self._is_ignored(file_path):
                        continue
                    if not self._is_text_file(file_path):
                        out_file.write(f"File Path: {self._get_path(file_path)}\n")
                        out_file.write("Content:\n")
                        out_file.write("Skipped binary or non-text file.\n")
                        out_file.write("\n" + "="*80 + "\n\n")
                        continue
                    out_file.write(f"File Path: {self._get_path(file_path)}\n")
                    out_file.write("Content:\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            out_file.write(content)
                    except Exception as e:
                        out_file.write(f"Could not read file due to: {e}\n")
                    out_file.write("\n" + "="*80 + "\n\n")

        print(f"All files and their contents have been written to {self.output_file}, excluding those in {self.ignore_file}")

if __name__ == "__main__":
    use_absolute = '--absolute' in sys.argv
    extractor = FileExtractor(use_absolute_paths=use_absolute)
    extractor.extract()
