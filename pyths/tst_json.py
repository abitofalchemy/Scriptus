import json
import ast
from pprint import pprint 

json_string = '{"first_name": "Guido", "last_name":"Rossum"}'
data = json.loads(json_string)

#with open('data.json', 'w') as fp:
#    json.dump(data, fp)
infile = "outfile.babai.json"
infile = "paper00.json"
data = []
with open(infile, 'r') as fp:
	i =0
	for l in fp.readlines():
		objs = l.replace('}{','}}\t{{').split('}\t{')
		tw_lst = [json.loads(obj) for obj in objs]
		print len(tw_lst)

print type(tw_lst[0])
print tw_lst[0].keys()

#  		#print [x for x in l]
# 		# data.append(l)
# #   lines = fp.readlines()
# 	#print type(data)	
# 	#data = json.loads([x for x in fp.readlines()])

# print len(l)

# # print type(data)
# exit()
# for el in data:
#   print el['id'], el['user']['id'], el['text']
# #   break
  
