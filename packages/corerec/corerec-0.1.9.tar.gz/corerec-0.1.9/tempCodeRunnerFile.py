import engine.corerec as cr
# import vish_graphs as vg
import pandas as pd
import numpy as np
import torch
df = np.loadtxt("/Users/visheshyadav/Documents/Github/COrerec/src/SANDBOX/swad.csv", delimiter=",")
k = 23
# test1 (no data loader, homo batches)
# new_file = vg.generate_random_graph(100,seed='k')
g_d = torch.GraphDataset(df)
d_l= torch.Dataloader(df,batch_size=5,shuffle=False)
