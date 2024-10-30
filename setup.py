from setuptools import setup, find_packages

setup(
    name='png_bank',
    version='0.1',
    description='Password manager that fits into a png',
    license='MIT',
    author='Ryan Stewart',
    author_email='rstewarr04@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pyperclip',
        'Pillow',
        'cryptography',
        'simple-terminal-menu',
    ],
    entry_points={
        'console_scripts': [
            'png_bank=png_bank.cli:run',  # Command to run the main script
        ],
    },
)
