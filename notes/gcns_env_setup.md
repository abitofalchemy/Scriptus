Pytorch Geom for Mol Graph Class
======

# Boltz

sal@boltz gnn $ jupyter-notebook --no-browser --port=8884 --ip=$(hostname -i)
`ssh -N -L 8884:LC02C7A0UMD6R:8884 sal@dsci` which should prompt one for a 
password as a sign that it's working.

Reference `https://docs.bitnami.com/google/faq/get-started/access-ssh-tunnel/` and
`https://docs.ycrc.yale.edu/clusters-at-yale/guides/jupyter/`

## Env & RDKit

https://www.rdkit.org/docs/Install.html
`conda activate gcns37`


## Pytorch

https://pytorch.org/

`conda install pytorch torchvision torchaudio cudatoolkit=11.0 -c pytorch`


## Pytorch Geom

### Datasets


## Proto

MoleculeNet
esol  


From graphneuralnets [1]


Install the ipykernel
- `python -m ipykernel install --user --name gcns37`


[ESOL][2]:  Water solubility data(log solubility in mols per litre) for common organic small molecules.

[Deep Learning on Graphs (a Tutorial)][3] Using [dgl][5] and dgllife.

## Background

Open Graph Benchmark [6] "A collection of benchmark datasets, data-loaders and evaluators for graph machine learning in PyTorch." Here one finds an example to binary classification at the
graph level

[1]: https://colab.research.google.com/drive/16GBgwYR2ECiXVxA1BoLxYshKczNMeEAQ?usp=sharing#scrollTo=BQnbktyWU3r3
[2]: http://moleculenet.ai/datasets-1
[3]: https://cloud4scieng.org/2020/08/28/deep-learning-on-graphs-a-tutorial/
[4]: https://hhaji.github.io/Deep-Learning/Graph-Neural-Networks/
[5]: https://github.com/dmlc/dgl
[6]: https://pypi.org/project/ogb/0.1.0/
[7]: https://github.com/snap-stanford/ogb.git
