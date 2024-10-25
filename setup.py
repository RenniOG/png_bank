from setuptools import setup, find_packages

setup(
    name='png_bank',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyperclip',
        'Pillow',
        'cryptography',
    ],
    entry_points={
        'console_scripts': [
            'my_project=my_project.main:run',  # Command to run the main script
        ],
    },
)
