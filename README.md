logview-gtk
===========

A Python based utility for looking at system logs on Linux. Still in the design
phase. The primary goal right now is for viewing syslog messages. The design 
goals are:

 - Remote access. The program is broken into two parts. The GTK frontend and 
 the log system. The log system is designed to be multithreaded and message
 based so that it wont lock up the GUI, and will make remote access possible.
 - Parsers for different formats of logs. Pull out message date/time, origin of
 message, etc
 - File "roll" detection. Syslog will rotate log files sometimes not in a
 consistent way.

*This is still in a very early stage, more to come.*
 
![Alt text](/../<screenshots>/logview-gtk.png?raw=true "Early screenshot")

