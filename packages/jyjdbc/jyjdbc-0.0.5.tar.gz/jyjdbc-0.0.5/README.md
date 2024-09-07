JyJDBC Pure Jython JDBC dbapi driver
========================================

--------

Overview
--------

https://pypi.org/project/jyjdbc/ is a pure Python pep-249 http://www.python.org/peps/pep-0249.html driver for JDBC usable under Jython.

Latest version available from https://hg.sr.ht/~clach04/jyjdbc

Original written for the Ingres JDBC driver, works with other drivers too.

Targets Jython 2.7.0, 2.5.3, and 2.5.2 (and also works with Jython 2.2).

CPython (and other Python implementations) can make use of JDBC
via a bridge to Jython. For example; RPyC, Pyro4, SPyRO, execnet, and SPIRO.
Use of a bridge may require additional security attention.

More information https://hg.sr.ht/~clach04/jyjdbc (previously https://bitbucket.org/clach04/jyjdbc/wiki/Home)

--------

Features
--------

-   Pure Python / Jython - no Java experience needed
-   No need for JDK, this driver can be extend with just a JRE
-   Only needs JRE, Jython, and JDBC driver for database
-   Better pep-249 compliance than zxJDBC, with a testsuite to prove it
-   Decimal data type support
-   Returns Java types when a Python type is not an option
-   Python developers can maintain it


Why?
----

I needed support for decimal data types which (in 2010) zxJDBC does not have
(nor do the other Python/JDBC solutions). I needed to create a number of
tests for the decimal type so this was a a major issue, I contributed
Decimal support to the IronPython driver but .NET has a limit of 28 decimal
places. JyJDBC has a simple internal structure, adding support for new
types is trivial.

Right now I recommed using jyjdbc instead of zxJDBC. Current weakness of
jyjdbc compared with zxJDBC is that row returning database procedures are
not yet implemented and a few types (Binary and ROWID) are not implemented
(Java types are returned instead).

A test suite is provided for JyJDBC as well as zxJDBC so the different
features/limitations/problems can be compared. There are tests for
Ingres and SQLite3.


## Installation

Either from PyPi or a checkout.

NOTE pip support is experimental and NOT recommended.

    java -jar jython-standalone-2.7.3.jar -m ensurepip
    # NOTE do not recommmend updating pip, especially under Microsoft Windows due to pip-20.3.4 errors related to missing winreg module
    java -jar jython-standalone-2.7.3.jar -m pip install jyjdbc

Demo
----

The following demos make use of the Ingres DBMS and the Ingres JDBC driver.
Connection is made to a database that always exists using Operating System
authentication (hence no username/password in the connect statement).
SELECT is against a table that always exists in all Ingres databases.


Regular Jython example
~~~~~~~~~~~~~~~~~~~~~~

This demo connects to a local Ingres DBMS as the current user.


    C:\>c:\jython2.5.1\jython.bat
    Jython 2.5.1 (Release_2_5_1:6813, Sep 26 2009, 13:47:54)
    [Java HotSpot(TM) Client VM (Sun Microsystems Inc.)] on java1.6.0_02
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import jyjdbc
    >>> con =jyjdbc.connect('iidbdb')  # II_SYSTEM already set, local connection
    >>> cur = con.cursor()
    >>> cur.execute('select * from iidbconstants')
    >>> print cur.description
    [(u'user_name', c, None, None, 32, 0, 0), (u'dba_name', c, None, None, 32, 0, 0), (u'system_owner', varchar, None, None, 32, 0, 0)]
    >>> print cur.fetchall()
    [(u'ingres                          ', u'$ingres                         ', u'$ingres                         ')]
    >>>

For more examples and using other databases see the project wiki
http://code.google.com/p/jyjdbc/wiki/Examples


CPython access to JDBC
~~~~~~~~~~~~~~~~~~~~~~

This demo uses RPyC version 3.1.0 from http://pypi.python.org/pypi/RPyC/

Jython starts rpyc_classic.py:


    jython rpyc_classic.py


CPython also uses RPyC, using the client:


    C:\>python.exe
    Python 2.4.4 (#71, Oct 18 2006, 08:34:43) [MSC v.1310 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import rpyc
    >>> conn = rpyc.classic.connect("localhost")
    >>> jyjdbc = conn.modules.jyjdbc
    >>> con =jyjdbc.connect('iidbdb')  # II_SYSTEM already set (under RPC), local connection
    >>> cur = con.cursor()
    >>> cur.execute('select * from iidbconstants')
    >>> print cur.description
    [(u'user_name', c, None, None, 32, 0, 0), (u'dba_name', c, None, None, 32, 0, 0), (u'system_owner', varchar, None, None, 32, 0, 0)]
    >>> print cur.fetchall()
    [(u'ingres                          ', u'$ingres                         ', u'$ingres                         ')]



NOTES
-----

-   JDBC Time type does NOT support sub second values.
    This means that when Python datetime.time values are sent the time is
    truncated to the second. Similarly when ANSI time values are returned
    from the database if the JDBC driver returns a JDBC time, sub second
    accuracy is lost to truncation. This is how JDBC works.

-   Currently the driver is not 100% pep-249 compliant, but it is closer
    to 100% than zxJDBC. Patches for improvements are welcome.
    See test suite for details. NOTE the driver is being used everyday in
    the current state.

-   The test suite is incomplete, it could benefit from database procedures
    tests and support for other databses.

-   The driver has been tested with:

    -   Actian Avalanche from http://www.actian.com
    -   Actian Vector from http://www.actian.com
    -   Apache Derby from http://db.apache.org/derby/
        Version 10.8.1.2
    -   Ingres DBMS from http://www.actian.com
    -   H2 from http://www.h2database.com/
        Version 1.4.198 (2019-02-22)
    -   sqlite3
        -   sqlite-jdbc-3.7.2.jar from https://bitbucket.org/xerial/sqlite-jdbc/downloads
            (also see https://github.com/xerial/sqlite-jdbc).

    The driver was originally developed using Ingres.
    Patches for support of other drivers/servers are welcome,
    along with API improvements to improve PEP-249 compliance.

-   Support for Jython 2.2 is present, but due to the use of modules:

    -   Decimal
    -   datetime
    -   logging
    
    The Python 2.4 modules are needed. Python 2.5 support is
    the main focus of this driver but where possible support for older
    releases will be added. See "backports" notes in source. Or use
    a patched Jython 2.2 from https://bitbucket.org/clach04/jython/downloads
    
    I have jyjdbc running on a server with Jython 2.2.1 under JRE 1.5.0.

-   The setup.py script uses either setuptools or distutils. Distutils
    requires either either the standalone Jython jar file or a Standard
    Jython install (installing Core does not install distutils).

-   Building the documentation (via setup.py) requires docutils (and the
    docutils depedencies).

-   Running the test suite requires dbapi20 / dbapi-compliance. There are
    other testsuites and it would be good to have jyjdbc running with those.
    For more information about dbapi20 see:

    -   https://web.archive.org/web/20200608201110/http://stuartbishop.net/Software/DBAPI20TestSuite/
    -   https://launchpad.net/dbapi-compliance

    A known working copy of dbapi-compliance (aka dbapi20) is available
    from https://bitbucket.org/clach04/dbapi-compliance/overview

    It would be useful to add support for some ORMs and make use of the ORM
    test suite, for example SQLAlchemy has comprehensive test suite.

    For any changes, please ensure the test suite runs clean using the H2 test
    suite.
