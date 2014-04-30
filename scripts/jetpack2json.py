#!/usr/bin/env python
import os, re
from sys import stdout, stderr
from os.path import join, abspath, isfile, isdir, exists, basename
from shutil import copyfile, copytree, rmtree
from time import strftime, strptime, localtime
import urllib2
import MySQLdb as mdb
import sys
from yaml import load, dump

# speedy YAML
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

con = None
config_file = './amo_db_config.yml'
download_dir = abspath('./addons')

def getYaml(path):
    """ loadin' YAML files. """
    if not exists(path):
        raise Exception("YAML file doesn't exist: %s" % path)
    return load(file(path, 'r'), Loader)


if __name__ == '__main__':
    # database connection.
    dbConfig = getYaml(config_file)

    errors = []

    try:
        # con = mdb.connect('localhost', 'testuser',
        #     'test623', 'testdb');

        con = mdb.connect(dbConfig['host'],
            dbConfig['user'],
            dbConfig['password'],
            dbConfig['database'],
        );

        path = os.path.join(os.path.dirname(__file__), 'queries.yml')
        queries = getYaml(path)

        cur = con.cursor()
        # repack_query_limit
        cur.execute(queries['repack_query_limit'])
        # cur.execute(queries['repack_query'])

        rows = cur.fetchall()

        i = 0
        total_rows = len(rows)

        def date2Str(o):
            out = []
            url_tpl = 'https://addons.cdn.mozilla.net/storage/public-staging/%s/%s'
            for i in o:

                out.append(str(i))
            out.append(url_tpl % (o[0], o[5]))
            return out

        rows = map(date2Str, rows)

        from simplejson import dumps
        print dumps(rows)

    except mdb.Error, e:

        stderr.write("Error %d: %s\n" % (e.args[0],e.args[1]))
        sys.exit(1)

    finally:
        if con:
            con.close()