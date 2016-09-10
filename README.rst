************
Introduction
************

.. image:: https://travis-ci.org/iLoveTux/pawn.svg?branch=master
    :alt: Travis-CI Build Status (for Linux)
    :scale: 100%
    :target: https://travis-ci.org/iLoveTux/pawn

.. image:: https://ci.appveyor.com/api/projects/status/0qltknipom8f2bi3?svg=true
    :alt: AppVeyor Build Status (for windows)
    :scale: 100%
    :target: https://ci.appveyor.com/project/iLoveTux/pawn

.. image:: https://codecov.io/gh/iLoveTux/pawn/branch/master/graph/badge.svg
    :alt: Test Coverage Status
    :scale: 100%
    :target: https://codecov.io/gh/iLoveTux/pawn

.. image:: https://codeclimate.com/github/iLoveTux/pawn/badges/gpa.svg
   :alt: Code Climate
   :scale: 100%
   :target: https://codeclimate.com/github/iLoveTux/pawn

.. image:: https://readthedocs.org/projects/pawn/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: http://pawn.readthedocs.io/en/latest/?badge=latest

-----------------------------
What is it and why do I care?
-----------------------------

Pawn is a language built by mashing Python together with AWK and gluing them together
with a little magic.

Simply put, Pawn is a language designed to scan a text file line-by-line looking
for patterns and when a pattern matches, its associated action is executed. This is
incredibly useful for parsing logs or other semi-structured, plain-text files.

I am a regular user of awk, but there are limitations to it. You are limited to the
awk programming language which is a interpreted language inspired by C. With
Pawn, you have complete access to Python and all the third-party modules
currently installed.

A typical Pawn script will look like this::

    BEGIN{
        import sys
        import requests

        critical_errors = 0
    }
    (?i)critical{
        requests.post("https://my-alerting-server", data=LINE)
        critical_errors += 1
    }
    END{
        print("There were {} critical errors found".format(critical_errors))
    }

This script makes use of the special patterns BEGIN and END. BEGIN is executed once
before processing any lines of the file. END is executed once after all the lines
have been processed.

The pattern in the middle portion "(?i)critical" is a regex using Python's inline-regex
modifiers. This regex matches on any occurance of "critical" regardless of case.

The script essentialy looks for any line containing the word "critical" and when it finds
one, it sends an http post request to an imaginary server (whose purpose is to respond to
any critical events) and increment a counter. At the end of the script, a count of the
lines containing the word "critical" is printed.

To execute this script, you would save it into a file called "critical_response.pawn" and
run::

    `pawn critical_response.pawn file.log`

----------------
Programatic API?
----------------

Pawn includes a programatic API as well for embeding its functionality into
other applications. To use pawn in your application, you might do something
like so::

    from pawn import pawn

    script = """
    BEGIN{
        print("starting")
    }
    \d+{
        print("found a number")
    }
    END{
        print("ending")
    }
    """

    pawn(script=script, files=os.path.listdir("."))

This would run the script against each file in the current directory.

So, now for the magic:

Pawn accepts a script and a list of files. If a single file is passed in and
it is not a list, it will be coerced into one. Once it is verified that we are
working with a list, the list is scanned for strings, if a string is found in
the list, it is assumed to be a filename and it will be opened. Once that is all
done, we loop through the list of files and iterate through the files.

This is where the magic really happens since in Python file-objects are iterators
which allow one to efficiently loop through the lines of a file. If we consider this,
along with the above rules, we can pass any iterable yielding lines for processing.

----------------
How do I get it?
----------------

To get the latest version::

  $ pip install https://github.com/ilovetux/pawn/archive/master.zip

For the nightlies::

  $ pip install https://github.com/ilovetux/pawn/archive/dev.zip

-----------------------
How do I run the tests?
-----------------------

You can clone the repository and use the following command::

  $ make test

or alternately::

  $ python setup.py nosetests


-----------------------------
What is this compatible with?
-----------------------------

Pawn is tested and confirmed to work with

* Python 3.5
* Python 3.4
* Python 3.3
* Python 2.7
* pypy

Pawn should work on all platforms on which Python runs.

-------------------------------
What is on the list to be done?
-------------------------------


Check out our `Issue Tracker <https://github.com/iLoveTux/pawn/issues>`_ for the
items we are currently working on.

---------------
How can I help?
---------------

You can do all the github type things, submit an issue in our `issue tracker <https://github.com/ilovetux/unitils/issues>`_ or fork and submit a `pull request <https://github.com/ilovetux/unitils/pulls>`_. If none of that appeals to you, you can always send me an email personally at me@ilovetux.com
