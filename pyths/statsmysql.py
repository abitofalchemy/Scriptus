import sys 
from   pylab import *
from   numpy import * 
import MySQLdb
import math


db = MySQLdb.connect('192.168.1.112', 'tremcam', 'trem00xB','neurobit')
cursor = db.cursor()

query = sys.argv[1]
cursor.execute(query)
result = cursor.fetchall()

t = []
s = []
u = []
y = []
n = []
#for record in result:
#	if len(record) > 0:
#		t.append(record[0])
#	if len(record) > 0: 
#		s.append(record[1])
#	if ( len(record[1]) > 0 ):
#		print "x: ",record[0]," y: ",record[1] 	

for record in result:
	if  (len(record[0]) > 0 ) and (len(record[1]) > 0 ) and (len(record[2]) > 0 ):
		t.append(record[0])
		s.append(record[1])
        u.append(record[2])

N = int(len(t))

print " int(len(t))",N
