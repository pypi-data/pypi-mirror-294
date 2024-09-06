from setuptools import setup, find_packages

setup(
    name='textipic',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'textipic = textipic.textipic:textipic',
        ],
    },
    author='Avinion',
    author_email='shizofrin@gmail.com',
    url='https://x.com/Lanaev0li',
    description='A script to generate images from text',
    long_description=open('textipic/README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)
