import os

def display_tree_structure(dir_path, indent="", is_last=True):
    """Recursively display the tree structure of a given directory."""
    try:
        dir_name = os.path.basename(dir_path) or dir_path
        connector = "└── " if is_last else "├── "
        print(f"{indent}{connector}{dir_name}")
        indent += "    " if is_last else "│   "

        # Get all items in the directory
        items = sorted(os.listdir(dir_path))
        item_count = len(items)

        for index, item in enumerate(items):
            item_path = os.path.join(dir_path, item)
            is_last_item = index == item_count - 1

            if os.path.isdir(item_path):
                # Recursively display directories
                display_tree_structure(item_path, indent, is_last_item)
            else:
                # Display files
                connector = "└── " if is_last_item else "├── "
                print(f"{indent}{connector}{item}")
    except PermissionError:
        print(f"{indent}└── [Permission Denied]")
