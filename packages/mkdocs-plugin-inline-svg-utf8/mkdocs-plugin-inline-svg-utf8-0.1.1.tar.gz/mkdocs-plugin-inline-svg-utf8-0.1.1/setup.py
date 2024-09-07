# setup.py

import os
from setuptools import setup, find_packages

def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='mkdocs-plugin-inline-svg-utf8',
    version='0.1.1',
    description='A MkDocs plugin that inlines SVG images into the output with utf-8 encoding.',
	long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs plugin inline svg utf8',
    url='https://github.dev/Grufbert/mkdocs-plugin-inline-svg-utf8',
    author='Nico Klinger',
	license='MIT',
	python_requires='>=3.5',
    install_requires=[
		'mkdocs'
	],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'inline-svg-utf8 = src:InlineSvgPluginUtf8',
        ]
    }
)
