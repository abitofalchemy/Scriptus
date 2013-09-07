import sys
import datetime as dt

s1 = sys.argv[1]
s2 = sys.argv[2]

#s1 = '10:33:26'
#s2 = '11:15:49' # for example
FMT = '%H:%M:%S'
start_dt = dt.datetime.strptime(s1, '%H:%M:%S')
end_dt = dt.datetime.strptime(s2, '%H:%M:%S')
diff = (end_dt - start_dt) 
#print diff.seconds/60.
print diff.seconds
