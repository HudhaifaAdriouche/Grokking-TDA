import torch
import torch.nn as nn

#constants: 

p=113
vocab_size=p+1
d_model=128
n_heads=4
batch = int(0.3*p*p)


class Transformer(nn.Module):
    def __init__(self, vocab_size, d_model, n_heads):
        super(Transformer, self).__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.posembedding = nn.Embedding(3, d_model)
        self.Q = nn.Linear(d_model,d_model)
        self.K = nn.Linear(d_model, d_model)
        self.V= nn.Linear(d_model, d_model)
        self.n_heads = n_heads
        self.d_model = d_model
        self.out = nn.Linear(d_model, d_model)

    def forward(self, tokens): # tokens : (batch , 3)
        W_E=self.embedding(tokens)
        W_P=self.posembedding(torch.arange(3).to(tokens.device))
        W=W_E+W_P
         





if __name__ == "__main__":
    batch_size = 5
    tokens = torch.randint(0, vocab_size, (batch_size, 3))
    
    model = Transformer(vocab_size, d_model, n_heads)
    output = model(tokens)
    
    assert output.shape == (batch_size, 3, d_model), f"Expected {(batch_size, 3, d_model)}, got {output.shape}"
    print(f"✓ Output shape: {output.shape}")
    
    # Add intermediate shape prints inside forward() to debug
