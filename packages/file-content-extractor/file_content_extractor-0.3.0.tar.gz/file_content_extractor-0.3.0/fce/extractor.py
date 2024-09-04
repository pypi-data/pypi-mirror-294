import mimetypes
import os
import logging
from datetime import datetime
from pathlib import Path
from anytree import Node, RenderTree
import pathspec

class FileExtractor:
    def __init__(self, target_directory=None, ignore_file="ignore.conf", output_file="output.txt", include_tree=False,
                 use_absolute_paths=False, file_extensions=None, min_size=None, max_size=None, modified_after=None,
                 split_size=None):
        self.current_directory = Path(target_directory) if target_directory else Path.cwd()
        self.ignore_file = Path(ignore_file)
        self.output_file = Path(output_file)
        self.include_tree = include_tree
        self.use_absolute_paths = use_absolute_paths
        self.file_extensions = file_extensions
        self.min_size = min_size
        self.max_size = max_size
        self.modified_after = modified_after
        self.split_size = split_size
        self.ignore_patterns = []
        self.filtered_paths = []
        self.spec = None

        logging.basicConfig(filename='extractor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_ignore_patterns(self):
        if self.ignore_file.exists():
            with self.ignore_file.open('r', encoding='utf-8') as f:
                patterns = [line.strip() for line in f if line.strip() and not line.startswith(('#', ';'))]
                self.spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)
            logging.info(f"Ignore patterns loaded from {self.ignore_file}")
        else:
            logging.warning(f"Ignore file {self.ignore_file} not found. Proceeding without ignoring any files.")

    def filter_paths(self):
        ignore_conf_name = self.ignore_file.name

        for root, dirs, files in os.walk(self.current_directory):
            root_path = Path(root)
            all_files = [root_path / d for d in dirs] + [root_path / f for f in files]

            for path in all_files:
                relative_path = path.relative_to(self.current_directory)

                if relative_path.name == ignore_conf_name:
                    logging.info(f"Ignoring {relative_path} (ignore file)")
                    # print(f"Ignoring {relative_path} (ignore file)")
                    continue

                if self.spec.match_file(str(relative_path)):
                    logging.info(f"Ignoring {relative_path}")
                    # print(f"Ignoring {relative_path}")
                    continue

                if self._file_matches_filters(path):
                    self.filtered_paths.append(path)

    def _file_matches_filters(self, file_path):
        file_size = os.path.getsize(file_path)
        if self.min_size and file_size < self.min_size:
            return False
        if self.max_size and file_size > self.max_size:
            return False
        
        if self.modified_after:
            modified_time = os.path.getmtime(file_path)
            if datetime.fromtimestamp(modified_time) < self.modified_after:
                return False
        
        if self.file_extensions:
            _, ext = os.path.splitext(file_path)
            if ext.lower() not in self.file_extensions:
                return False
        
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and not mime_type.startswith("text"):
            return False

        return True

    def extract_file_content(self):
        with self.output_file.open('w', encoding='utf-8') as out_file:
            if self.include_tree:
                tree_content = self.generate_tree()
                out_file.write("Directory Tree:\n")
                out_file.write(tree_content + "\n\n")

            for path in self.filtered_paths:
                out_file.write(f"File Path: {path}\n")
                out_file.write("Content:\n")
                try:
                    if path.is_file():
                        with path.open('r', encoding='utf-8') as f:
                            content = f.read()
                            out_file.write(content)
                    else:
                        out_file.write("Skipped directory.\n")
                except Exception as e:
                    out_file.write(f"Could not read file due to: {e}\n")
                    logging.error(f"Failed to read file {path}: {e}")
                out_file.write("\n" + "="*80 + "\n\n")

        logging.info(f"Extraction completed. All contents written to {self.output_file}")
        print(f"Extraction completed. All contents written to {self.output_file}")

    def generate_tree(self):
        root_node = Node(str(self.current_directory))
        nodes = {str(self.current_directory): root_node}

        for path in self.filtered_paths:
            parts = path.relative_to(self.current_directory).parts

            for i, part in enumerate(parts):
                current_path = self.current_directory.joinpath(*parts[:i + 1])
                if str(current_path) not in nodes:
                    nodes[str(current_path)] = Node(part, parent=nodes[str(current_path.parent)])

        tree_content = "\n".join([f"{pre}{node.name}" for pre, fill, node in RenderTree(root_node)])
        return tree_content

    def run(self):
        self.load_ignore_patterns()
        self.filter_paths()
        self.extract_file_content()

