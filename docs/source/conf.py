import sys
import os

sys.path.append(os.path.abspath('D:\\Python_projects\\WEB\\web_home_work_14'))
project = 'Contacts REST API'
copyright = '2023, hubsit'
author = 'hubsit'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'nature'
html_static_path = ['_static']
