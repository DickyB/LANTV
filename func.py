#!/usr/bin/python
#
# func.py: Dicky B (dickyb@dickyb.com)
#
# a couple of stupid functions to save some cut/paste later,
# and also make it easier to fix when I break it.
#
#
#
import datetime
import os

tmppath="/run/shm/"


def getDayOfWeek():
  nowd=datetime.datetime.now()
  dow=nowd.weekday() #0=Monday
  return dow

def getCurrentHour():
  CurrentTime=datetime.datetime.now()
  return int(datetime.datetime.strftime(CurrentTime,'%H'))

def getCurrentMinute():
  CurrentTime=datetime.datetime.now()
  return int(datetime.datetime.strftime(CurrentTime,'%M'))

def getCurrentSecond():
  CurrentTime=datetime.datetime.now()
  return int(datetime.datetime.strftime(CurrentTime,'%S'))

def getTODMin():
  CurrentTime=datetime.datetime.now()
  ht=int(datetime.datetime.strftime(CurrentTime,'%H'))
  mt=int(datetime.datetime.strftime(CurrentTime,'%M'))
  return (ht*60)+mt

def isRunning(procname):
  found=False
  os.system("/bin/ps -A | /bin/grep "+procname+" > "+tmppath+"mondo."+procname)
  siz = os.path.getsize(tmppath+"mondo."+procname)
  if siz < 10:
    found=False
  else:
    found=True  
  os.remove(tmppath+"mondo."+procname)  
  return found
    
    
