from setuptools import setup, find_packages

setup(
    name = "Athena",
    version = "0.1",
    packages = find_packages(),

    entry_points = {
        'console_scripts' : [
            'athena = athena:main'
            ]
    },

    #author details
    author = "Hourd, Zantier, RaVeY",
    description = "A MUD IRCBot written in Python",
    url="https://github.com/datkinson/athena"
)
