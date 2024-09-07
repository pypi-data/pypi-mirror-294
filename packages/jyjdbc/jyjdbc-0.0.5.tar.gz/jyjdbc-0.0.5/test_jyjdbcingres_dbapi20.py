#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Test suite for jyjdbc and Ingres.

Uses/requires old/original http://stuartbishop.net/Software/DBAPI20TestSuite/
(also see https://launchpad.net/dbapi-compliance).

Does not use the newer (http://code.google.com/p/acute-dbapi/)

For use with Jython 2.5.x.

Sample usage:
    c:\jython2.5.2\jython test_jyjdbcingres_dbapi20.py
    c:\jython2.5.2\jython test_jyjdbcingres_dbapi20.py -v
    c:\jython2.5.2\jython test_jyjdbcingres_dbapi20.py > ingresres.txt 2>&1
    c:\jython2.5.2\jython test_jyjdbcingres_dbapi20.py test_JyjdbcIngres.test_interval_type_day_to_second

"""

import unittest
import os
import sys

try:
    from decimal import Decimal
except ImportError:
    """This is probably Jython 2.2 or earlier.
    NOTE decimal module from Python 2.4 will not work
    with Jython 2.1 without extra work
    
    Backports is not included but can be easily created:
    
        backports/__init__.py           empty file
        backports/decimal.py            from python 2.4
    """
    from jyjdbc.backports.decimal import Decimal

import datetime


import mydbapi

JYTHON_RUNTIME_DETECTED = 'java' in sys.platform.lower() or hasattr(sys, 'JYTHON_JAR') or str(copyright).find('Jython') > 0
if JYTHON_RUNTIME_DETECTED:
    import jyjdbc
else:
    jyjdbc = None


# global database name
DATABASE_NAME = 'jyjdbc_test'
## FIXME add check and createdb
print('Ensure database exists and supports Unicode, for example:')
print('    createdb -i %s' % DATABASE_NAME)

globalsetUpOnceFlag = False


class test_JyjdbcIngres(mydbapi.MyDatabaseAPITest):
    driver = jyjdbc
    connect_args = ()
    connect_kw_args = {
                        'dsn': DATABASE_NAME,
                        #'dsn': 'jdbc:ingres://localhost:II7/jyjdbc_test;select_loop=on',  # explict jdbc connection string
                        #'debug': True,
                        'callproc_force_input_only': True,
                        }
    sql_types = {
                'BLOB': 'LONG BYTE',
                'CLOB': 'LONG NVARCHAR',
                }
    
    def setUp(self):
        # NOTE using Python unittest, setUp() is called before EACH and every
        # test. There is no single setup routine hook (other than hacking init,
        # module main, etc.). Setup is done here in case an external test
        # suite runner is used (e.g. nose, py.test, etc.).
        
        # Call superclass setUp In case this does something in the
        # future
        mydbapi.MyDatabaseAPITest.setUp(self)
        
        # ensure intial setup complete
        self.setUpOnce()
        
        # end of setUp() there is no per test setup required.

    def setUpOnce(self):
        """Custom, one shot custom setup issued only once for
        the entire batch of tests.
        NOTE actually runs for every test if it fails......
        """
        global globalsetUpOnceFlag
        if globalsetUpOnceFlag:
            return
        
        con = self._connect()  # FIX could add createdb information here
        # Do we have a procedure called lower?
        cur = con.cursor()
        # Dumb SQL generation in case bind parameters not implemented/working
        # (useful when first creating driver)
        cur.execute("""select procedure_name
                        from iiprocedures
                        where procedure_name = '%s'
                        and procedure_owner = USER""" % self.lower_func)
        if len(cur.fetchall()) == 0:
            cur.execute("""create procedure %s( a varchar(20) not null)
                            result row (varchar(20))
                            as
                                declare x=varchar(20) not null;
                            begin
                                select lower(a) into x;
                                return row(x);
                            end""" % self.lower_func)
            con.commit()

        # check we have the expected type of Unicode support.
        sql_query = "select DBMSINFO('UNICODE_NORMALIZATION') from iidbconstants"
        cur.execute(sql_query)
        rs = cur.fetchone()
        self.assertEqual(rs[0], 'NFC', 'Test database needs to use NFC UNICODE_NORMALIZATION (i.e. "createdb -i ...")')  # this probably should be made more obvious in the error output!
        con.close()
        # set complete flag AFTER everything has been done successfully
        globalsetUpOnceFlag = True

    def select_and_check(self, cursor, sql_text, expected_results, bind_params=None, expected_description=None):
        """Simple SELECT and check results.
        
        @param cursor - pep-249 cursor to execute/test
        @param sql_text - SQL query text to run
        @param expected_results - list of result rows
        @param bind_params - optional bind parameters
        @param expected_description - used to compare with cursor.description
            If expected_description is specified this is compared with cursor.description.
            If expected_description is ommitted cursor.description is ignored.
        """
        if bind_params:
            cursor.execute(sql_text, bind_params)
        else:
            cursor.execute(sql_text)
        rs = cursor.fetchall()
        self.assertEqual(len(rs), len(expected_results), 'Incorrect number of rows (%d instead of %d)' % (len(rs), len(expected_results)))
        self.assertEqual(rs, expected_results)
        if expected_description:
            self.assertEqual(cursor.description, expected_description)

    def test_select_decimal_literal_0_01(self):
        con = self._connect()
        try:
            cur = con.cursor()
            sql_text = "select decimal('0.01', 3, 2) as decimal_result from iidbconstants"
            expected_results = [(Decimal('0.01'),), ]
            bind_params = None
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_decimal_literal_0_00000000001(self):
        con = self._connect()
        try:
            cur = con.cursor()
            sql_text = "select decimal('0.00000000001', 15, 11) as decimal_result from iidbconstants"
            expected_results = [(Decimal('0.00000000001'),), ]
            bind_params = None
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_decimal_literal_0_1111111111111111111111111111(self):
        con = self._connect()
        try:
            cur = con.cursor()
            """Test "large" decimal values - these values are not that large
            but they are larger than vaguely similar types.
            Microsoft .NET framework/CLR has a precision limit of
            28 for Decimal numbers.
            float4/float8 types tend to have problems with more than
            15 repeating digits
            """
            sql_text = "select decimal('0.1111111111111111111111111111', 28, 28) as decimal_result from iidbconstants"
            expected_results = [(Decimal('0.1111111111111111111111111111'),), ]
            bind_params = None
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_decimal_literal_0_11111111111111111111111111111(self):
        con = self._connect()
        try:
            cur = con.cursor()
            """Test "large" decimal values - these values are not that large
            but they are larger than vaguely similar types.
            Microsoft .NET framework/CLR has a precision limit of
            28 for Decimal numbers.
            float4/float8 types tend to have problems with more than
            15 repeating digits
            """
            sql_text = "select decimal('0.1111111111111111111111111111', 29, 29) as decimal_result from iidbconstants"
            expected_results = [(Decimal('0.1111111111111111111111111111'),), ]
            bind_params = None
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_decimal_bind_0_01(self):
        con = self._connect()
        try:
            cur = con.cursor()
            tmp_decimal = Decimal('0.01')
            sql_text = "select ? as decimal_result from iidbconstants"
            expected_results = [(tmp_decimal,), ]
            bind_params = (tmp_decimal,)
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_decimal_bind_0_00000000001(self):
        con = self._connect()
        try:
            cur = con.cursor()
            tmp_decimal = Decimal('0.00000000001')
            sql_text = "select ? as decimal_result from iidbconstants"
            expected_results = [(tmp_decimal,), ]
            bind_params = (tmp_decimal,)
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_decimal_bind_0_1111111111111111111111111111(self):
        con = self._connect()
        try:
            cur = con.cursor()
            tmp_decimal = Decimal('0.1111111111111111111111111111')
            sql_text = "select ? as decimal_result from iidbconstants"
            expected_results = [(tmp_decimal,), ]
            bind_params = (tmp_decimal,)
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_decimal_bind_0_11111111111111111111111111111(self):
        con = self._connect()
        try:
            cur = con.cursor()
            tmp_decimal = Decimal('0.11111111111111111111111111111')
            sql_text = "select ? as decimal_result from iidbconstants"
            expected_results = [(tmp_decimal,), ]
            bind_params = (tmp_decimal,)
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_ingresdate_literal_2008_07_15(self):
        con = self._connect()
        try:
            cur = con.cursor()
            sql_text = "select ingresdate('2008_07_15') as result from iidbconstants"
            expected_results = [(datetime.datetime(2008, 7, 15),), ]  # Ingres dates (containing only date) are returned as datetime with midnight time
            bind_params = None
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_ansidate_literal_2008_07_15(self):
        con = self._connect()
        try:
            cur = con.cursor()
            sql_text = "select ansidate('2008_07_15') as result from iidbconstants"
            expected_results = [(datetime.date(2008, 7, 15),), ]
            bind_params = None
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_date_bind_2008_07_15(self):
        con = self._connect()
        try:
            cur = con.cursor()
            tmp_var = datetime.date(2008, 7, 15)
            sql_text = "select ? as bind_result from iidbconstants"
            expected_results = [(tmp_var,), ]
            bind_params = (tmp_var,)
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_timestamp_literal_2008_07_15_132342(self):
        con = self._connect()
        try:
            cur = con.cursor()
            sql_text = "select timestamp('2008-07-15 13:23:42') as result from iidbconstants"
            expected_results = [(datetime.datetime(2008, 7, 15, 13, 23, 42),), ]
            bind_params = None
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_timestamp_literal_2008_07_15_132342_99(self):
        con = self._connect()
        try:
            cur = con.cursor()
            sql_text = "select timestamp('2008-07-15 13:23:42.99') as result from iidbconstants"
            expected_results = [(datetime.datetime(2008, 7, 15, 13, 23, 42, 99),), ]
            bind_params = None
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_timestamp_literal_2008_07_15_132342_5(self):
        con = self._connect()
        try:
            cur = con.cursor()
            sql_text = "select timestamp('2008-07-15 13:23:42.5') as result from iidbconstants"  # 1/2 a second == 500000 microseconds
            expected_results = [(datetime.datetime(2008, 7, 15, 13, 23, 42, 500000),), ]
            bind_params = None
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_datetime_bind_2008_07_15_132342(self):
        con = self._connect()
        try:
            cur = con.cursor()
            tmp_var = datetime.datetime(2008, 7, 15, 13, 23, 42)
            sql_text = "select ? as bind_result from iidbconstants"
            expected_results = [(tmp_var,), ]
            bind_params = (tmp_var,)
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_datetime_subsec_bind_2008_07_15_132342_99(self):
        con = self._connect()
        try:
            cur = con.cursor()
            tmp_var = datetime.datetime(2008, 7, 15, 13, 23, 42, 99)
            sql_text = "select ? as bind_result from iidbconstants"
            expected_results = [(tmp_var,), ]
            bind_params = (tmp_var,)
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_time_literal_132342(self):
        con = self._connect()
        try:
            cur = con.cursor()
            sql_text = "select time('13:23:42') as result from iidbconstants"
            expected_results = [(datetime.time(13, 23, 42),), ]
            bind_params = None
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()
    
    def test_select_time_literal_132342_99(self):
        con = self._connect()
        # problem here is that JDBC time type does NOT support sub-second component
        try:
            cur = con.cursor()
            sql_text = "select time('13:23:42.99') as result from iidbconstants"
            expected_results = [(datetime.time(13, 23, 42),), ]  # NOTE no sub second component!
            bind_params = None
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()
    
    def test_select_time_bind_132342(self):
        con = self._connect()
        try:
            cur = con.cursor()
            tmp_var = datetime.time(13, 23, 42)
            sql_text = "select ? as bind_result from iidbconstants"
            expected_results = [(tmp_var,), ]
            bind_params = (tmp_var,)
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_select_time_bind_132342_99(self):
        con = self._connect()
        # problem here is that JDBC time type does NOT support sub-second components
        try:
            cur = con.cursor()
            tmp_var = datetime.time(13, 23, 42, 99)
            sql_text = "select ? as bind_result from iidbconstants"
            expected_results = [(datetime.time(13, 23, 42),), ]  # NOTE no sub second component!
            bind_params = (tmp_var,)
            expected_description = None
            self.select_and_check(cur, sql_text=sql_text, expected_results=expected_results, bind_params=bind_params, expected_description=expected_description)
        finally:
            con.close()

    def test_paramstyle_is_qmark(self):
        self.assertEqual(self.driver.paramstyle, 'qmark')  # bind param tests uses qmark

def main(test_class=None):
    if test_class:
        test_class.driver.connect(*test_class.connect_args,**test_class.connect_kw_args)  # simple connect, fail sooner rather than running each test and failing with the same error
    mydbapi.main()

if __name__ == '__main__':
    mydbapi.main()
