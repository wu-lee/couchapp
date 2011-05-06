# -*- coding: utf-8 -*-
#
# This file is part of couchapp released under the Apache 2 license. 
# See the NOTICE for more information.

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import Extension


from distutils.core import Extension
from distutils.sysconfig import get_python_lib
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.install_data import install_data
from imp import load_source

import os
import sys

if not hasattr(sys, 'version_info') or sys.version_info < (2, 6, 0, 'final'):
    raise SystemExit("Couchapp requires Python 2.6 or later.")


executables = []
setup_requires = []
extra = {}

SELECT_BACKPORT_MACROS = []

if "linux" in sys.platform:
    SELECT_BACKPORT_MACROS.append(("HAVE_EPOLL", 1))
    SELECT_BACKPORT_MACROS.append(("HAVE_SYS_EPOLL_H", 1))
elif "darwin" in sys.platform or "bsd" in sys.platform:
    SELECT_BACKPORT_MACROS.append(("HAVE_KQUEUE", 1))
    SELECT_BACKPORT_MACROS.append(("HAVE_SYS_EVENT_H", 1))
else:
    pass

SELECT_BACKPORT_SOURCES = [
        os.path.join('couchapp','autopush','select_backportmodule.c')]

if len(SELECT_BACKPORT_MACROS) > 0:
    extra['ext_modules'] = [
        Extension("couchapp.autopush.select_backport", 
            sources=SELECT_BACKPORT_SOURCES,
            define_macros = SELECT_BACKPORT_MACROS,
            )]

if "darwin" in sys.platform:
    WATCHDOG_SRC_DIR = os.path.join('couchapp', 'autopush', 'watchdog')


    watchdog_version = load_source('version',
                          os.path.join(WATCHDOG_SRC_DIR, 'version.py'))


    _watchdog_fsevents_sources = [
        os.path.join(WATCHDOG_SRC_DIR, '_watchdog_fsevents.c'),
        os.path.join(WATCHDOG_SRC_DIR, '_watchdog_util.c'),
    ]
    
    extra['ext_modules'].append(
            Extension(name='_watchdog_fsevents',
                sources=_watchdog_fsevents_sources,
                libraries=['m'],
                define_macros=[
                    ('WATCHDOG_VERSION_STRING',
                        '"' + watchdog_version.VERSION_STRING + '"'),
                    ('WATCHDOG_VERSION_MAJOR', watchdog_version.VERSION_MAJOR),
                    ('WATCHDOG_VERSION_MINOR', watchdog_version.VERSION_MINOR),
                    ('WATCHDOG_VERSION_BUILD', watchdog_version.VERSION_BUILD),
                    ],
                extra_link_args=[
                    '-framework', 'CoreFoundation',
                    '-framework', 'CoreServices',
                    ],
                extra_compile_args=[
                    '-std=c99',
                    '-pedantic',
                    '-Wall',
                    '-Wextra',
                    '-fPIC',
                    ]
                ))
            
    
def get_data_files():
    data_files = []
    data_files.append(('couchapp', 
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

MODULES = [
        'couchapp',
        'couchapp.autopush',
        'couchapp.autopush.brownie',
        'couchapp.autopush.brownie.datastructures',
        'couchapp.autopush.pathtools',
        'couchapp.autopush.watchdog',
        'couchapp.autopush.watchdog.observers',
        'couchapp.autopush.watchdog.tricks',
        'couchapp.autopush.watchdog.utils',
        'couchapp.hooks',
        'couchapp.hooks.compress',
        'couchapp.restkit',
        'couchapp.restkit.manager',
        'couchapp.restkit.contrib',
        'couchapp.simplejson',
        'couchapp.vendors',
        'couchapp.vendors.backends',
    ]

CLASSIFIERS = [
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Database',
        'Topic :: Utilities',
    ]

def get_scripts():
    scripts = [os.path.join("resources", "scripts", "couchapp")]
    if os.name == "nt":
        scripts.append(os.path.join("resources", "scripts",
            "couchapp.bat"))
    return scripts

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

class install_package_data(install_data):
    def finalize_options(self):
        self.set_undefined_options('install',
                                   ('install_lib', 'install_dir'))
        install_data.finalize_options(self)


# ssl build

def find_file(filename, std_dirs, paths):
    """Searches for the directory where a given file is located,
    and returns a possibly-empty list of additional directories, or None
    if the file couldn't be found at all.

    'filename' is the name of a file, such as readline.h or libcrypto.a.
    'std_dirs' is the list of standard system directories; if the
        file is found in one of them, no additional directives are needed.
    'paths' is a list of additional locations to check; if the file is
        found in one of them, the resulting list will contain the directory.
    """

    # Check the standard locations
    for dir in std_dirs:
        f = os.path.join(dir, filename)
        print 'looking for', f
        if os.path.exists(f): return []

    # Check the additional directories
    for dir in paths:
        f = os.path.join(dir, filename)
        print 'looking for', f
        if os.path.exists(f):
            return [dir]

    # Not found anywhere
    return None

def find_library_file(compiler, libname, std_dirs, paths):
    result = compiler.find_library_file(std_dirs + paths, libname)
    if result is None:
        return None

    # Check whether the found file is in one of the standard directories
    dirname = os.path.dirname(result)
    for p in std_dirs:
        # Ensure path doesn't end with path separator
        p = p.rstrip(os.sep)
        if p == dirname:
            return [ ]

    # Otherwise, it must have been in one of the additional directories,
    # so we have to figure out which one.
    for p in paths:
        # Ensure path doesn't end with path separator
        p = p.rstrip(os.sep)
        if p == dirname:
            return [p]
    else:
        assert False, "Internal error: Path not found in std_dirs or paths"


cmdclass = {'install_data': install_package_data }


def main():
    couchapp = load_source("couchapp", os.path.join("couchapp",
        "__init__.py"))

    # read long description
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        long_description = f.read()

    PACKAGES = {}
    for name in MODULES:
        PACKAGES[name] = name.replace(".", "/")

    DATA_FILES = [
        ('couchapp', ["LICENSE", "MANIFEST.in", "NOTICE", "README.rst",
                        "THANKS",])
        ]


    options = dict(
            name = 'Couchapp',
            version = couchapp.__version__,
            url = 'http://github.com/couchapp/couchapp/tree/master',
            license =  'Apache License 2',
            author = 'Benoit Chesneau',
            author_email = 'benoitc@e-engura.org',
            description = 'Standalone CouchDB Application Development Made Simple.',
            long_description = long_description,
            keywords = 'couchdb couchapp',
            platforms = ['any'],
            classifiers = CLASSIFIERS,
            packages = PACKAGES.keys(),
            package_dir = PACKAGES,
            data_files = DATA_FILES,
            package_data = get_packages_data(),
            #cmdclass=cmdclass,
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
            )
    )
    options.update(extra)
    setup(**options)

if __name__ == "__main__":
    main()



