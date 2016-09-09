import sys
from setuptools import setup

tests_require = ["nose"]
if sys.version_info < (3,0):
    tests_require = ["nose", "mock"]

setup(
    name="pawn",
    version="0.1.0",
    author="iLoveTux",
    author_email="me@ilovetux.com",
    description="One intersect of AWK, Python and Awesomness",
    license="GPLv3",
    keywords="language interpreter",
    url="http://github.com/ilovetux/pawn",
    packages=['pawn'],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pawn=pawn.cli:main",
        ]
    },
    test_suite="nose.collector",
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPLv3",
    ],
)
