import torch
import random

def generate_data(p):
    A=torch.arange(p)
    B=torch.arange(p)
    X=torch.cartesian_prod(A,B)
    c=torch.full((p*p, 1), p)
    X=torch.cat((X,c), dim=1)
    Y=(X[:,0]+X[:,1])%p
    return X,Y

def train_test_split(X,Y, train_ratio, seed):
    N=X.shape[0]
    g=torch.Generator().manual_seed(seed)
    perm=torch.randperm(N,generator=g)
    X=X[perm]
    Y=Y[perm]
    ratio=int(N*train_ratio)
    X_train=X[:ratio]
    Y_train=Y[:ratio]
    X_test=X[ratio:]
    Y_test=Y[ratio:]
    return X_train,Y_train,X_test,Y_test


if __name__=="__main__":
    p=87
    X,Y=generate_data(p)
    X_train,Y_train,X_test,Y_test=train_test_split(X,Y, train_ratio=0.3, seed=42)
    assert len(X_train) == int(87*87*0.3)
    X_train_encoded=X_train[:,0]*p+X_train[:,1]
    X_test_encoded=X_test[:,0]*p+X_test[:,1]
    assert set(X_train_encoded.tolist()).isdisjoint(set(X_test_encoded.tolist()))
    i=random.randint(0,len(X_train)-1)
    assert (X_train[i,0]+X_train[i,1])%p==Y_train[i]
    A,B,C,D=train_test_split(X,Y, train_ratio=0.3, seed=42)
    K,L,M,N=train_test_split(X,Y, train_ratio=0.3, seed=42)
    assert torch.equal(A,K) and torch.equal(B,L) and torch.equal(C,M) and torch.equal(D,N)
    print("All tests passed!")


