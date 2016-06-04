#!/usr/bin/python
#
# This requires understanding of what does what, and some editing to 
# reflect your system, notably file paths, etc.
#
#
#
#

import os
import random
import sys
import time
import pexpect
import MySQLdb

#get where this file is.
basepath=os.path.dirname(os.path.realpath(__file__))+'/'



print "\ngetlist.py by Dicky B (C)2012-2016\n"

#you'll need to edit this here.
mysqlhost='127.0.0.1'
mysqluser='username'
mysqlpass='password'
mysqldatabase='databasename'
mysqltable='tablename'
VidDir = '/path/to/your/videos/'
#TNDir = '/path/to/thumbs/'
#AniDir = '/path/to/thumbs/ani/'
TXTDir= basepath+'/info/'
WWWDir= basepath

ssize= "320x200"  #widescreen 16:10 aspect for shots.
#this should be it, unless you want thumbnails, which
#adds a lot to the runtime if there's a lot of videos
#without them.


startt=time.time()

os.chdir(basepath)

os.system('find '+VidDir+'|sort -n > cow.txt')
file = open('cow.txt','r')
numvids=0
master = open('./master.temp','w')
db = MySQLdb.connect(mysqlhost,mysqluser,mysqlpass,mysqldatabase)
cursor = db.cursor()
def ffgo(cmd):
  thread = pexpect.spawn(cmd)
  cpl=thread.compile_pattern_list([pexpect.EOF,"time= *\d+",'(.+)'])
  while True:
    i=thread.expect_list(cpl,timeout=None)
    if i==0:
      break
    elif i==1:
      timecode = thread.match.group(0)
      thread.close
    elif i==2:
      pass
  return;
print "Add New Videos run engaged."

for line in file.xreadlines():
  a=line.replace('\r','')
  b=a.replace('\n','')
  ci = b.lower()[-4:]
  PRINTIT=0
  if ci=='.avi':
    PRINTIT=1
  if ci=='.flv':
    PRINTIT=1
  if ci=='.mp4':
    PRINTIT=1
  if ci=='.mpg':
    PRINTIT=1
  if ci=='.mov':
    PRINTIT=1
  if ci=='.mkv':
    PRINTIT=1
  if ci=='.wmv':
    PRINTIT=1
  if ci=='.m4v':
    PRINTIT=1
  if PRINTIT:
    numvids = numvids + 1  
    # b contains full movie path, need to just get filename
    fn = os.path.basename(b)
    sys.stdout.write('\r                                                                          \r')
    qfn=fn[:70]    
    seconds = str(random.randint(35,80))
    if "/Movies/" in b:
      seconds = str(random.randint(125,180))
    sys.stdout.write(qfn)
    sys.stdout.flush()
    min = str(random.randint(10,15))
    bbb=db.escape_string(b)
    bbb=bbb.strip()
    qline="SELECT fullpath FROM "+mysqltable+" WHERE fullpath='"+bbb+"'"
    qq=0
    
    
    if cursor.execute(qline):
      data=cursor.fetchone()
      qq=1
    else:
      qq=0
#      
#    commented lines below to disable thumbnail generation.
#
#    q = os.path.isfile(TNDir+fn+".jpg")
#    MONGO=False
#    if q:
#      statinfo = os.stat(TNDir+fn+".jpg")
#      if statinfo.st_size < 1:
#        q = False
#        MONGO=True
    leng='EMPTY'
    if qq <> 1:
      cmd='echo "'+b+'\r" > "'+TXTDir+fn+'.txt"'
      os.system(cmd)
      cmd='/usr/local/bin/ffmpeg -i "'+b+'" 2>&1 | grep "Duration" | cut -d \' \' -f 4 | sed s/,// >> "'+TXTDir+fn+'.txt"'
      os.system(cmd)
      tf = open (TXTDir+fn+'.txt')
      for line in tf.readlines():
        if not line == '':
          leng=line.rstrip('\n')
      tf.close()
      os.system(cmd)
    if leng == 'EMPTY':
      qline="SELECT length FROM "+mysqltable+" WHERE fullpath='"+bbb+"'"
      cursor.execute(qline)
      data=cursor.fetchone()
      leng = data[0]
#    if not q:
#      cmd = '/usr/local/bin/ffmpeg -y -v 0 -ss '+seconds+' -i "'+b+'" -vcodec mjpeg -vframes 1 -an -f rawvideo -s '+ssize+' "'+TNDir+fn+'.jpg"'
      
      #if we tried once, and got a 0 byte thumbnail, fuckit, we tried.  Have a default NO IMAGE jpeg, and put the info on that shit.
#      if MONGO:
#        cmd = 'cp '+TNDir+'/default/noimage.jpg "'+TNDir+fn+'.jpg"'
#      
#      
#      
#      os.system(cmd)
#      dfn=fn.translate(None,"'")
#      cmd="/usr/bin/convert \""+TNDir+fn+".jpg\" -fill black pointsize 12 -draw \"text 3,13'"+dfn+"'\" \""+TNDir+fn+".jpg\""
#      ffgo(cmd)
#      cmd="/usr/bin/convert \""+TNDir+fn+".jpg\" -fill white pointsize 12 -draw \"text 2,12'"+dfn+"'\" \""+TNDir+fn+".jpg\""
#      ffgo(cmd)
#      cmd="/usr/bin/convert \""+TNDir+fn+".jpg\" -fill black pointsize 12 -draw \"text 3,33'"+leng+"'\" \""+TNDir+fn+".jpg\""
#      ffgo(cmd)
#      cmd="/usr/bin/convert \""+TNDir+fn+".jpg\" -fill white pointsize 12 -draw \"text 2,32'"+leng+"'\" \""+TNDir+fn+".jpg\""
#      ffgo(cmd)
#
    master.write(b+'\r\n')
    master.write(fn+'\r\n')
    master.write(str(leng)+'\r\n')
db.close()
master.close()
cmd='echo "Just a timestamp, but do not remove."  > '+WWWDir+'master.list';
os.system(cmd)
sys.stdout.write('\r                                                                          \r')
sys.stdout.write('Add New Videos run completer.\n')
print "\nPruning database. (This may take a while)"
cmd="cp master.temp master.list"
os.system(cmd)


#this is what actually enters all this into mysql database
# it needs to be edited
#
cmd='/usr/bin/php '+basepath+'updatedb.php > /dev/null';
os.system(cmd)

#"completer" is not a typo, it's an old in-joke between me and a guy I haven't
#even talked to in years.  It's from a CDROM cleaning kit.  Inside, there
#was a CD with a brush on it (yeah, a brush right on it).  Anyway, you played
#the CD as audio, and you got some prompts from a female voice that was 
#obviously japanese, and didn't quite speak english perfectly.  No fault on her,
#since she knows another language, and I don't.  But, when it was done, she'd
#say something like "CD Cleaning is Completer".  And "Completer" stuck as what
#we'd say anything was done doing what it was doing. It was probably "complete-oo", 
#but it sounded like "completer" to us.  Nevermind, correct it if you want, and 
#throw out decades of tradition.  Be that way.
print "Pruning completer.\n"
endt=time.time()
rtim=str(endt-startt)
print numvids," videos indexed in",rtim,"seconds."
cmd="cp master.temp master.list"
os.system(cmd)
