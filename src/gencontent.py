import os, shutil
from pathlib import Path
from block_markdown import markdown_to_html_node

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise Exception("No title found!")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown)

    result = template.replace("{{ Title }}", title).replace("{{ Content }}", html.to_html())
    result = result.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(result)

        
