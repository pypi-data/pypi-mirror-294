import os

def print_directory_tree(root_path, files_to_include):
    tree_lines = []
    last_depth = 0

    for file_path in files_to_include:
        # Convert to relative path from root_path
        rel_path = os.path.relpath(file_path, root_path)
        parts = rel_path.split(os.sep)
        depth = len(parts) - 1

        if depth > last_depth:
            tree_lines.append(' ' * 4 * last_depth + '|')
        last_depth = depth

        tree_lines.append(' ' * 4 * depth + parts[-1])

    tree_content = "\n".join(tree_lines)
    return tree_content
