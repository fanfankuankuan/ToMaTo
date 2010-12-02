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

import uuid, os, traceback

import config, util, fault, atexit, time, log

from cStringIO import StringIO

class TaskStatus():
	tasks={}
	ACTIVE = "active"
	DONE = "done"
	FAILED = "failed"
	def __init__(self, func, *args, **kwargs):
		self.id = str(uuid.uuid1())
		TaskStatus.tasks[self.id]=self
		self.func = func
		self.args = args
		self.kwargs = kwargs
		self.output = StringIO()
		self.subtasks_total = 0
		self.subtasks_done = 0
		self.status = TaskStatus.ACTIVE 
		self.started = time.time()
	def done(self):
		self.status = TaskStatus.DONE
	def failed(self):
		self.status = TaskStatus.FAILED
	def is_active(self):
		return self.status == TaskStatus.ACTIVE
	def dict(self):
		return {"id": self.id, "output": self.output.getvalue(), 
			"subtasks_done": self.subtasks_done, "subtasks_total": self.subtasks_total,
			"status": self.status, "active": self.status == TaskStatus.ACTIVE, 
			"failed": self.status == TaskStatus.FAILED, "done": self.status==TaskStatus.DONE,
			"started": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.started))}
	def _run(self):
		try:
			self.func(*self.args, task=self, **self.kwargs)
			self.done()
		except Exception, exc:
			if config.TESTING:
				traceback.print_exc()
			fault.errors_add('%s:%s' % (exc.__class__.__name__, exc), traceback.format_exc())
			self.output.write('%s:%s' % (exc.__class__.__name__, exc))
			self.failed()
	def start(self):
		util.start_thread(self._run)
	def check_delete(self):
		if (time.time() - self.started > 3600*24*3) or (time.time() - self.started > 3600 and self.status == TaskStatus.DONE):
			if not os.path.exists(config.log_dir + "/tasks"):
				os.makedirs(config.log_dir + "/tasks")
			logger = log.get_logger(config.log_dir + "/tasks/%s"%self.id)
			logger.lograw(self.output.getvalue())
			logger.close()
			del TaskStatus.tasks[self.id]

class UploadTask():
	tasks={}
	def __init__(self):
		self.id = str(uuid.uuid1())
		UploadTask.tasks[self.id]=self
		self.filename = config.local_control_dir+"/tmp/"+self.id
		if not os.path.exists(config.local_control_dir+"/tmp/"):
			os.makedirs(config.local_control_dir+"/tmp/")
		self.fd = open(self.filename, "w")
		self.started = time.time()
	def chunk(self, data):
		self.fd.write(data)
	def finished(self):
		self.fd.close()
		del UploadTask.tasks[self.id]
	def check_delete(self):
		if time.time() - self.started > 3600:
			del UploadTask.tasks[self.id]
			if os.path.exists(self.filename):
				os.remove(self.filename)
		
class DownloadTask():
	tasks={}
	def __init__(self, filename):
		self.filename = filename
		self.id = str(uuid.uuid1())
		DownloadTask.tasks[self.id]=self
		self.fd = open(self.filename, "rb")
		self.started = time.time()
	def chunk(self):
		size=1024*1024
		data = self.fd.read(size)
		if len(data) == 0:
			self.fd.close()
			del DownloadTask.tasks[self.id]
			os.remove(self.filename)
		return data
	def check_delete(self):
		if time.time() - self.started > 3600:
			del DownloadTask.tasks[self.id]
			if os.path.exists(self.filename):
				os.remove(self.filename)
	
def cleanup():
	for task in TaskStatus.tasks.values():
		task.check_delete()
	for task in DownloadTask.tasks.values():
		task.check_delete()
	for task in UploadTask.tasks.values():
		task.check_delete()
	
if not config.TESTING:	
	cleanup_task = util.RepeatedTimer(3, cleanup)
	cleanup_task.start()
	atexit.register(cleanup_task.stop)