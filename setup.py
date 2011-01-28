# -*- coding: utf-8 -*-
#
# This file is part of couchapp released under the Apache 2 license. 
# See the NOTICE for more information.

from distutils.core import setup

import os
import sys

from couchapp import __version__

if not hasattr(sys, 'version_info') or sys.version_info < (2, 5, 0, 'final'):
    raise SystemExit("Couchapp requires Python 2.5 or later.")

executables = []
setup_requires = []
extra = {}

def get_data_files():
    data_files = []
    data_files.append((os.curdir, 
                       ["LICENSE", "MANIFEST.in", "NOTICE", "README.md", 
                        "THANKS.txt",]))
    return data_files

def ordinarypath(p):
    return p and p[0] != '.' and p[-1] != '~'

def get_packages_data():
    packagedata = {'couchapp': []}

    for root in ('templates',):
        for curdir, dirs, files in os.walk(os.path.join("couchapp", root)):
            print curdir
            curdir = curdir.split(os.sep, 1)[1]
            dirs[:] = filter(ordinarypath, dirs)
            for f in filter(ordinarypath, files):
                f = os.path.join(curdir, f)
                packagedata['couchapp'].append(f)
    return packagedata 

def all_packages():
    return [
        'couchapp',
        'couchapp.ext',
        'couchapp.hooks',
        'couchapp.hooks.compress',
        'couchapp.restkit',
        'couchapp.restkit.client',
        'couchapp.restkit.conn',
        'couchapp.restkit.filters',
        'couchapp.restkit.http',
        'couchapp.restkit.util',
        'couchapp.vendors',
        'couchapp.vendors.backends',
    ]

def get_scripts():
    if os.name == "posix":
        return [os.path.join("resources", "scripts", "couchapp")]
    return [os.path.join("resources", "scripts", "couchapp.bat")]

Executable = None
if os.name == "nt" or sys.platform == "win32":
    # py2exe needs to be installed to work
    try:
        import py2exe

        # Help py2exe to find win32com.shell
        try:
            import modulefinder
            import win32com
            for p in win32com.__path__[1:]: # Take the path to win32comext
                modulefinder.AddPackagePath("win32com", p)
            pn = "win32com.shell"
            __import__(pn)
            m = sys.modules[pn]
            for p in m.__path__[1:]:
                modulefinder.AddPackagePath(pn, p)
        except ImportError:
            raise SystemExit('You need pywin32 installed ' +
                    'http://sourceforge.net/projects/pywin32')

        # If run without args, build executables, in quiet mode.
        if len(sys.argv) == 1:
            sys.argv.append("py2exe")
            sys.argv.append("-q")

        extra['console'] = [{
             'script': os.path.join("resources", "scripts", "couchapp"),
             'copyright':'Copyright (C) 2008-2011 Benoît Chesneau and others',
             'product_version': __version__ 
        }]


    except ImportError:
        raise SystemExit('You need py2exe installed to run Couchapp.')



 
setup(
    name = 'Couchapp',
    version = __version__,
    url = 'http://github.com/couchapp/couchapp/tree/master',
    license =  'Apache License 2',
    author = 'Benoit Chesneau',
    author_email = 'benoitc@e-engura.org',
    description = 'Standalone CouchDB Application Development Made Simple.',
    long_description = """CouchApp is a set of helpers and a jQuery plugin
    that conspire to get you up and running on CouchDB quickly and
    correctly. It brings clarity and order to the freedom of CouchDB's
    document-based approach.""",
    keywords = 'couchdb couchapp',
    platforms = ['any'],
    classifiers = [
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Database',
        'Topic :: Utilities',
    ],

    packages = all_packages(),
    package_data = get_packages_data(),
    data_files=get_data_files(),

    scripts=get_scripts(),

    options = dict(py2exe={
                        'dll_excludes': [
                            "kernelbase.dll",
                            "powrprof.dll" 
                        ]
                   },

                   bdist_mpkg=dict(zipdist=True,
                                   license='LICENSE',
                                   readme='resources/macosx/Readme.html',
                                   welcome='resources/macosx/Welcome.html')
    ),
 
    **extra
)
