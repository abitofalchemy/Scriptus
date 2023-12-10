MBP GNN 
=======

## Notes on Edge Drive AutoEncoder using PyG

When we have an edgelist and each edge has a set of edge features, how do we build an autoencoder for such a dataset? Below is
an exploration of this question using Pytorch Geometric (pyg).

Here is dataset:

```
srcLabel trgLabel edgVar1, edgVar2, edgLabel
```

### Conditions 

1. No node level features 
2. Labels are all of one kind (no binary labels)

### Objective 

The objective or goal we are after in this exploration is to build a graph autoencoder that trains on edges labeled as `0` and 
we test on a fraction of the dataset to obtain a relatively low reconstruction loss. 




## Setup on MacOS 

source activate torosx this is for a Deloitte project

for exploring baselines with pyg and dgl: pytg

## Working 

1. torosx
2. gnn38 for dgl + pytorch backend
3. pytorgeo: pytorch geometric 

## Misc Notes 

## Dataset Creation 

Real data: Homogeneous graph from CSV files is described in [3]. 

[1]: https://colab.research.google.com/drive/14OvFnAXggxB8vM4e8vSURUp1TaKnovzX?usp=sharing
[2]: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiYoLGe4bfxAhWbQs0KHaNHDIUQFjAFegQICxAD&url=https%3A%2F%2Ftowardsdatascience.com%2Fneo4j-dgl-a-seamless-integration-624ad6edb6c0&usg=AOvVaw3wyyWdHYy_OmLvyqO7-nFX
[3]: https://stellargraph.readthedocs.io/en/stable/demos/basics/loading-pandas.html
