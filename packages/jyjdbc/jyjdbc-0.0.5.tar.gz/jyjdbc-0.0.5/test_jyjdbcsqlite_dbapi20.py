#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Test suite for jyjdbc and SQLite.

Uses/requires old/original http://stuartbishop.net/Software/DBAPI20TestSuite/
(also see https://launchpad.net/dbapi-compliance).

Does not use the newer (http://code.google.com/p/acute-dbapi/)

For use with Jython 2.5.x. Although also works with patched Jython 2.2 from
https://bitbucket.org/clach04/jython/downloads

Suggest running test with Xerial SQLiteJDBC, e.g. sqlite-jdbc-3.7.2.jar
There are other implementations of SQLite for the JVM:

  * original Zentus pure Java sqlitejdbc-v056.jar jyjdbc was originally
    tested with this driver but Xerial is now used as test_simple_blob()
    fails with original Zentus v056. Zentus sqlitejdbc may not be available
    anymore from http://www.zentus.com/sqlitejdbc/
  * http://www.xerial.org/trac/Xerial/wiki/SQLiteJDBC - which is based
    on Zentus pure Java version but also has JNI (C) sqlite implementations
    for some platforms, always falls back to pure Java version if there is
    no native shared library option.
  * http://www.ch-werner.de/javasqlite/ - JNI only (and only supplies source
    code or Win32 binaries). Untested with jyjdbc

Sample usage:

    # Get jar file from https://bitbucket.org/xerial/sqlite-jdbc/downloads

    wget https://bitbucket.org/xerial/sqlite-jdbc/downloads/sqlite-jdbc-3.7.2.jar
    
    set CLASSPATH=sqlite-jdbc-3.7.2.jar
    set JYTHONPATH=%CLASSPATH%
    c:\jython2.5.2\jython test_jyjdbcsqlite_dbapi20.py
    
    export CLASSPATH=sqlite-jdbc-3.7.2.jar
    export JYTHONPATH=$CLASSPATH
    jython test_jyjdbcsqlite_dbapi20.py
    
    jython test_jyjdbcsqlite_dbapi20.py -v test_JyjdbcSQLite.test_simple_blob
    java -jar jython.jar test_jyjdbcsqlite_dbapi20.py -v test_JyjdbcSQLite.test_simple_blob
    /usr/lib/jvm/java-6-sun-1.6.0.26/bin/java -jar jython.jar test_jyjdbcsqlite_dbapi20.py -v test_JyjdbcSQLite.test_simple_blob


    java -Dpython.console=org.python.util.InteractiveConsole -Xmx512m -Xss1152k  -classpath "C:\jython2.5.2\jython.jar;%CLASSPATH%" org.python.util.jython  test_jyjdbcsqlite_dbapi20.py
    
    etc.

"""

import os
import sys

import mydbapi

JYTHON_RUNTIME_DETECTED = 'java' in sys.platform.lower() or hasattr(sys, 'JYTHON_JAR') or str(copyright).find('Jython') > 0
if JYTHON_RUNTIME_DETECTED:
    import jyjdbc
else:
    jyjdbc = None


if jyjdbc:
    # assume/hope jdbc driver is in the current directory
    tmp_jdbc_jar_path = os.path.join('sqlite-jdbc-3.7.2.jar')

    # try and add JDBC jar file to CLASSPATH automatically
    jarLoad = jyjdbc.classPathHacker()
    a = jarLoad.addFile(tmp_jdbc_jar_path)

    # Import will fail if classpath is not set correctly (i.e. this is a diagnostic)
    from org.sqlite import JDBC


# global database name
DATABASE_NAME = 'jdbc:sqlite::memory:'  # at least one test (test_close_rollback) needs a persistent backend
DATABASE_NAME = 'jdbc:sqlite:unittest.sqlite3'  # persistent database needed for test_close_rollback


class test_JyjdbcSQLite(mydbapi.MyDatabaseAPITest):
    """Expected failures, due to the way sqlite3 behaves:
    
    TODO implement "pass" tests for below?
      * test_description - typeless so no string type specified
        from JDBC (and jyjdbc deliberately does NOT default to string)
      * test_ROWID - typeless so no ROWID type 
      * test_Binary - typeless so no ROWID type
    """
    driver = jyjdbc
    connect_args = ()
    connect_kw_args = {
                        'dsn': DATABASE_NAME,
                        'driver_name': None,  # Name is optional
                        #'driver_name': 'org.sqlite.JDBC',
                        #'debug': True,
                        }
    sql_types = {
                'BLOB': 'BLOB',
                'CLOB': 'CLOB',
                }

    ddl1 = 'create table %sbooze (name TEXT)' % mydbapi.MyDatabaseAPITest.table_prefix
    ddl2 = 'create table %sbarflys (name TEXT)' % mydbapi.MyDatabaseAPITest.table_prefix

    def test_callproc(self):
        self.skip('SQLite does not support Stored Procedures')
    
    def test_interval_type_day_to_second(self):
        self.skip('SQLite does not support INTERVAL types')

    # override test_description()
    # test is fine but due to sqlite3 not returning a type for empty selects one assert fails, this is a sqlite3 behavior
    def test_description(self):
        if jyjdbc is None:
            mydbapi.MyDatabaseAPITest.test_description(self)
        else:
            con = self._connect()
            try:
                cur = con.cursor()
                self.executeDDL1(cur)
                self.assertEqual(cur.description,None,
                    'cursor.description should be none after executing a '
                    'statement that can return no rows (such as DDL)'
                    )
                cur.execute('select name from %sbooze' % self.table_prefix)
                self.assertEqual(len(cur.description),1,
                    'cursor.description describes too many columns'
                    )
                self.assertEqual(len(cur.description[0]),7,
                    'cursor.description[x] tuples must have 7 elements'
                    )
                self.assertEqual(cur.description[0][0].lower(),'name',
                    'cursor.description[x][0] must return column name'
                    )
                # start of custom code
                # sqlite3 behavior - empty select does not know the type, needs data in row
                self.assertEqual(cur.description[0][1], jyjdbc.DBAPITypeObject(jyjdbc.java.sql.Types.NULL, name='null'),
                    'cursor.description[x][1] must return column type. Got %r'
                        % cur.description[0][1]
                    )
                # end of custom code

                # Make sure self.description gets reset
                self.executeDDL2(cur)
                self.assertEqual(cur.description,None,
                    'cursor.description not being set to None when executing '
                    'no-result statements (eg. DDL)'
                    )
            finally:
                con.close()


def main():
    mydbapi.main()

if __name__ == '__main__':
    main()
