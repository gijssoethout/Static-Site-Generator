import os, shutil, pathlib
from block_markdown import markdown_to_html_node

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        filename = filename.replace(".md", ".html")
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            generate_path(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise Exception("No title found!")

def generate_path(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown)

    result = template.replace("{{ Title }}", title).replace("{{ Content }}", html.to_html())

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(result)

        
