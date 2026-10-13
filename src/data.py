import torch
def generate_data(p):
    A=torch.arange(p)
    B=torch.arange(p)
    X=torch.cartesian_prod(A,B)
    c=torch.full((p*p, 1), p)
    X=torch.cat((X,c), dim=1)
    Y=(X[:,0]+X[:,1])%p
    return X,Y



