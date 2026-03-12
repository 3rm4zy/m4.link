import configparser
from jinja2 import Environment, FileSystemLoader
import os

# Read the config
config = configparser.ConfigParser()
config.read('config.ini')

# Read profile
profile = {
    'name': config.get('profile','Name'),
    'picture': config.get('profile','Picture'),
    'description': config.get('profile','Description'),
    'avatar_style': config.get('profile', 'Avatar_Style') if config.has_option('profile', 'Avatar_Style') else 'rounded',
    'favicon': config.get('settings', 'favicon') if config.has_option('settings', 'favicon') else None,
}

# Read settings
settings = {
    'button_style': config.get('settings','button_style'),
    'button_color': config.get('settings','button_color'),
    'background': config.get('settings', 'Background') if config.has_option('settings', 'Background') else None,
}

# Read links
links = []
link_number = 1
while True:
    section_name = f'link {link_number}'
    if config.has_section(section_name):
        link = {
            'title': config.get(section_name,'Title'),
            'url': config.get(section_name, 'URL'),
            'icon': config.get(section_name, 'Icon'),
            'background': config.get(section_name, 'Background') if config.has_option(section_name, 'Background') else None,
            'description': config.get(section_name, 'Description') if config.has_option(section_name, 'Description') else None,
        }
        links.append(link)
        link_number += 1
    else:
        break

# Jinja2
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index.html.j2')

# Generate the HTML
html_output = template.render(
    profile=profile,
    settings=settings,
    links=links,
)

# Write to file
with open('html/index.html', 'w') as f:
    f.write(html_output)

print("Website generated successfully! YAY :3")
print(f"Profile: {profile['name']}")
print(f"Links: {len(links)}")