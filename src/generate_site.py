from parse_markdown import markdown_to_html_node, extract_title
import os
from fileio import *

def copy_static_to_public():
    cur_path = get_root_path()
    try:
        copy_to_dir(f"{cur_path}/static/",f"{cur_path}/public/")
    except Exception as e:
        print(e)

def generate_content(basepath):
    content_dir = "./content"
    template_path = "./template.html"
    dest_dir = "./docs"
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith('.md'):
                mod_path = file_path.replace(content_dir, dest_dir)
                mod_path = mod_path.replace('.md', '.html')
                generate_page(basepath, file_path, template_path, mod_path)




def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r', encoding='utf-8') as from_file:
        markdown = from_file.read()

    # Load the template.html from the template_path
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    try:
        title = extract_title(markdown)
    except Exception as e:
        print(f"Error extracting title: {e}")
        title = "Untitled"
    # Replace the placeholder in the template with the generated HTML
    template_content = template_content.replace("{{ Content }}", html)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    # Create the directory structure if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as dest_file:
        dest_file.write(template_content)
    print(f"Page generated at {dest_path}")
    # For now, just return the template content (you can process it later)
    return template_content
    