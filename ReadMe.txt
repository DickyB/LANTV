LAN TV from your pal Dicky B (dickyb@dickyb.com)

This is a stripped-down version of what I use.  I've taken out all the
overlays, to simplify understanding of What's Going On for anyone who might
actually look at this unholy den of scripts (not really, you should have
seen the OG Version 1 of this mess).  It doesn't have any of the overlay
options for ffmpeg or anything.  Having to deal with that while you're
figuring out how to get this thing running is something you shouldn't have
to do.  You can add that stuff if you ever get it working.

If this does not have the MySQL database stuff for updating the tables for
your video files, then you got this early, since I'm planning to put a
stripped-down, Just For This version of what I use on my system.  It's not
difficult to do, and anyone with any MySQL experience to speak of can
improve my system easily.  I've only learned enough MySQL to do this, and
pretty much only this.

What This Does:

It is supposed to coordinate streaming videos from ffmpeg to ffserver, so
that it is not only possible to create your own LAN TV Channel(s) with a
daily schedule, but fairly simple.

What You'll Need:

You will need ffmpeg and ffserver, so that means Nope to Windows.  Sort of.
There is nothing in here that can't be altered, if necessary, to run your
channel.  I don't believe there's an ffserver port that will run under
Windows, but there's no requirement to run ffserver on the same machine as
your video feeder.  There's also no requirement to even use ffserver.  You
just need something that will pass along streams to clients that ffmpeg can
send a video feed to.  I happen to use ffmpeg and ffserver, but feel free to
experiment.

You will also need MySQL server running on something.  This can be run on
anything, and again, no requirement to run the MySQL server on the same
machine as the ffmpeg channel feeder, or the ffserver video server.

You will need a lot of video files.  It helps if they're somewhat arranged
on the hard drive.  I have mine arranged into Shows and Movies.  I have
those organized into subdirectories containing each TV Show (for Shows) and
genre, and sub-genres (go as deep as you want) for Movies.

You may need root. I'm writing this version so you shouldn't need root, but
I'm not sure why I thought I needed root when I did a project that this
entire thing is based on.  I wrote that years ago, so I don't know.  If I
get it working without root at all, this paragraph won't be here.

You will need to know how to put something up as a cronjob.

You will need a little bit of knowledge about how MySQL search queries
should be worded (but only a little), and a smattering of Python
familiarity.  Also, how bash works.  If these scare you, don't worry, the
amount of knowledge you'll need is really small, and you might be surprised
at how little is involved.  It's mostly fetching data and setting variables. 
Really easy stuff.  I'm not smart, so you don't have to be, either.

You will need some time.

You need to call your mother, and stay hydrated.

Brief Summary Of What Each File Is Supposed To Do:

director: The heart.  Run every minute.  It checks to see if the channel
feed is running, and if not, determine where in the show we're supposed to
be, and restart the feed from that point.  If the Show is over (or Movie,
but we're using Show to denote the Main Video), show a filler video (more on
that later).  If it's time for another Show, kill all of this channel's
feeds, figure out what Show is next, call the appropriate Show file in the
Shows subdirectory, then play the video.  That's basically director.

cameraman: This is what actually sends the feed to the server.  Any overlays
and such that you would like to add would really go here. After the feed
ends (by end of file or some error), it will run dofiller.

func.py: Some stupid functions to do some things.

dofiller: called by director to run the filler video script and then run director
again. It could just run the filler script, but then after it ran, there
would be dead air until the next cron tick that runs director.  Dead Air Is
Bad.  Let's avoid that.

fillshow: This is called by dofiller.  It picks a video of filler (something
like sketch comedy, or videos of your own making, but anything that doesn't
need to be viewed in its entirety to enjoy) and plays it.  This will need to
be edited, as it's different from regular shows as it does not need a Show
file in the Shows directory, but *does* use index files.

queueshow: This is called by the show files in Shows (more later) to fetch the 
episode index, increment it, reset to 0 if it's larger than the number of episodes, 
get the video file full path, write info to a few files for director to read so 
it can play the video (with cameraman). Yeah, it sounds complicated, but it's 
really not that bad.

killchannel: This is to kill the channel when you want the channel killed.
If you want it to stay dead, make sure you comment out your crontab entry
for director.

ReadMe.txt: Probably would be this.

In the subdirectory Shows, you should have a small script that calls
queueshow with appropriate arguments.  There should be an example of this
script in Shows.

In the subdirectory 1, there are two files, schedule and channel.conf.  You
may be able to guess what those are for, and I'll go ahead and assume you
do.  There is also a subdirectory named index, which is used to keep track
of which episode of a Show you're supposed to be on.  It's more versatile
than that, since you can use it for anything, really, like which # movie of
the Sci-Fi genre you watched last, etc.

I will say that schedule can be used as Day Of Week scheduling.  Monday is
Day-Of-Week 0, so schedule.0 would be used instead of the default schedule
on Mondays, etc.  The format of schedule is:

12:0:30:magnet:The Magnet Show!

12 being 12pm (24hour)
0 being at 0 minutes past 12pm
30 being how long the time slot is
magnet being the index file (no extension)
The Magnet Show! being the show's Friendly Name

Not really rocket science, but I may as well spell that out.

LIBFREETYPE
When it comes to putting a movie into the schedule. Not just movies, but any
video where the title is actually nicely formatted with episode/movie name,
like this:

Boo's Awful Day.mp4

or

Awesome Show - The Big Fish.avi

Here's some voodoo for you.  For shows or for movies named like this, you
can also do this to your schedule:

12:0:30:awesomeshow:*

The * denotes to use queueshowtitle to rip the title out of the database. If
the index file doesn't exist yet, it will be off.  Just will.  The line in
the schedule would show in the output from showschedule as:

12:00pm  Awesome Show - The Big Fish

instead of the normal

12:00pm  Awesome Show #42

Anything after the * will prepend the name like this:

12:0:30:awesomeshow:*WOO

12:00pm  WOO: Awesome Show - The Big Fish

Note: This writes to channel path/dyntext2.txt by default.  If you haven't
enabled libfreetype in your ffmpeg build, all this is useless information
from LIBFREETYPE to here. It may come in handy later.  Never know.

This may seem like a lot of crap, but you didn't read the whole thing
anyway. I know I wouldn't have.  Just look at the scripts, you can figure it out,
I have the utmost confidence in you.  Just jump in the pool without testing
the water, that's how I wrote all of this anyway.  Have fun.

