from setuptools import setup, find_packages

setup(
    name="hello_from_steffy",
    version="0.1",
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        "console_scripts":[
            "hey = hello_from_steffy:greetings"
        ]
    }
)