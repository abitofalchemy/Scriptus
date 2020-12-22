from dgl.data import Coauthor
x = Coauthor('cs')
coau=x[0]
coau

coaux = coau.to_networkx()
coaux.edges(0)

f = coau.ndata['feat'][0]*coau.ndata['feat'][5111]*coau.ndata['feat'][12716]*coau.ndata['feat'][12963]
for i in range(len(f)):
  if f[i]!=0:
    print(
