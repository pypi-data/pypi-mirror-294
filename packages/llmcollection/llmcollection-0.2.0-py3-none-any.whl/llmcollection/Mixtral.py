import math
import torch
import torch.nn as nn
import torchtune
from torch.nn import functional as F

class FeedForward(nn.Module):
    '''
        Initializes the FeedForward layer

        Args:

        d_model :int -> Embedding size of the model
        dropout :float -> Dropout value

        Input:

        Tensor of shape (*)

        Output:

        Tensor of shape (*)
    '''

    def __init__(self,d_model,dropout):
        super().__init__()
        self.d_model = d_model
        self.dropout = dropout

        self.ffn = nn.Sequential(
            nn.Linear(in_features=self.d_model, out_features=self.d_model * 4),
            nn.SiLU(),
            nn.Linear(in_features=self.d_model * 4, out_features=self.d_model),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        return self.ffn(x)
    
class MOEFeedForward(nn.Module):
    '''
        Initializes Mixture of Experts FFN Layer

        Args:

        d_model :int -> Embedding size of the model
        num_experts :int -> Number of experts in MOE FFN
        dropout :float -> Dropout value
        top_k -> Number of experts to be considered(Default 2)

        Input:

        Tensor of the shape [Batch size,Sequence Length,Embedding dimension]

        Output:

        Tensor of the shape [Batch size,Sequence Length,Embedding dimension]        

    '''
    def __init__(self,d_model,num_experts,dropout,top_k=2):
        super().__init__()
        self.d_model = d_model
        self.num_experts = num_experts
        self.dropout = dropout
        self.top_k = top_k

        self.experts = nn.ModuleList([FeedForward(self.d_model,self.dropout) for _ in range(self.num_experts)])
        self.router = nn.Linear(self.d_model, self.num_experts)

    def forward(self,x):
        logits = self.router(x)
        top_k_logits, indices = logits.topk(self.top_k, dim=-1)
        zeros = torch.full_like(logits, float('-inf'))
        sparse_logits = zeros.scatter(-1, indices, top_k_logits)

        gating_output = F.softmax(sparse_logits, dim=-1)
        final_output = torch.zeros_like(x)

        flat_x = x.reshape(-1, x.size(-1))
        gating_output_flat = gating_output.reshape(-1, gating_output.size(-1))

        # Process each expert in parallel
        for i, expert in enumerate(self.experts):
            # Create a mask for the inputs where the current expert is in top-k
            expert_mask = (indices == i).any(dim=-1)
            flat_mask = expert_mask.view(-1)

            if flat_mask.any():
                expert_input = flat_x[flat_mask]
                expert_output = expert(expert_input)

                # Extract and apply gating scores
                gating_scores = gating_output_flat[flat_mask, i].unsqueeze(1)
                weighted_output = expert_output * gating_scores

                # Update final output additively by indexing and adding
                final_output[expert_mask] += weighted_output.squeeze(1)

        return final_output


class MixtralBlock(nn.Module):
    '''
        Initializes the transformer block of the model

        Args:

        d_model :int -> Embedding size of the model
        context_length :int -> Context length of the model
        num_heads :int -> Number of heads in Multihead attention
        num_experts :int -> Number of experts in MOE FFN
        dropout :float -> Dropout value

        Input:

        Tensor of the shape [Batch size,Sequence Length,Embedding dimension]

        Components:

        embedding: Adds rotary positional embeddings to query and key
        multi_head_attention_layer: Performs scaled_dot_product_attention() for num_heads in parallel
        att_mask: Adds a causal attention mask
        feed_forward_layer: Performs operations of the feed forward layer
        rms_norm: Applies RMSNorm

        Output:

        Tensor of the shape [Batch size,Sequence Length,Embedding dimension]
    '''
    def __init__(self,d_model,context_length,num_heads,num_experts,dropout):
        super().__init__()
        self.device='cuda' if torch.cuda.is_available() else 'cpu'
        self.d_model = d_model
        self.context_length = context_length
        self.head_size = d_model // num_heads
        self.num_heads = num_heads
        self.num_experts = num_experts
        self.dropout = dropout

        self.embedding=torchtune.modules.RotaryPositionalEmbeddings(dim=self.head_size,max_seq_len=self.context_length)
        self.multi_head_attention_layer = nn.MultiheadAttention(d_model, num_heads,batch_first=True)
        self.att_mask=torch.ones((self.context_length,self.context_length),dtype=torch.bool).to(self.device)
        self.feed_forward_layer = MOEFeedForward(self.d_model,self.num_experts,self.dropout)
        self.rms_norm =torchtune.modules.RMSNorm(self.d_model)

    def forward(self, x):
        B,T,D=x.shape
        attn_mask1=torch.triu(self.att_mask[:T,:T],diagonal=1)
        attn_mask2=torch.tril(self.att_mask[:T,:T],diagonal=-T//2)
        attn_mask=torch.logical_or(attn_mask1,attn_mask2)
        x=self.rms_norm(x)
        q=k=x.view((B,T,self.num_heads,self.head_size))
        q=self.embedding(q)
        k=self.embedding(k)
        q=q.view((B,T,D))
        k=k.view((B,T,D))
        x = self.multi_head_attention_layer(q,k,x,attn_mask=attn_mask,need_weights=False,is_causal=True)[0]
        x = x + self.feed_forward_layer(self.rms_norm(x))  
        return x
    
class Mixtral(nn.Module):
    '''
        Instantiates the Mixtral model

        Input Arguments:

        d_model :int -> Embedding size of the model
        context_length :int -> Context length of the model
        num_heads :int -> Number of heads in Multihead attention
        num_blocks :int -> Number of transformer blocks
        num_experts :int -> Number of experts in MOE FFN
        embedding_table :nn.Embedding -> Embedding table
        dropout :float -> Dropout value (default value 0.0)
        
        Output:

        Tensor of the shape [Batch size,Context length,Number of embeddings]
        
        '''
    
    def __init__(self,d_model: int,context_length: int,num_heads: int,num_blocks: int,num_experts: int,embedding_table,dropout=0.0):
        super().__init__()
        
        assert isinstance(embedding_table,nn.Embedding)
        assert embedding_table.weight.shape[1]==d_model

        self.device='cuda' if torch.cuda.is_available() else 'cpu'
        self.d_model = d_model
        self.context_length = context_length
        self.num_heads = num_heads
        self.num_blocks = num_blocks
        self.num_experts = num_experts
        self.dropout = dropout
        self.token_embedding_lookup_table=embedding_table
        self.max_token_value=self.token_embedding_lookup_table.weight.shape[0]-1

        self.transformer_blocks = nn.Sequential(*(
                [MixtralBlock(self.d_model,self.context_length,self.num_heads,self.num_experts,self.dropout) for _ in range(self.num_blocks)] +
                [torchtune.modules.RMSNorm(self.d_model)] #Added RMSNorm for stability
        ))
        self.language_model_out_linear_layer = nn.Linear(in_features=self.d_model, out_features=self.max_token_value)

    def forward(self, idx, targets=None):
        '''
            Applies positional encoding and forwards the weights.
        '''
        B, T = idx.shape

        x = self.token_embedding_lookup_table(idx)
        x = self.transformer_blocks(x)
        logits = self.language_model_out_linear_layer(x)

        if targets is not None:
            B, T, C = logits.shape
            logits_reshaped = logits.view(B * T, C)
            targets_reshaped = targets.view(B * T)
            loss = F.cross_entropy(input=logits_reshaped, target=targets_reshaped)
        else:
            loss = None
        return logits, loss

    def generate(self, idx, max_new_tokens :int):
        '''
            Generates the output for range(max_new_tokens)

            Args:
            max_new_token :int -> Number of tokens to be generated

            Returns -> Tensor of token values
        '''
        # idx is (B,T) array of indices in the current context
        for _ in range(max_new_tokens):
            # Crop idx to the max size of our positional embeddings table
            idx_crop = idx[:, -self.context_length:]
            # Get predictions
            logits, loss = self(idx_crop)
            # Get the last time step from logits where the dimensions of the logits are (B,T,C)
            logits_last_timestep = logits[:, -1, :]
            # Apply softmax to get probabilities
            probs = F.softmax(input=logits_last_timestep, dim=-1)
            # Sample from the probabilities' distribution.
            idx_next = torch.multinomial(input=probs, num_samples=1)
            # Append the sampled indexes idx_next to idx
            idx = torch.cat((idx, idx_next), dim=1)
        return idx
