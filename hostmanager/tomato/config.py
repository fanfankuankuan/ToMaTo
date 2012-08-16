# -*- coding: utf-8 -*-
# ToMaTo (Topology management software) 
# Copyright (C) 2010 Dennis Schwerdel, University of Kaiserslautern
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import os

VERSION = 0.1

COORDINATES = []

SITE = ""

AUTH = []

PASSWORD_SALT = "tomato"

TMP_DIR = "/tmp/tomato"
LOG_DIR = "logs"
DATA_DIR = "/var/lib/tomato"

SERVER = [
	{
		"PORT": 8000,
		"SSL": False,
		"SSL_OPTS": {
			"private_key" : "",
			"ca_key": ""
		}
	}
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite'
    }
}

FILESERVER = {
	'port': 8888,
	'path': os.path.join(DATA_DIR, "files"),
}

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'de-de'

INSTALLED_APPS = ('tomato', 'south')

DISABLE_TRANSACTION_MANAGEMENT = True

MAINTENANCE = os.environ.has_key('TOMATO_MAINTENANCE')

ERROR_NOTIFY = []

try:
	import sys
	for path in filter(os.path.exists, ["/etc/tomato/hostmanager.conf", os.path.expanduser("~/.tomato/hostmanager.conf"), "hostmanager.conf"]):
		try:
			execfile(path)
			print >>sys.stderr, "Loaded config from %s" % path
		except Exception, exc:
			print >>sys.stderr, "Failed to load config from %s: %s" % (path, exc)
except:
	import traceback
	traceback.print_exc()

if not isinstance(SERVER, list):
	SERVER = [SERVER]