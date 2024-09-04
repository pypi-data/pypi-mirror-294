import logging
from pathlib import Path
import os
import pathspec
from anytree import Node, RenderTree


class FileExtractor:
    def __init__(self, target_directory=None, ignore_file="ignore.conf", output_file="output.txt", include_tree=False):
        self.current_directory = Path(target_directory) if target_directory else Path.cwd()
        self.ignore_file = Path(ignore_file)
        self.output_file = Path(output_file)
        self.include_tree = include_tree
        self.ignore_patterns = []
        self.filtered_paths = []
        self.spec = pathspec.PathSpec.from_lines('gitwildmatch', [])  # 기본적으로 빈 패턴 리스트로 초기화

        logging.basicConfig(filename='extractor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_ignore_patterns(self):
        if self.ignore_file.exists():
            with self.ignore_file.open('r', encoding='utf-8') as f:
                patterns = [line.strip() for line in f if line.strip() and not line.startswith(('#', ';'))]
                if patterns:  # 패턴이 있을 경우에만 spec을 다시 초기화
                    self.spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)
            logging.info(f"Ignore patterns loaded from {self.ignore_file}")
        else:
            logging.warning(f"Ignore file {self.ignore_file} not found. Proceeding without ignoring any files.")

    def filter_paths(self):
        ignore_conf_name = self.ignore_file.name  # ignore.conf 파일 이름

        for root, dirs, files in os.walk(self.current_directory):
            root_path = Path(root)
            all_files = [root_path / d for d in dirs] + [root_path / f for f in files]

            for path in all_files:
                relative_path = path.relative_to(self.current_directory)

                # ignore.conf 파일을 항상 제외
                if relative_path.name == ignore_conf_name:
                    logging.info(f"Ignoring {relative_path} (ignore file)")
                    # print(f"Ignoring {relative_path} (ignore file)")
                    continue

                # pathspec을 사용하여 패턴과 경로 일치 여부 확인
                if self.spec.match_file(str(relative_path)):
                    logging.info(f"Ignoring {relative_path}")
                    # print(f"Ignoring {relative_path}")
                    continue

                self.filtered_paths.append(path)

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
