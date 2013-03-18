from setuptools import setup, find_packages

setup(
    name = "avalize",
    version = "0.1",
    packages = find_packages(),
    scripts = ['talk.py', 'listen.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['python-easygui'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    entry_points = {
        'console_scripts': [
            'avalize = avalize.talk.py',
        ]
    },

    # metadata for upload to PyPI
    author = "Dylan Taylor",
    author_email = "dylanjt3@gmail.com",
    description = "share files over a network.",
    license = "PSF",
    keywords = "file share network hosts transfer",
    url = "http://github.com/wasdylan/avalize/",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
