#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Test suite for zxjdbc and Ingres. Extends jyjdbc test to use zxjdbc.

Basically a sanity check to compare behaviors/behaviours between drivers.

Uses/requires old/original http://stuartbishop.net/Software/DBAPI20TestSuite/
(also see https://launchpad.net/dbapi-compliance).

Does not use the newer (http://code.google.com/p/acute-dbapi/)

For use with Jython 2.5.x.

Sample usage:
    c:\jython2.5.2\jython test_zxjdbcingres_dbapi20.py

"""

import unittest
import os
import sys

from com.ziclix.python.sql import zxJDBC

import jyjdbc

import test_jyjdbcingres_dbapi20

# Example (not used) explict jdbc connection string
jdbc_connect_str = 'jdbc:ingres://localhost:II7/jyjdbc_test;select_loop=on'

ingres_driver_uri = 'ingres'
default_gcd_port = jyjdbc.get_default_port()
# Try and find Ingres environment and construct connection string
jdbc_connect_str = "jdbc:%s://localhost:%s/%s;select_loop=on" % (ingres_driver_uri, default_gcd_port, test_jyjdbcingres_dbapi20.DATABASE_NAME)
username_str = None  # Assume local connection with Operating System auth
password_str = None  # Assume local connection with Operating System auth
ingres_driver_class = 'com.ingres.jdbc.IngresDriver'


class test_ZxJdbcIngres(test_jyjdbcingres_dbapi20.test_JyjdbcIngres):
    driver = zxJDBC
    connect_args = [jdbc_connect_str, username_str, password_str, ingres_driver_class]
    connect_kw_args = {}

if __name__ == '__main__':
    test_jyjdbcingres_dbapi20.main()
