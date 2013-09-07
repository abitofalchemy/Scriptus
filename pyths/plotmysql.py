import sys 
from   pylab import *
from   numpy import * 
import MySQLdb
import math

print len(sys.argv)

#if (len(sys.argv) < 1):
#    print "Usage: python plotmysql.py hostname `"sql query`""
#else:
#    db = MySQLdb.connect(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4])
#    cursor = db.cursor()
#
#    query = sys.argv[5]
#    cursor.execute(query)
#    result = cursor.fetchall()
#
#    t = []
#    s = []
#    u = []
#    y = []
#    n = []
#    #for record in result:
#    #	if len(record) > 0:
#    #		t.append(record[0])
#    #	if len(record) > 0: 
#    #		s.append(record[1])
#    #	if ( len(record[1]) > 0 ):
#    #		print "x: ",record[0]," y: ",record[1] 	
#
#    for record in result:
#        if  (len(record[0]) > 0 ) and (len(record[1]) > 0 ) and (len(record[2]) > 0 ):
#            t.append(record[0])
#            s.append(record[1])
#            u.append(record[2])
#
#    N = int(len(t))
#
#    ##
    fig = plt.figure()
    ax1 = fig.add_subplot(311)

    ax1.grid(True)
    suptitle(query)
    ax1.set_title('X axis')
    ax1.axhline(0, color='black', lw=2)
#    ax2 = fig.add_subplot(312, sharex=ax1)
#    ax2.grid(True)
#    ax2.set_title('Y axis')
#    ax2.axhline(0, color='black', lw=2)
#    ax3 = fig.add_subplot(313, sharex=ax1)
#    ax3.grid(True)
#    ax3.set_title('Z axis')
#    ax3.axhline(0, color='black', lw=2)
#    for i in range(0,N):
#        y  = [float(fv) for fv in t[i].split(",")] 
#        n = range(0,len(y))
#        ax1.plot(n, y, 'ko')
#        y  = [float(fv) for fv in s[i].split(",")] 
#        n = range(0,len(y))
#        ax2.plot(n, y, 'ko')
#        y  = [float(fv) for fv in u[i].split(",")] 
#        n = range(0,len(y))
#        ax3.plot(n, y, 'ko')
#
#
#
#
#    #axis([min(x), max(x), min(y), max(y)])
#
#
#    #
#    F = gcf()
#    DPI = F.get_dpi()
#    F.savefig('figplot.png',dpi = (150))
#    #show()
