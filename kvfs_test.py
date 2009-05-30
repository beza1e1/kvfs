# -!- encoding: utf-8 -!-
from kvfs import KVFS
import stat

def test_basic_root():
	"""testing basic root properties"""
	K = KVFS(dict())
	attr = K.getattr("/")
	assert stat.S_ISDIR(attr['st_mode'])
	dir = list(K.readdir("/"))
	assert len(dir) == 2
	assert '.' in dir
	assert '..' in dir

def test_basic_file():
	"""testing basic file properties"""
	K = KVFS(dict())
	K.create("/blub")
	assert "blub" in K.readdir("/")
	attr = K.getattr("/blub")
	assert stat.S_ISREG(attr['st_mode'])
	K.remove("/blub")
	print list(K.readdir("/"))
	assert not "blub" in K.readdir("/")
	K.flush()

def test_basic_dir():
	"""testing basic directory properties"""
	K = KVFS(dict())
	K.mkdir("/bla")
	assert "bla" in K.readdir("/")
	assert stat.S_ISDIR(K.getattr("/bla")['st_mode'])
	dir = list(K.readdir("/bla"))
	assert '.' in dir
	assert '..' in dir
	K.remove("/bla")
	K.flush("/")

def test_used_root():
	K = KVFS(dict())
	attr = K.getattr("/")
	assert stat.S_ISDIR(attr['st_mode'])
	K.mkdir("/bla")
	K.remove("/bla")
	K.getattr("/")

def test_dir_operations():
	K = KVFS(dict())
	assert stat.S_ISDIR(K.getattr("/")['st_mode'])
	K.mkdir("/bla")
	assert "bla" in K.readdir("/")
	K.create("/bla/blub")
	assert "blub" in K.readdir("/bla")
	assert stat.S_ISREG(K.getattr("/bla/blub")['st_mode'])
	K.remove("/bla")
	assert not "bla" in K.readdir("/")
	assert stat.S_ISDIR(K.getattr("/")['st_mode'])

def test_basic_readwrite():
	msg = "Hello Wörld!"
	K = KVFS(dict())
	K.create("/blub")
	l = K.write("/blub", msg, 0)
	assert len(msg) == l
	msg2 = K.read("/blub", len(msg), 0)
	assert msg == msg2, (msg, msg2)

def test_hardlink():
	K = KVFS(dict())
	K.create("/blub")
	
	

