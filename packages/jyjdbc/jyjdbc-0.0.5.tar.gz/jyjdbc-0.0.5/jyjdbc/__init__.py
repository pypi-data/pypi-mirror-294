#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
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

Tested with Jython:
    2.5.1
    2.5.2

Run demo (Ingres):
    c:\jython2.5.2\jython -m jyjdbc

Use this over zxJDBC if:

  * support for types like Decimal is needed.
    See http://bugs.jython.org/issue1499
  * want to enhance driver without need for JDK or Java.

Do not use this if:

  * full http://www.python.org/peps/pep-0249.html compliance is needed

Main reason for existence of this module was for performing Ingres tests
so whilst support for other databases is possible this is currently not
tested.

If you want to hack on this, become familar with the JDBC api :-)

  * http://download.oracle.com/javase/1.4.2/docs/api/java/sql/Statement.html
  * http://download.oracle.com/javase/1.4.2/docs/api/java/sql/PreparedStatement.html
  * http://download.oracle.com/javase/1.4.2/docs/api/java/sql/CallableStatement.html
  * http://download.oracle.com/javase/1.4.2/docs/api/java/sql/ResultSet.html#getMetaData%28%29

enabling Ingres JDBC tracing at the command line is easy:

    jython -Dingres.jdbc.trace.timestamp=ON -Dingres.jdbc.trace.log=ingres.jdbctrace.log  -Dingres.jdbc.trace.drv=5 ....
    jython -Dingres.jdbc.trace.timestamp=ON -Dingres.jdbc.trace.log=ingres.jdbctrace.log  -Dingres.jdbc.trace.drv=5 -Dingres.jdbc.trace.msg.tl=5 ....  # Hex trace

Logs to: ingres.jdbctrace.log

"""

import sys
import os
import string
import exceptions
import weakref
import array

import jarray

try:
    import logging
except ImportError:
    """This is probably Jython 2.2 or earlier.
    NOTE decimal module from Python 2.4 will not work
    with Jython 2.1 without extra work
    
    Backports is not included but can be easily created:
    
        backports/__init__.py           empty file
        backports/decimal.py            from python 2.4
        backports/logging/__init__.py   from python 2.4
        backports/logging/config.py     from python 2.4
        backports/logging/handlers.py   from python 2.4
    
    Example:
        export TMP_PYDR=/usr/lib/python2.4/
        mkdir backports
        cd backports
        touch __init__.py
        cp ${TMP_PYDR}/decimal.py .
        cp -R ${TMP_PYDR}/logging .
    
    NOTE issues with "finally" blocks which started to creep into test suite.
    """
    from backports import logging

try:
    import decimal
except ImportError:
    from backports import decimal

import datetime
import time

import java
import java.math
try:
    import java.sql
except ImportError:
    # probably jython 2.2.1, which has some odd bugs, workaround time
    from java.sql import Types
    import java.sql
from java.util.concurrent import Executors   # Java 1.5 feature
# below are not needed in Java JRE 6 but with OpenJDK they are needed
#import java.lang

from ._version import __version__, __version_info__

paramstyle = 'qmark'  # if want to ever change this, consider https://github.com/cpburnz/python-sql-parameters
apilevel = '2.0'
threadsafety = 0  # NO thread testing has been made. FIXME this should be examined


#  ** DBI exceptions hierarchy taken as-is from 2.0 spec http://www.python.org/peps/pep-0249.html


class Error(exceptions.StandardError):
    def __init__(self, error_text, sqlcode=0, sqlstate='', sql_statement=None):  # should sqlstate be string or simply hex (i.e. int)? String matches iiapi.h defs
        self.error_text = error_text
        #self.sqlcode = int(sqlcode) # typecast may be over kill but lets be safe
        #self.sqlstate = str(sqlstate) # typecast may be over kill but lets be safe
        self.sqlcode = sqlcode
        self.sqlstate = sqlstate
        self.sql_statement = sql_statement
        self.args = (self.error_text, self.sqlcode, self.sqlstate, sql_statement)


class Warning(exceptions.StandardError):
    pass


class InterfaceError(Error):
    pass


class DatabaseError(Error):
    pass


class InternalError(DatabaseError):
    pass


class OperationalError(DatabaseError):
    pass


class ProgrammingError(DatabaseError):
    pass


class IntegrityError(DatabaseError):
    pass


class DataError(DatabaseError):
    pass


class NotSupportedError(DatabaseError):
    pass


#  * DBI Type/object based on 2.0 spec http://www.python.org/peps/pep-0249.html example


class DBAPITypeObject(object):
    def __init__(self, *args, **kwargs):
        self.values = args
        name = kwargs.get('name')
        self.name = name
    
    def __cmp__(self, other):
        if other in self.values:
            return 0
        if other < self.values:
            return 1
        else:
            return -1
    
    def __repr__(self):
        if self.name:
            return self.name
        else:
            return self.__class__.__name__  # FIXME this is not pretty

# DBI Types, see java.sql.Types http://download.oracle.com/javase/1.4.2/docs/api/java/sql/Types.html

# NOTE java.sql.Types.NVARCHAR + ..Types.LONGNVARCHAR added in Java 1.6
STRING = DBAPITypeObject(java.sql.Types.VARCHAR,
                            java.sql.Types.CHAR,
                            java.sql.Types.CLOB,
                            java.sql.Types.LONGVARCHAR,
                            name='STRING')

NUMBER = DBAPITypeObject(java.sql.Types.BIGINT,
                            java.sql.Types.INTEGER,
                            java.sql.Types.TINYINT,
                            java.sql.Types.SMALLINT,
                            java.sql.Types.FLOAT,
                            java.sql.Types.REAL,
                            java.sql.Types.DOUBLE,
                            java.sql.Types.NUMERIC,
                            java.sql.Types.DECIMAL,
                            name='NUMBER')

DATETIME = DBAPITypeObject(java.sql.Types.TIMESTAMP,
                            # FIXME/TODO pep-249 is unclear on whether the following should be included:
                            java.sql.Types.DATE,
                            java.sql.Types.TIME,
                            name='DATETIME')
                            
BINARY = DBAPITypeObject(java.sql.Types.BINARY,
                            java.sql.Types.VARBINARY,
                            java.sql.Types.LONGVARBINARY,
                            java.sql.Types.BLOB,
                            name='BINARY')

ROWID = DBAPITypeObject(java.sql.Types.OTHER,  #...for want of a better type
                            name='ROWID')
# NOTE ROWID .lastrowid not implemented yet ... pick up from meta data .isAutoIncrement(x)


class JyJDBCType(object):
    """Simple wraper type, used by driver to allow conversion when being sent
    via JDBC
    """
    def __init__(self, value, jdbc_type):
        self.value = value
        self.jdbc_type = jdbc_type


if sys.version_info < (2, 7):
    # pre-Jython 2.7
    def str2byte(in_str):
        return jarray.array(in_str, 'b')
else:
    def str2byte(in_str):
        return array.array('b', in_str)  # signed char -- appears to match old 2.5.3 and earlier behavior of: jarray.array(in_str, 'b')
        # None of the below work correctly :-(
        #return array.array('B', in_str)  # unsigned char
        #return bytes(in_str)
        #return buffer(in_str)

def Binary(string):
    """This function constructs an object capable of holding a
    binary (long) string value.

    Returns a binary object which avoids Unicode processing.
    """
    # TODO add a check (not an assert) for python (byte) string type
    # NOTE zentus sqlitejdbc doesn't understand array of byte, it only handles "str" type
    return JyJDBCType(str2byte(string), java.sql.Types.BINARY)

Date = datetime.date
Time = datetime.time
Timestamp = datetime.datetime


def DateFromTicks(ticks):
    """This function constructs an object holding a date value
    from the given ticks value (number of seconds since the
    epoch; see the documentation of the standard Python time
    module for details).
    """
    return apply(Date, time.localtime(ticks)[:3])


def TimeFromTicks(ticks):
    """This function constructs an object holding a time value
    from the given ticks value (number of seconds since the
    epoch; see the documentation of the standard Python time
    module for details).
    """
    return apply(Time, time.localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
    """This function constructs an object holding a time stamp
    value from the given ticks value (number of seconds since
    the epoch; see the documentation of the standard Python
    time module for details).
    """
    return apply(Timestamp, time.localtime(ticks)[:6])

###############
_drivers_loaded = {}  # keep track of what drivers have been loaded

try:
    # Ingres specific jar file loading
    # Always try and load the Ingres driver
    import com.ingres.jdbc.IngresDriver
    _drivers_loaded['com.ingres.jdbc.IngresDriver'] = True
except ImportError:
    # classpath is (probably) wrong, caller should add jar file to class path
    pass

def get_default_port():
    """Generates a DAS port suitable for use with Ingres.
    Attempts to pick the local installation listen address,
    defaults to the out-of-box default if unable to find a local installation.
    """
    result = defport = 'II7'
    II_SYSTEM = os.environ.get('II_SYSTEM')
    if II_SYSTEM is not None:
        config_dat_path = os.path.join(II_SYSTEM, 'ingres', 'files', 'config.dat')
        try:
            f = open(config_dat_path)
            # could use a regex here... not sure on performance
            for line in f:
                # Not a great search string but good enough
                if '.gcd.*.tcp_ip.port' in line.lower():
                    result = line.split(':')[1]
                    result = result.strip()
                    break
        except IOError:
            result = defport
    return result


def gen_ingres_connect_string(ingres_dbname, ingres_driver_uri='ingres', default_gcd_port=None):
    """Generate a default JDBC connection string suitable for connecting
    to an Ingres installation. See iijdbcprop tool for other options.
    """
    default_gcd_port = default_gcd_port or get_default_port()

    url = "jdbc:%s://localhost:%s/%s;select_loop=on" % (ingres_driver_uri, default_gcd_port, ingres_dbname)
    return url


#############################
"""_to_python_mappings() and _to_python() are used for database results and
input bind parameters respectively. Basically an ultra simplistic version of
SQLAlchemy's Custom Types, http://www.sqlalchemy.org/docs/core/types.html#custom-types
specifically the types.TypeDecorator methods process_bind_param() and process_result_value()
"""


def _array_conv(x):
    """Convert JDBC Binary type into Python 2.x (byte) string.
    Typically used for BLOB/LONG BYTE/BYTE/VARBYTE/BINARY/etc. SQL types
    """
    if x.typecode == 'b':
        return x.tostring()  # Convert to a byte string (i.e. not Unicode)
    return x  # no conversion

if sys.version_info < (2, 3):
    """Accessing x.typecode (when using jdbc type BLOB, after
    getBytes()) in Jython 2.2 causes:
    
    java.lang.IllegalArgumentException: Cannot create PyString from null!
    
    NOT sure on impact for CLOB/NCLOB (or other array types) so this is a
    Jython 2.2 special case.
    """
    
    def _array_conv(x):
        """Convert JDBC Binary type into Python 2.x (byte) string.
        Typically used for BLOB/LONG BYTE/BYTE/VARBYTE/BINARY/etc. SQL types
        """
        return x.tostring()  # Convert to a byte string (i.e. not Unicode)

_to_python_mappings = {
    java.math.BigDecimal: lambda d: decimal.Decimal(str(d)),
    java.sql.Date: lambda d: datetime.date(*map(int, d.toString().split('-'))),
    java.sql.Time: lambda d: datetime.time(*map(int, d.toString().split(':'))),
    java.sql.Timestamp: lambda d: datetime.datetime(*map(int, d.toString().replace('.', ' ').replace(':', ' ').replace('-', ' ').split())),  # NOTE negative times if they exist (not sure with JDBC) would cause issues
    #java.sql.Timestamp: lambda d: datetime.datetime(),  # could use python 2.5+ .strptime() with input from .toString()
    array.array: _array_conv,  # Binary array
}


JDBCTYPE2NAME = {}
for x in dir(java.sql.Types):
    if x[0] in string.ascii_uppercase:
        JDBCTYPE2NAME[getattr(java.sql.Types, x)] = x


def _to_python(jval):
    """Convert Java/JDBC object (i.e. SELECT/dbprocedure result) into Python object
    Currently uses the Java object type/class to determine the conversion process.
    TODO consider using the jdbc type code, e.g. java.sql.Types.VARCHAR.
        The type code could be optional with class type as a backup/last-ditch conversion."""
    if isinstance(jval, java.sql.Blob):
        # A lob locator - for now grab all the data and convert.
        # There is the (future) option to lazy evaluate the data
        # (the caller may throw the result away) via a proxy object
        lob_len = jval.length();
        jval = jval.getBytes(1, lob_len)
    elif isinstance(jval, java.sql.Clob):
        # A lob locator - for now grab all the data and convert.
        lob_len = jval.length();
        jval = jval.getSubString(1, lob_len)
    
    try:
        pval = _to_python_mappings[jval.__class__](jval)
    except KeyError:
        pval = jval  # Leave the Java object as-is (Python can usually deal with it)
    return pval

_from_python_mappings = {
    # Python type:  (function to convert from Python to Java/JDBC type, java sql (DBMS) type to bind as)
    type(None): ((lambda d: d), java.sql.Types.NULL),
    decimal.Decimal: ((lambda d: java.math.BigDecimal(str(d))), java.sql.Types.DECIMAL),
    int: ((lambda d: d), java.sql.Types.BIGINT),  # TODO check older Ingres clients that do not support 8 byte ints. Also check long type: java.lang.Long
    JyJDBCType: ((lambda d: d.value), java.sql.Types.BINARY),
    str: ((lambda d: d), java.sql.Types.VARCHAR),  # FIXME tricky as this is really bytes and will likely go through site packages default locale. should use the II_CHARSET setting to determine character set and convert to Unicode
    unicode: ((lambda d: d), java.sql.Types.VARCHAR),  # NOTE java.sql.Types.NVARCHAR added in Java 1.6
    datetime.date: ((lambda d: java.sql.Date.valueOf(d.isoformat())), java.sql.Types.DATE),
    datetime.time: ((lambda d: java.sql.Time.valueOf(d.strftime('%H:%M:%S'))), java.sql.Types.TIME),  # NOTE datetime.time sub seconds are truncated and lost
    datetime.datetime: ((lambda d: java.sql.Timestamp.valueOf(d.strftime('%Y-%m-%d %H:%M:%S') + ('.%d' % d.microsecond))), java.sql.Types.TIMESTAMP),
    # Timestamp use isoformat()? NOTE issue of Olsen (java) timezone name versus Ingres name (devolves into gmt offset with no DST awareness)
    #: (, java.sql.Types.VARCHAR),
}


def _from_python(pval):
    """Convert Python object (i.e. bind parameter) into Java/JDBC object
    suitable for use with JDBC api"""
    try:
        tmpfunction, tmptype = _from_python_mappings[type(pval)]
        jval = tmpfunction(pval)
    except KeyError:
        # NOTE java.sql.Types.NVARCHAR added in Java 1.6
        jval, tmptype = str(pval), java.sql.Types.VARCHAR  # FIXME I'm not happy with this, note str used and NOT unicode (For Ingres should use the II_CHARSET setting to determine character set and convert to Unicode)
    return jval, tmptype


class Cursor(object):
    def __init__(self, connection):
        self._connection = connection
        self._logger = self._connection._logger
        self.lastrowid = None  # FIXME see http://community.ingres.com/wiki/JDBC_Identity_Column_Support_As_Generated_Keys - specifically IDENTITY=on
        self.arraysize = 1  # TODO should probably be a property to prevent updates (TODO Bulk operations support)
        self._rs = None
        self._stmt = None
        self._reset()
        self._use_prepared = False  # NOTE can not use select loops with JDBC if this is true (SELECT LOOPS are more significantly performant but do have some limitations)
        self._callproc_force_input_only = self._connection._callproc_force_input_only
        self._timeout = 0  # jyjdbc extension to pep-249, non-zero values are sent to statement.setQueryTimeout()
    
    def _ensure_not_closed(self, caller_name):
        if self._connection is None:
            # got closed at some point
            sql_text = self._last_sql_text
            raise Error(error_text='%s method when %s is closed.' % (caller_name, self.__class__.__name__), sqlcode=None, sqlstate=None, sql_statement=sql_text)
    
    def _reset(self):
        # FIXME rowcount never gets updated by execute/callproc/fetch*
        self.rowcount = -1  # TODO should probably be a property to prevent updates
        self.description = None
        self._last_sql_text = None
        self._number_of_result_columns = 0
    
    def _close_current_statement_no_check(self):
        """If there is an active query, close/abort it
        """
        self._logger.debug('ENTRY: cursor _close_current_statement_no_check')
        if self._rs:
            self._rs.close()
            self._rs = None
        if self._stmt:
            self._stmt.close()
            self._stmt = None
    
    def callproc(self, procname, parameters=None, parameter_names=None, force_input_only=None):
        """(This method is optional since not all databases provide
            stored procedures. [3])
            
            Call a stored database procedure with the given name. The
            sequence of parameters must contain one entry for each
            argument that the procedure expects. The result of the
            call is returned as modified copy of the input
            sequence. Input parameters are left untouched, output and
            input/output parameters replaced with possibly new values.
            
            The procedure may also provide a result set as
            output. This must then be made available through the
            standard .fetch*() methods.
            
            parameter_names is a non-standard extension;
            parameter_names is an optional indexable (e.g. tuple)
            of parameter names, that will be used for named parameters.
            
            force_input_only is a non-standard extension;
            if specified does NOT use BYREF (In/Out) parameters.
        """
        self._ensure_not_closed(sys._getframe().f_code.co_name)
        self._close_current_statement_no_check()
        self._reset()

        if force_input_only is None:
            force_input_only = self._callproc_force_input_only
        if force_input_only:
            MARK_PARAMETERS_AS_OUTPUT = False
        else:
            MARK_PARAMETERS_AS_OUTPUT = True  # make parameters By Reference (BYREF)
        have_results = False

        """
        if parameters:
            raise NotSupportedError('bind parameter support not implemented')
        """

        sql_text = '{ call %s }' % procname  # TODO return code

        if parameters:
            param_marker = '?'  # Standard for ODBC, JDBC. Just like pep-249 paramstyle == 'qmark'
            
            number_of_params = len(parameters)
            if number_of_params > 0:
                pmarker_str = ', '.join([param_marker for dummy_values in range(number_of_params)])
                sql_text = '{call %s (%s)}' % (procname, pmarker_str)  # TODO return code
        try:
            self._logger.debug('callproc sql_text %r', sql_text)
            callable_stmt = self._connection._jdbcconnection.prepareCall(sql_text)
            #print 'callable_stmt', dir(callable_stmt)

            # get stored procedure metadata
            # http://docs.oracle.com/javase/7/docs/api/java/sql/DatabaseMetaData.html#getProcedureColumns%28java.lang.String,%20java.lang.String,%20java.lang.String,%20java.lang.String%29
            # https://docs.oracle.com/javadb/10.6.2.1/ref/rrefpgc1.html
            # http://www.java2s.com/Code/Java/Database-SQL-JDBC/GetStoredProcedureSignature.htm
            db_metadata = self._connection._jdbcconnection.getMetaData()  # DatabaseMetaData
            rs = db_metadata.getProcedureColumns(None, None, procname, '%')  # ResultSet
            dbproc_param_types = []
            while rs.next():
                column_datatype = rs.getInt(6)
                # TODO check return type (procedureColumnIn, procedureColumnInOut, etc.)
                dbproc_param_types.append(column_datatype)
            rs.close()


            ## See http://community.ingres.com/wiki/Calling_Stored_Procedures#Stored_procedure_call_using_IN_and_OUT_statements
            if parameters:
                # FIXME callproc() and execute() both need to deal with bind parameters
                # they should share code and note duplicate each other
                # FIXME TODO use _bind_params()
                param_counter = 0
                for param_counter, temp_param in enumerate(parameters):
                    if parameter_names:
                        # named parameters (has potential to be extended to handle dict parameters)
                        param_pos_indicator = parameter_names[param_counter]
                        #param_pos_indicator = 'A'  # experimental named parameter test (for example, if parameters is a dict)
                    else:
                        # positional parameters
                        param_pos_indicator = param_counter + 1
                    temp_param, dbms_type = _from_python(temp_param)
                    if dbproc_param_types:
                        dbms_type = dbproc_param_types[param_counter]  # use declared type from metadata
                    self._logger.debug('setObject %r', (param_pos_indicator, type(temp_param), repr(temp_param), JDBCTYPE2NAME[dbms_type]))
                    #dbms_type = java.sql.Types.VARCHAR  # fixme lookup/map
                    if MARK_PARAMETERS_AS_OUTPUT:
                        callable_stmt.setObject(param_pos_indicator, temp_param)
                        callable_stmt.registerOutParameter(param_pos_indicator, dbms_type)
                        have_results = True
                    else:
                        ## http://download.oracle.com/javase/1.3/docs/api/java/sql/PreparedStatement.html#setObject%28int,%20java.lang.Object,%20int%29
                        ## NOTE scale parameter option
                        ## With Ingres JDBC driver simply using; callable_stmt.setObject(param_pos_indicator, temp_param)
                        ## results in strings being used.
                        if dbms_type == java.sql.Types.DECIMAL:
                            callable_stmt.setObject(param_pos_indicator, temp_param, dbms_type, temp_param.scale())
                        else:
                            callable_stmt.setObject(param_pos_indicator, temp_param, dbms_type)
                    #print dir(java.sql.Types)
            
            call_result = callable_stmt.execute()
            if call_result:
                self._rs = callable_stmt.getResultSet()
                self.description = self._gen_description()
        except java.sql.SQLException, info:
            ############
            #print java.sql.SQLException, info
            #import traceback
            #traceback.print_exc()
            #raise
            #############
            raise DatabaseError(error_text=info.getMessage(), sqlcode=info.errorCode, sqlstate=info.getSQLState(), sql_statement=sql_text)

        if have_results:
            # Assume same number of result parameters as input parameters
            number_of_result_columns = len(parameters)
            result = []
            for x in range(1, number_of_result_columns + 1):
                #result.append(_to_python(callable_stmt.getObject(x)))
                # Debug above broken into steps for easy debugging
                dummy_debug1 = callable_stmt.getObject(x)
                dummy_debug2 = _to_python(dummy_debug1)
                result.append(dummy_debug2)
            result = tuple(result)
        else:
            result = parameters
        self._logger.debug('result %r', result)

        return result


    def _bind_params(self, stmt, params):
        # probably don't need to pass stmt but just in case...
        param_counter = 0
        #import pdb ; pdb.set_trace()
        for temp_param in params:
            param_counter = param_counter + 1
            temp_param, dbms_type = _from_python(temp_param)
            self._logger.debug('setObject %r', (param_counter, type(temp_param), JDBCTYPE2NAME[dbms_type], repr(temp_param)))
            if dbms_type == java.sql.Types.DECIMAL:
                stmt.setObject(param_counter, temp_param, dbms_type, temp_param.scale())
            else:
                stmt.setObject(param_counter, temp_param, dbms_type)
        
        return param_counter


    def _gen_description(self):
        """Determine result description, currently works by side effects
        """
        if self._rs:
            # Number of result columns?
            self._number_of_result_columns = self._rs.getMetaData().getColumnCount()
            self._logger.debug('self._number_of_result_columns %r', self._number_of_result_columns)
        
        if self._number_of_result_columns == 0:
            tuple_description = None
        else:
            tuple_description = []
            result_metadata = self._rs.getMetaData()
            name = type_code = display_size = internal_size = precision = scale = null_ok = None # FIXME
            self._logger.debug('Number of result columns %r', self._number_of_result_columns)
            for x in range(1, self._number_of_result_columns + 1):
                name = type_code = display_size = internal_size = precision = scale = null_ok = None # FIXME
                # Required
                name = result_metadata.getColumnName(x)
                jdbc_type_code = result_metadata.getColumnType(x) # e.g. 1=char/c, 12=varchar, etc. See SQL type from java.sql.Types http://download.oracle.com/javase/1.4.2/docs/api/java/sql/Types.html
                dbms_ddl_type = result_metadata.getColumnTypeName(x)
                type_code = DBAPITypeObject(jdbc_type_code, name=dbms_ddl_type) # NOTE jdbc driver returns varchar rather than nvarchar for nvarchar result type as there is no nvarchar type in JDBC (NOTE java.sql.Types.NVARCHAR added in Java 1.6)
                self._logger.debug('Result column %r of %r: %r %r %r (%r)', x, self._number_of_result_columns, name, type_code, JDBCTYPE2NAME.get(jdbc_type_code), jdbc_type_code)
                # Optional
                null_ok = result_metadata.isNullable(x) # see columnNullable/columnNoNulls constants FIXME (make bool)
                precision = result_metadata.getPrecision(x)
                scale = result_metadata.getScale(x)
                column_descriptor = name, type_code, display_size, internal_size, precision, scale, null_ok
                tuple_description.append(column_descriptor)
        
        return tuple_description

    def _execute(self, sql_text, params=None, param_array=None):
        self._ensure_not_closed(sys._getframe().f_code.co_name)
        self._logger.debug('ENTRY: _execute: %r %r', sql_text, params)
        ## TODO add setQueryTimeout() call to Statement (or PreparedStatement) object.
        ## http://docs.oracle.com/javase/1.5.0/docs/api/java/sql/Statement.html
        ## http://docs.oracle.com/javase/1.5.0/docs/api/java/sql/Statement.html#setQueryTimeout%28int%29
        # Check if attempting to re-use same query text as last call
        # TODO add an LRU cache, currently only one prepared query is cached
        if self._last_sql_text == sql_text:
            # should be able to re-use the existing (prepared) statement
            if isinstance(self._stmt, java.sql.PreparedStatement):
                self._logger.debug('ENTRY: _execute: re-using PreparedStatement')
                # clear just in case bind param count is different
                self._stmt.clearParameters()
            else:
                if params or param_array:
                    self._close_current_statement_no_check()
                else:
                    self._logger.debug('ENTRY: _execute: re-using Statement')
        else:
            self._close_current_statement_no_check()
        self._reset()
        self._last_sql_text = sql_text
        
        try:
            if param_array:
                # This is a bulk/batch operation using array/list/tuple/iterator/generator
                if self._stmt is None:
                    self._stmt = self._connection._jdbcconnection.prepareStatement(sql_text)
                    if self._timeout:
                        self._logger.debug('setQueryTimeout %r', self._timeout)
                        self._stmt.setQueryTimeout(self._timeout)
                
                p = iter(param_array)
                chunk_size = 1000  # TODO param option, use Cursor.arraysize if >1
                params_left = True
                while params_left:
                    for dummy in xrange(chunk_size):
                        try:
                            params = p.next()
                        except StopIteration:
                            params_left = False
                            break
                        self._bind_params(self._stmt, params)
                        self._stmt.addBatch()
                    batch_result_array = self._stmt.executeBatch()
                
                
                """Optional, check if each entry is:
                    >= 0 (sucess with row count)
                    java.sql.Statement.SUCCESS_NO_INFO (success no row count)
                    or java.sql.Statement.EXECUTE_FAILED
                For now rely on exception propagation.
                """
                # Whilst non-SELECT statements could be closed here,
                # defer in case same query text comes in again on
                # the next call which should perform faster.
            elif params:
                # This is a regular operation using bind parameters
                
                if self._stmt is None:
                    self._stmt = self._connection._jdbcconnection.prepareStatement(sql_text)
                    if self._timeout:
                        self._logger.debug('setQueryTimeout %r', self._timeout)
                        self._stmt.setQueryTimeout(self._timeout)

                #print dir(self._stmt)
                #print dir(self._stmt.metaData)
                # NOTE with sqlite JDBC driver this call will fail! sqlite needs the to be executed first
                #print 'nocols', self._stmt.getMetaData().getColumnCount()
                #print 'nocols', self._stmt.metaData.getColumnCount()
                
                self._bind_params(self._stmt, params)
                """
                if self._number_of_result_columns:
                    # SELECT
                    self._rs = self._stmt.executeQuery()  # works for select not insert, update, delete, etc.
                else:
                    # Not a SELECT, no result set
                    self._stmt.execute()
                    self._rs = self._stmt.getResultSet()
                """
                
                if self._stmt.execute():
                    self._rs = self._stmt.getResultSet()
            else:
                # No bind parameters, plain query text
                if self._stmt is None:
                    use_prepared = self._use_prepared
                    """Naive 'is it a DML query?' check.
                    This is required as prepared statements can only be
                    used for DML. Neither DDL nor DBMS specific statements
                    (e.g. change locking) can be used as prepared statements.
                    This checks the first words for DML statements,
                    so comments will confound it as will non-DML that start
                    with DML words.
                    
                    May be better to never prepared statements without
                    bind parameters"""
                    if use_prepared:
                        query_start = sql_text[:6]
                        query_start = query_start.lower()
                        use_prepared = False
                        for dml_start in ('select', 'insert', 'update', 'delete'):
                            if query_start.startswith(dml_start):
                                use_prepared = True
                                break
                    if use_prepared:
                        self._stmt = self._connection._jdbcconnection.prepareStatement(sql_text)
                    else:
                        self._stmt = self._connection._jdbcconnection.createStatement()
                    if self._timeout:
                        self._logger.debug('setQueryTimeout %r', self._timeout)
                        self._stmt.setQueryTimeout(self._timeout)

                if isinstance(self._stmt, java.sql.PreparedStatement):
                    is_select = self._stmt.execute()
                else:
                    is_select = self._stmt.execute(sql_text)
                
                if is_select:
                    self._logger.debug('have a result set')
                    # get ResultSet object
                    # http://download.oracle.com/javase/1.4.2/docs/api/java/sql/ResultSet.html
                    self._rs = self._stmt.getResultSet()
        except java.sql.SQLException, info:
            ############
            #print java.sql.SQLException, info
            #import traceback
            #traceback.print_exc()
            #raise
            #############
            error_text = info.getMessage()
            self._logger.debug('ERROR: execute: %r', error_text)
            raise DatabaseError(error_text=error_text, sqlcode=info.errorCode, sqlstate=info.getSQLState(), sql_statement=sql_text)
    
        '''
        try:
            self._rs = self._stmt.executeQuery(sql_text) # this returns http://download.oracle.com/javase/1.4.2/docs/api/java/sql/ResultSet.html
        except java.sql.SQLException, info:
            if 802839 == info.getErrorCode():
                # not a select?
                self._number_of_result_columns = 0
                self._rs = None
            else:
                """
                print info
                print dir(info)
                print info.errorCode
                print info.getSQLState()
                print info.getLocalizedMessage()
                print info.getMessage()
                """
                raise DatabaseError(error_text=info.getMessage(), sqlcode=info.errorCode, sqlstate=info.getSQLState(), sql_statement=sql_text)
        '''


        # TODO self.description could be a property, for now simply make it an attribute
        self.description = self._gen_description()
        self._logger.debug('EXIT: _execute')
    
    def execute(self, sql_text, params=None):
        self._ensure_not_closed(sys._getframe().f_code.co_name)
        self._logger.debug('ENTRY: execute: %r %r', sql_text, params)
        self._execute(sql_text, params)
        self._logger.debug('EXIT: execute')
    
    def executemany(self, operation, seq_of_parameters):
        self._ensure_not_closed(sys._getframe().f_code.co_name)
        self._logger.debug('ENTRY: executemany')
        self._execute(operation, param_array=seq_of_parameters)
        self._logger.debug('EXIT: executemany')
    
    def fetchone(self):
        self._ensure_not_closed(sys._getframe().f_code.co_name)
        self._logger.debug('ENTRY: fetchone')
        if self.description is None:
            # Simple is a query with results test
            sql_text = self._last_sql_text
            raise Error(error_text='fetch method called with no open query', sqlcode=None, sqlstate=None, sql_statement=sql_text)
        
        if self._rs is None:
            row = None
        else:
            if self._rs.next():
                row = []
                for x in range(1, self._number_of_result_columns + 1):
                    row.append(_to_python(self._rs.getObject(x)))
                row = tuple(row)
            else:
                row = None
        self._logger.debug('fetch %r', row)
        return row
    
    def fetchmany(self, size=None):
        self._logger.debug('ENTRY: fetchmany')
        self._ensure_not_closed(sys._getframe().f_code.co_name)
        size = size or self.arraysize

        result = []
        for _ in range(size):
            row = self.fetchone()
            if row:
                result.append(row)
            else:
                break
        self._logger.debug('fetchmany result: %r', result)
        return result
    
    def fetchall(self):
        """Naive "get-em-all" fetch all.
        Returns a list so can/will consume lots of memory and will stall
        until last fetch completes.
        """
        self._ensure_not_closed(sys._getframe().f_code.co_name)
        retArray = []
        row = self.fetchone()
        while row != None:
            retArray.append(row)
            row = self.fetchone()
        return retArray
    
    def _real_close(self):
        self._logger.debug('ENTRY: cursor _real_close')
        self._close_current_statement_no_check()
        self._reset()
        # This is probably overkill....
        del(self._connection._cursors[id(self)])
        self._connection = None
        
    def close(self):
        self._logger.debug('ENTRY: cursor close')
        self._ensure_not_closed(sys._getframe().f_code.co_name)
        self._real_close()
    
    def __del__(self):
        self.close()

    def setinputsizes(self, sizes):
        """This can be used before a call to .execute*() to
        predefine memory areas for the operation's parameters.
        
        sizes is specified as a sequence -- one item for each
        input parameter.  The item should be a Type Object that
        corresponds to the input that will be used, or it should
        be an integer specifying the maximum length of a string
        parameter.  If the item is None, then no predefined memory
        area will be reserved for that column (this is useful to
        avoid predefined areas for large inputs).
        
        This method would be used before the .execute*() method
        is invoked.
        
        Implementations are free to have this method do nothing
        and users are free to not use it.
        
        THIS implementation does nothing.
        """
        pass

    def setoutputsize(self, sizes, column=None):
        """Set a column buffer size for fetches of large columns
        (e.g. LONGs, BLOBs, etc.).  The column is specified as an
        index into the result sequence.  Not specifying the column
        will set the default size for all large columns in the
        cursor.
        
        This method would be used before the .execute*() method
        is invoked.
        
        Implementations are free to have this method do nothing
        and users are free to not use it.

        THIS implementation does nothing.
        """
        pass


class Connection(object):
    Error = Error
    Warning = Warning
    InterfaceError = InterfaceError
    DatabaseError = DatabaseError
    InternalError = InternalError
    OperationalError = OperationalError
    ProgrammingError = ProgrammingError
    IntegrityError = IntegrityError
    DataError = DataError
    NotSupportedError = NotSupportedError
    # Sets up optional 2.0 extension to expose exceptions in connection
    
    def __init__(self, dsn=None, user=None, password=None, driver_name='com.ingres.jdbc.IngresDriver', debug=None, callproc_force_input_only=False):
        """Connect to JDBC driver.
        
        @param dsn - JDBC connection string/url. This parameter is defined as
        optional but is currently required (marked as optional for future
        functionality).
        
        @param user - Optional name to connect as.
        
        @param password - Optional password for `user`.
        
        @param driver_name - EXTENSION the Java driver class name. If set to
        None, no attempt is made to load the driver (assume driver was
        pre-loaded).
        
        @param debug - EXTENSION if True enables internal tracing/logging.
        
        @param callproc_force_input_only - EXTENSION if True dbproc params are assumed to be input and not output/byref. May only be useful for Ingres.
        
        TODO implement "host", "database" (name), and "port" (for Ingres only)
        """
        log_format = '%(asctime)s %(levelname)s %(message)s'
        log_format = '%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s'
        logging.basicConfig(format=log_format)
        self._logger = logging.getLogger("jdbc")
        
        if debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.NOTSET)  # only logs; WARNING, ERROR, CRITICAL
        self._logger.debug("debug logging started")
        self._logger.debug("connection parameters: %r", (dsn, driver_name, debug))
        
        #self._logger.debug("debug message")
        #self._logger.info("info message")
        #self._logger.warn("warn message")
        #self._logger.error("error message")
        #self._logger.critical("critical message")
        
        self._autocommit = False
        
        url = dsn
        if driver_name:
            if 'ingres' in driver_name:
                # TODO 'edbc' check?
                ingres_dbname = dsn
                if not ingres_dbname.startswith('jdbc:'):
                    url = gen_ingres_connect_string(ingres_dbname)
                else:
                    url = ingres_dbname
            
            # load JDBC driver, if not already loaded
            if _drivers_loaded.get(driver_name) is None:
                self._logger.debug('Attempting to load %r', driver_name)
                java.lang.Class.forName(driver_name).newInstance()
                _drivers_loaded[driver_name] = True
        
        self._logger.debug('url %r', url)

        if user:
            self._jdbcconnection = java.sql.DriverManager.getConnection(url, user, password)
        else:
            self._jdbcconnection = java.sql.DriverManager.getConnection(url)
        self._jdbcconnection.setAutoCommit(self._autocommit)
        self._logger.debug('getClass %r', self._jdbcconnection.getClass())
        self._meta_data = self._jdbcconnection.getMetaData()
        self._logger.debug('DatabaseProductName %r', self._meta_data.getDatabaseProductName())
        self.dbversion = self._meta_data.getDatabaseProductVersion()  # zxJDBC extension
        self._logger.debug('DatabaseProductVersion %r', self.dbversion)
        self._logger.debug('DriverVersion %r', self._meta_data.getDriverVersion())
        self._logger.debug('DriverMajorVersion %r', self._meta_data.getDriverMajorVersion())
        self._logger.debug('DriverMinorVersion %r', self._meta_data.getDriverMinorVersion())
        self._logger.debug('DriverName %r', self._meta_data.getDriverName())
        self._cursors = weakref.WeakValueDictionary()  # Used to keep track of cursors spawned by this connection
        self._callproc_force_input_only = callproc_force_input_only
        self._timeout_msecs = 0  # jyjdbc extension to pep-249, non-zero values are sent to connection.setNetworkTimeout()
        if self._timeout_msecs:
            num_threads = 1
            try:
                time_out_func = self._jdbcconnection.setNetworkTimeout
            except AttributeError:
                # this is NOT JRE7 / Java 1.7
                raise
                time_out_func = None
                self._logger.debug('setNetworkTimeout requested and not available (needs JRE7)')
            if time_out_func:
                self._logger.debug('setNetworkTimeout %r', self._timeout_msecs)
                # NOTE driver may not implement this....
                time_out_func(Executors.newFixedThreadPool(num_threads), self._timeout_msecs)
        # TODO mix of secs and msecs with these...
        # conn.setNetworkTimeout(Executors.newFixedThreadPool(numThreads), yourTimeout);
        # http://stackoverflow.com/questions/10654547/how-to-use-java-sql-connection-setnetworktimeout

    def _ensure_not_closed(self, caller_name):
        if self._jdbcconnection is None:
            # got closed at some point
            raise Error(error_text='%s method when %s is closed.' % (caller_name, self.__class__.__name__), sqlcode=None, sqlstate=None, sql_statement=None)
        elif self._jdbcconnection.closed:
            # got closed at some point - not sure how though
            raise Error(error_text='%s method when %s is closed.' % (caller_name, self.__class__.__name__), sqlcode=None, sqlstate=None, sql_statement=None)

    def commit(self):
        self._logger.debug('ENTRY: db commit')
        self._ensure_not_closed(sys._getframe().f_code.co_name)
        ## from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66062
        #this_function_name = sys._getframe().f_code.co_name
        #mywarning('%s.%s() not implemented' % (self.__class__.__name__, this_function_name))
        self._jdbcconnection.commit()
    
    def rollback(self):
        self._logger.debug('ENTRY: db rollback')
        self._ensure_not_closed(sys._getframe().f_code.co_name)
        self._jdbcconnection.rollback()
    
    def cursor(self):
        self._logger.debug('ENTRY: db cursor')
        self._ensure_not_closed(sys._getframe().f_code.co_name)
        curs = Cursor(self)
        self._cursors[id(curs)] = curs
        return curs
    
    def close(self):
        self._logger.debug('ENTRY: db close')
        self._ensure_not_closed(sys._getframe().f_code.co_name)
        for curs in list(self._cursors.values()):
            try:
                self._logger.debug('db close, last sql %r', curs._last_sql_text)
                curs._real_close()
                del(curs)
            except weakref.ReferenceError:
                # Already gone
                pass
        del(self._cursors)
        self._jdbcconnection.rollback()
        self._jdbcconnection.close()
        del(self._jdbcconnection)
        self._jdbcconnection = None
        
    def __del__(self):
        """NOTE I've not seen del ever called by the Jython/Java GC.
        """
        self._logger.debug('ENTRY: db __del__')
        self.close()


def connect(*args, **kwargs):
    return Connection(*args, **kwargs)
# Set connect doc string to the function that does all the work
connect.__doc__ = Connection.__init__.__doc__


########################
#
# Extras / Demos
#

def simple_execute(c, sql_query, bind_params=None):
    """Issue SQL, if query is a SELECT display (raw) results.
    
    Where c is a cursor"""
    print sql_query
    if bind_params is None:
        c.execute(sql_query)
    else:
        print bind_params
        c.execute(sql_query, bind_params)
    if c.description is not None:
        # it is a SELECT statement
        print c.description
        row = c.fetchone()
        while row:
            print row
            row = c.fetchone()
    print ''


def dumb_drop(c, obj_name, obj_type='table'):
    """NOTE1 schema name is expected to be in obj_name (or current schema used)
    NOTE2 delim'd id's need to be pre-delimited!"""
    sql_query = 'drop %s %s' % (obj_type, obj_name)
    try:
        c.execute(sql_query)
    except DatabaseError, info:
        #print 'DatabaseError', info
        pass
    except DataError, info:
        #print 'DataError', info
        pass


def main(argv=None):
    """Ingres specific demo showing simple select and database procedure usage.
    """
    if argv is None:
        argv = sys.argv

    # Horrible quick and dirty argument handling
    if len(argv) > 1:
        dbconstr = argv[1]
    else:
        dbconstr = 'iidbdb'
    
    db = connect(dbconstr)
    c = db.cursor()
    
    sql_text = "select dbmsinfo('_version') from iidbconstants"
    simple_execute(c, sql_text)

    table_name = 'jdbc_dbapi_demo'
    dumb_drop(c, table_name)

    sql_text = 'create table jdbc_dbapi_demo (col1 varchar(20))'
    c.execute(sql_text)
    
    dbproc_name = 'dbp_vc12_noparms'
    dbproc_name = 'dbp_jdbc_dbapi_demo'
    dumb_drop(c, dbproc_name, 'procedure')
    sql_query = '''create procedure DBPROC_NAME_MARKER  as
            begin
                INSERT INTO jdbc_dbapi_demo (col1) values ('fromdbproc');
            end
    '''
    
    sql_query = sql_query.replace('DBPROC_NAME_MARKER', dbproc_name)  # Avoid % (and {{}}) replacements
    print sql_query
    c.execute(sql_query)
    
    simple_execute(c, 'select * from jdbc_dbapi_demo')

    sql_query = "execute procedure DBPROC_NAME_MARKER".replace('DBPROC_NAME_MARKER', dbproc_name)
    print sql_query
    c.execute(sql_query)

    simple_execute(c, 'select * from jdbc_dbapi_demo')

    bind_params = None
    dbproc_result = c.callproc(dbproc_name, bind_params)
    print 'dbproc_result ', dbproc_result

    simple_execute(c, 'select * from jdbc_dbapi_demo')

    dbproc_name = 'dbp_vc12'
    dumb_drop(c, dbproc_name, 'procedure')
    sql_query = '''create procedure DBPROC_NAME_MARKER (a varchar(12)) as
            begin
                INSERT INTO jdbc_dbapi_demo (col1) values (a);
                
                a = NULL;
                a = '5';
                a = 'hello world!';
            end
    '''
    sql_query = sql_query.replace('DBPROC_NAME_MARKER', dbproc_name)  # Avoid % (and {{}}) replacements
    print sql_query
    c.execute(sql_query)
    
    simple_execute(c, 'select * from jdbc_dbapi_demo')

    sql_query = "execute procedure DBPROC_NAME_MARKER (a='test?')".replace('DBPROC_NAME_MARKER', dbproc_name)
    print sql_query
    c.execute(sql_query)

    simple_execute(c, 'select * from jdbc_dbapi_demo')

    bind_params = ('callproc!',)
    dbproc_result = c.callproc(dbproc_name, bind_params)
    print 'dbproc_result ', dbproc_result

    simple_execute(c, 'select * from jdbc_dbapi_demo')
    
    simple_execute(c, 'select ? from iidbconstants', (decimal.Decimal('123.456'),))


if __name__ == "__main__":
    sys.exit(main())
