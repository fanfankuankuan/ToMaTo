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

import os, sys, signal, time, thread

# tell django to read config from module tomato.config
os.environ['DJANGO_SETTINGS_MODULE']=__name__+".config"

#TODO: debian package
#TODO: tinc clustering
#TODO: external network management
#TODO: interface auto-config
#TODO: topology timeout
#TODO: link measurement

def db_migrate():
	"""
	NOT CALLABLE VIA XML-RPC
	Migrates the database forward to the current structure using migrations
	from the package tomato.migrations.
	"""
	from django.core.management import call_command
	call_command('syncdb', verbosity=0)
	from south.management.commands import migrate
	cmd = migrate.Command()
	cmd.handle(app="tomato", verbosity=1)


import config

	
import threading
_currentUser = threading.local()

def currentUser():
	return _currentUser.user if hasattr(_currentUser, "user") else None
	
def setCurrentUser(user):
	_currentUser.user = user

def login(credentials, sslCert):
	user = auth.login(*credentials) if credentials else None
	setCurrentUser(user)
	return user or not credentials

from lib import tasks #@UnresolvedImport
scheduler = tasks.TaskScheduler(maxLateTime=30.0, minWorkers=5, maxWorkers=10)

starttime = time.time()

from models import *
	
import api

from . import lib, resources, host, accounting, auth, rpcserver #@UnresolvedImport
from lib.cmd import bittorrent, process #@UnresolvedImport
from lib import logging, util #@UnresolvedImport

scheduler.scheduleRepeated(config.BITTORRENT_RESTART, util.wrap_task(bittorrent.restartClient))

stopped = threading.Event()

def start():
	logging.openDefault(config.LOG_FILE)
	db_migrate()
	auth.init()
	resources.init()
	global starttime
	bittorrent.startTracker(config.TRACKER_PORT, config.TEMPLATE_PATH)
	bittorrent.startClient(config.TEMPLATE_PATH)
	rpcserver.start()
	starttime = time.time()
	scheduler.start()
	
def reload_(*args):
	print >>sys.stderr, "Reloading..."
	logging.closeDefault()
	reload(config)
	logging.openDefault(config.LOG_FILE)
	#stopRPCserver()
	#startRPCserver()

def _stopHelper():
	stopped.wait(10)
	if stopped.isSet():
		return
	print >>sys.stderr, "Stopping takes long, waiting some more time..."
	stopped.wait(10)
	if stopped.isSet():
		return
	print >>sys.stderr, "Ok last change, killing process in 10 seconds..."
	stopped.wait(10)
	if stopped.isSet():
		return
	print >>sys.stderr, "Killing process..."
	process.kill(os.getpid(), force=True)

def stop(*args):
	print >>sys.stderr, "Shutting down..."
	thread.start_new_thread(_stopHelper, ())
	rpcserver.stop()
	scheduler.stop()
	bittorrent.stopTracker()
	bittorrent.stopClient()
	logging.closeDefault()
	stopped.set()

def run():
	start()
	signal.signal(signal.SIGTERM, stop)
	signal.signal(signal.SIGINT, stop)
	signal.signal(signal.SIGHUP, reload_)
	try:
		while not stopped.isSet():
			stopped.wait(1.0)
	except KeyboardInterrupt:
		stop()