#!/usr/bin/env python
# encoding: UTF-8
'''
###############################################################################################################################################################
##   File Name              : sqlplus_manager.py
##   File Description       : This is to handle SQL query preparation and execution
##   Modification History   : None
################################################################################################################################################################
## Token              When               Who                     What (Add SR/CR Reference)
## None               Jul 2016           Soumya                  - Initial Version
################################################################################################################################################################
'''

import os.path
import datetime
import tempfile
import subprocess
import HTMLParser


class SqlplusManager(object):

    QUERY_ERROR_HANDLER = '''WHENEVER SQLERROR EXIT SQL.SQLCODE;
WHENEVER OSERROR EXIT 9;
'''

    def __init__(self, database=None, username=None, password=None):
        if database and username and password:
            self.database = database
            self.username = username
            self.password = password
        else:
            raise Exception('Missing database configuration')

    def run_query(self, query, check_unknown_command=True):
        command = self.QUERY_ERROR_HANDLER + query
        return self._run_command(command, check_unknown_command=check_unknown_command)

    def run_script(self, script, check_unknown_command=True):
        if not os.path.isfile(script):
            raise Exception("Script '%s' was not found" % script)
        stream = open(script,'r')
        source = stream.read()
        filename = tempfile.mkstemp(prefix='sqlmanager-',
                                    suffix='.sql')[1]
        stream1 = open(filename, 'wb')
        stream1.write(self.QUERY_ERROR_HANDLER + source)
        stream1.close()
        try:
            return self._run_command("@%s" % filename, check_unknown_command=check_unknown_command)
        finally:
            os.remove(filename)
            stream.close()
            stream1.close()

    def _run_command(self, command, check_unknown_command):
        connection_url = self._get_connection_url()
        session = subprocess.Popen(['sqlplus', '-S', '-L', '-M', 'HTML ON',
                                    connection_url],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        session.stdin.write(command)
        output, _ = session.communicate()
        code = session.returncode
        if code != 0:
            raise Exception(OracleErrorParser.parse(output))
        else:
            if output:
                result = OracleResponseParser.parse(output, check_unknown_command=check_unknown_command)
                return result

    def _get_connection_url(self):
        return "%s/%s@%s" %(self.username, self.password, self.database)



class OracleResponseParser(HTMLParser.HTMLParser):

    UNKNOWN_COMMAND = 'SP2-0734: unknown command'

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.active = False
        self.result = []
        self.fields = []
        self.values = []
        self.header = True
        self.data = ''

    @staticmethod
    def parse(source, check_unknown_command):
        if OracleResponseParser.UNKNOWN_COMMAND in source and check_unknown_command:
            raise Exception(OracleErrorParser.parse(source))
        parser = OracleResponseParser()
        parser.feed(source)
        return tuple(parser.result)

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.active = True
        elif self.active:
            if tag == 'th':
                self.header = True
            elif tag == 'td':
                self.header = False

    def handle_endtag(self, tag):
        if tag == 'table':
            self.active = False
        elif self.active:
            if tag == 'tr' and not self.header:
                row = dict(zip(self.fields, self.values))
                self.result.append(row)
                self.values = []
            elif tag == 'th':
                self.fields.append(self.data.strip())
                self.data = ''
            elif tag == 'td':
                data = self.data.strip()
                self.values.append(data)
                self.data = ''

    def handle_data(self, data):
        if self.active:
            self.data += data


class OracleErrorParser(HTMLParser.HTMLParser):

    UNKNOWN_COMMAND = 'SP2-0734: unknown command'

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.active = False
        self.message = ''

    @staticmethod
    def parse(source):
        parser = OracleErrorParser()
        parser.feed(source)
        return '\n'.join([l for l in parser.message.split('\n') if l.strip() != ''])

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.active = True

    def handle_endtag(self, tag):
        if tag == 'body':
            self.active = False

    def handle_data(self, data):
        if self.active:
            self.message += data
