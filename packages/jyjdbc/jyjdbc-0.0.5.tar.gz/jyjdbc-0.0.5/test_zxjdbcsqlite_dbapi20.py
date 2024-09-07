#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Test suite for jyjdbc and SQLite.

Uses/requires old/original http://stuartbishop.net/Software/DBAPI20TestSuite/
(also see https://launchpad.net/dbapi-compliance).

Does not use the newer (http://code.google.com/p/acute-dbapi/)

For use with Jython 2.5.x.

Sample usage:
    c:\jython2.5.2\jython test_zxjdbcsqlite_dbapi20.py
    
    java -Dpython.console=org.python.util.InteractiveConsole -Xmx512m -Xss1152k  -classpath "C:\jython2.5.2\jython.jar;%CLASSPATH%" org.python.util.jython  test_zxjdbcsqlite_dbapi20.py
    java -Dpython.console=org.python.util.InteractiveConsole -Xmx512m -Xss1152k  -classpath "C:\jython2.5.2\jython.jar;%CLASSPATH%" org.python.util.jython  test_zxjdbcsqlite_dbapi20.py test_ZxJdbcSQLite.test_callproc
    
"""

import unittest
import os
import sys

import test_jyjdbcsqlite_dbapi20

from com.ziclix.python.sql import zxJDBC


class test_ZxJdbcSQLite(test_jyjdbcsqlite_dbapi20.test_JyjdbcSQLite):
    driver = zxJDBC
    connect_args = (test_jyjdbcsqlite_dbapi20.DATABASE_NAME, None, None, 'org.sqlite.JDBC')
    connect_kw_args = {}


if __name__ == '__main__':
    test_jyjdbcsqlite_dbapi20.main()
