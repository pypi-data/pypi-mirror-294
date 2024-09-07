# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""jyjdbc Pure Jython (Python in the JVM) JDBC dbapi pep-249 driver
Copyright (C) 2011 Ingres Corporation
Copyright (C) 2011 Chris Clark

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License version 2.1 only, as published by the Free Software Foundation.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

import sys
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
    find_packages = None

from distutils.util import get_platform


try:
    from docutils.core import publish_cmdline
except ImportError:
    publish_cmdline = None


readme_filename = 'README.md'  # FIXME this is actually rst
if os.path.exists(readme_filename):
    f = open(readme_filename)
    long_description = f.read()
    f.close()
else:
    long_description = None


if len(sys.argv) <= 1:
    print("""
Suggested setup.py parameters:

    * build
    * install
    * sdist  --formats=zip
    * sdist  # NOTE requires tar/gzip commands


    python -m pip install -e .

PyPi:

    python -m pip install setuptools twine

    python setup.py sdist
    # python setup.py sdist --formats=zip
    python -m twine upload dist/* --verbose

    ./setup.py  sdist ; twine upload dist/* --verbose

""")


# Metadata
project_name = 'jyjdbc'
project_name_lower = project_name.lower()

__version__ = None  # Overwritten by executing _version.py.
exec(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), project_name_lower, '_version.py')).read())  # get __version__

person_name = 'Chris Clark'
person_email = None


"""
    The "sources" section below could be replaced with a static MANIFEST.IN
    file, but at the moment we are leaving all the build logic in one file,
    and the MANIFEST file gets created dynamically, by distutils. 
    The MANIFEST.in is generated semi-dynamically from this script. 
    Note that if one changes the contents of setup.py, the MANIFEST file
    needs to be deleted.
    
    NOTE could use "hg manifest" to generate manifest (sans html file).
"""
if os.path.exists('MANIFEST'):
    os.unlink('MANIFEST')
MANIFEST_in = open('MANIFEST.in', 'w')
#MANIFEST_in.write('include CHANGELOG\n')  # FIXME missing TODO autogenerate from commit log
MANIFEST_in.write('include LICENSE\n')
MANIFEST_in.write('include test_jyjdbcingres_dbapi20.py\n')
MANIFEST_in.write('include test_zxjdbcingres_dbapi20.py\n')
MANIFEST_in.write('include test_jyjdbcsqlite_dbapi20.py\n')
MANIFEST_in.write('include test_zxjdbcsqlite_dbapi20.py\n')
MANIFEST_in.close()

# disable package finding, explictly list package
find_packages = False
if find_packages:
    packages = find_packages()
else:
    packages = [project_name_lower]



"""
TODO

hg ? sdist_hg
"""

setup(
    name=project_name,
    version=__version__,
    url='https://hg.sr.ht/~clach04/jyjdbc',
    author=person_name,
    author_email=person_email,
    maintainer=person_name,
    maintainer_email=person_email,
    packages=packages,
    license='LGPLv2.1',  # NOTE http://guide.python-distribute.org/creation.html and http://docs.python.org/distutils/setupscript.html disagree on what this field is
    description='Pure Jython (Python in the JVM) JDBC dbapi pep-249 driver',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[  # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Environment :: Other Environment',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',

        'Intended Audience :: Developers',

        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows :: Windows NT/2000',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: Implementation :: Jython',
        'Programming Language :: SQL',
        'Topic :: Database',
        ],
    platforms='any',
    # Requirements / dependencies: dbapi20 <http://stuartbishop.net/Software/DBAPI20TestSuite/> (for running test suite) docutils (optional), setuptools (optional)
    zip_safe=True,
)
