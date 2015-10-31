# Python Bing Wallpaper Read Write Lock Module

import threading 

class RWLock:
	
	def __init__(self):
		self._reading_threads = dict()
		self._write_accesses = 0
		self._write_requests = 0
		self._write_thread = None
		self._condition = threading.Condition()
	
	def acquire_read(self):
		self._condition.acquire(blocking=True)
		_calling_thread = threading.current_thread()
		while(not self._can_grant_read_access(_calling_thread)):
			_condition.wait()
		
		self._reading_threads[_calling_thread] = self._get_read_access_count(_calling_thread) + 1
		self._condition.release()
	
	def _can_grant_read_access(self, _calling_thread):
		if(self._is_writer(_calling_thread)): return True
		if(self._has_writer()): return False
		if(self._is_reader(_calling_thread)): return True
		if(self._has_write_requests()): return False
		
		return True
		
	def release_read(self):
		self._condition.acquire(blocking=True)
		_calling_thread = threading.current_thread()
		if(not self._is_reader(_calling_thread)):
			raise Exception('Calling Thread does not hold the read lock on this ReadWriteLock')
		
		_access_count = self._get_read_access_count(_calling_thread)
		if(_access_count == 1):
			del self._reading_threads[_calling_thread]
		else:
			self._reading_threads[_calling_thread] = _access_count - 1
		
		self._condition.notify_all()
		self._condition.release()
		
	def acquire_write(self):
		self._condition.acquire(blocking=True)
		self._write_requests = self._write_requests + 1
		_calling_thread = threading.current_thread()
		while(not self._can_grant_write_access(_calling_thread)):
			self._condition.wait()
			
		self._write_requests = self._write_requests - 1
		self._write_accesses = self._write_accesses + 1
		self._write_thread = _calling_thread 
		self._condition.release()
		
	def release_write(self):
		self._condition.acquire(blocking=True)
		if(not self._is_writer(threading.current_thread())):
			raise Exception('Calling Thread does not hold the write lock on this ReadWriteLock')
		
		self._write_accesses = self._write_accesses - 1
		if(self._write_accesses == 0):
			self._write_thread = None
		
		self._condition.notify_all()
		self._condition.release()
		
	def _can_grant_write_access(self, _calling_thread):
		if(self._is_only_reader(_calling_thread)): return True
		if(self._has_reader()): return False
		if(self._write_thread == None): return True
		if(not self._is_writer(_calling_thread)): return False
		
		return True
		
	def _get_read_access_count(self, _calling_thread):
		if (_calling_thread in self._reading_threads):
			return self._reading_threads[_calling_thread]
		else:
			return 0
			
	def _has_reader(self):
		return len(self._reading_threads)
	
	def _is_reader(self, _calling_thread):
		return _calling_thread in self._reading_threads
	
	def _is_only_reader(self, _calling_thread):
		return self._get_read_access_count(_calling_thread) == 1 & self._is_reader(_calling_thread)
		
	def _has_writer(self):
		return self._write_thread != None
	
	def _is_writer(self, _calling_thread):
		return id(self._write_thread) == id(_calling_thread)
		
	def _has_write_requests(self):
		return self._write_requests > 0