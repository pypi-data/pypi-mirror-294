from setuptools import setup, find_packages

setup(
    name='TOOLS-IDM',  # Nama package di PyPI
    version='1.0.3',  # Versi package kamu
    packages=find_packages(),  # Secara otomatis menemukan semua packages
    entry_points={
        'console_scripts': [
            'ess=ess.ess:main',  # Nama command-line dan fungsi utama
        ],
    },
    install_requires=[
       'aiohttp'
    ],
    description='HANYA UNTUK BERSENANG SENANG',
    author='robbii13',
    author_email='email@example.com',
    url='https://github.com/username/my_project',  # URL repositori atau website
)
