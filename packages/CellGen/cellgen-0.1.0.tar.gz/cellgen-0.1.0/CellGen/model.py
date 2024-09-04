import os
import sys
import time
import gzip
import gc
import math
import random
from collections import Counter
from copy import deepcopy
from functools import partial
from typing import List
from random import sample
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import colorcet as cc

import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
import torch.quantization
from torch.autograd import Variable
from torch.nn.parameter import Parameter
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
import torch.optim.lr_scheduler as lr_scheduler

# Flag for GPU
cuda = True if torch.cuda.is_available() else False

"""
Generator Network
"""

class Generator(nn.Module):
    def __init__(self, data_size, embedding_dim, hidden_dim, latent_dim, n_heads, dropout_rate = 0.2):   
        
        super(Generator, self).__init__()
        # self.relu = nn.ReLU(inplace = True)
        self.dropout_rate = dropout_rate

        self.gamma = nn.Parameter(torch.full((1, data_size), 1.0))

        self.input_atten_layer = nn.Sequential(
            GeneExpressionAttention(data_size, data_size, n_heads = n_heads, bias = True),
        )

        # FILM
        self.film1 = FiLM(data_size, embedding_dim)
        
        # encoder for the gene expression
        self.encoder = nn.Sequential(
            nn.Linear(data_size, hidden_dim),
            nn.Dropout(self.dropout_rate),
            FusedLeakyReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
            FusedLeakyReLU(),
            nn.Linear(hidden_dim // 2, latent_dim),
        )

        # FILM layer at the latent space

        # FILM
        self.film2 = FiLM(latent_dim, embedding_dim)
        
        # create a share decoder
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim // 2),
            FusedLeakyReLU(),
            nn.Linear(hidden_dim // 2, hidden_dim),
            nn.Dropout(self.dropout_rate),
            FusedLeakyReLU(),
            nn.Linear(hidden_dim, data_size),
        )

        self.decoder_beta = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim // 2),
            FusedLeakyReLU(),
            nn.Linear(hidden_dim // 2, hidden_dim),
            nn.Dropout(self.dropout_rate),
            FusedLeakyReLU(),
            nn.Linear(hidden_dim, data_size),
        )
        
    def forward(self, x, c):
        batch_size = x.shape[0]
        
        # attention layer with shortcut connection        
        atten_input = self.input_atten_layer(x) * self.gamma + x * (1 - self.gamma)
        data = self.film1(atten_input, c) # Film layer for conditioning
    
        # content network
        latent_data = self.encoder(data)

        # adding film layer in the latent space
        latent_data = self.film2(latent_data, c)
        corrected_gamma = self.decoder(latent_data)
        corrected_beta = self.decoder_beta(latent_data)
        
        return corrected_gamma, corrected_beta

"""
Discriminator
"""
class Discriminator(nn.Module):
    def __init__(self, data_size, embedding_dim, hidden_dim, latent_dim, n_heads, dropout_rate = 0.2):
        super(Discriminator, self).__init__()
        
        self.dropout_rate = dropout_rate

        self.relu_slope = 0.2
        self.gamma = nn.Parameter(torch.full((1, data_size), 1.0))

        self.input_atten = nn.Sequential(
            GeneExpressionAttention(data_size, data_size, n_heads = n_heads, bias = True),
        )

        # FILM
        self.film1 = FiLM(data_size, embedding_dim)
        
        self.model = nn.Sequential(
            nn.Linear(data_size, hidden_dim),
            nn.Dropout(self.dropout_rate),
            FusedLeakyReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
            FusedLeakyReLU(),
            nn.Linear(hidden_dim // 2, latent_dim),
            FusedLeakyReLU(),
        )

        # FILM
        self.film2 = FiLM(latent_dim, embedding_dim)
        
        self.adv_layer = nn.Linear(latent_dim, 1)
        

    def forward(self, data, c):
        # c = torch.log(c + 1)
        data = self.input_atten(data) * self.gamma + data * (1 - self.gamma)
        data = self.film1(data, c)
        out = self.model(data)

        # adding film in the latent space
        out = self.film2(out, c)
        validity =  self.adv_layer(out)

        return validity


### efficient self attention mechanism
def multi_attention(q, k, v, attn_mask=None, dropout=0.0, n_heads = 4):
    """
    Computes scaled dot product attention over three tensors.
    
    Args:
        q (torch.Tensor): Query tensor of shape (batch_size, num_heads, seq_len, d_k).
        k (torch.Tensor): Key tensor of shape (batch_size, num_heads, seq_len, d_k).
        v (torch.Tensor): Value tensor of shape (batch_size, num_heads, seq_len, d_v).
        attn_mask (torch.Tensor, optional): Attention mask of shape (batch_size, num_heads, seq_len, seq_len).
        dropout (float, optional): Dropout probability.

    Returns:
        torch.Tensor: Output tensor of shape (batch_size, num_heads, seq_len, d_v).
    """

    batch_size, n_heads, seq_len, d_k = q.size()
#     attn = torch.bmm(q, k.transpose(1, 3))
    attn = q @ k.transpose(-2, -1)
    attn = attn / math.sqrt(d_k/n_heads)
    
    if attn_mask is not None:
        attn = attn.masked_fill(attn_mask, float('-inf'))
        
    # before or after who know    
    attn = torch.nn.functional.dropout(attn, p=dropout)
    attn = torch.softmax(attn, dim=-1)
    
    output = attn @ v
    output = output.view(-1, seq_len * n_heads)    
    return output

class GeneExpressionAttention(nn.Module):
    def __init__(self, n_features, d_k, bias=True, bias_kv = False, n_heads=4):
        super(GeneExpressionAttention, self).__init__()
        self.d_k = d_k // n_heads
        self.bias = bias
        self.bias_kv = bias_kv
        self.n_heads = n_heads

        # Query representation
        self.W_Q = nn.Linear(n_features, self.d_k * n_heads, bias = self.bias)

        # Key and value pair to attend to
        self.W_K = nn.Linear(n_features, self.d_k * n_heads, bias = self.bias_kv)
        self.W_V = nn.Linear(n_features, self.d_k * n_heads, bias = self.bias_kv)


    def forward(self, tabular_data):
        batch_size = tabular_data.shape[0]
        
        # Project tabular data into Q, K, and V matrices
        Q = self.W_Q(tabular_data)
        K = self.W_K(tabular_data)
        V = self.W_V(tabular_data)

        # Split Q, K, and V into n_heads and also include the seq_length
        Q = Q.view(batch_size, self.n_heads, self.d_k, 1)
        K = K.view(batch_size, self.n_heads, self.d_k, 1)
        V = V.view(batch_size, self.n_heads, self.d_k, 1)

        # Apply multi-head attention
        out = multi_attention(Q, K, V, None, 0.0, self.n_heads)

        return out

### FusedLeakyRelu Activation layer
def fused_leaky_relu(input, bias, negative_slope=0.2, scale=2 ** 0.5):
    return F.leaky_relu(input + bias, negative_slope) * scale

class FusedLeakyReLU(nn.Module):
    def __init__(self, channel = 1, negative_slope=0.2, scale=2 ** 0.5):
        super().__init__()
        self.bias = nn.Parameter(torch.zeros(1, 1))
        self.negative_slope = negative_slope
        self.scale = scale

    def forward(self, input):
        # print("FusedLeakyReLU: ", input.abs().mean())
        out = fused_leaky_relu(input, self.bias,
                               self.negative_slope,
                               self.scale)
        
        # learnable negative slope parameter for fused leaky relu
        # out = torch.where((input + self.bias) >= 0, (input + self.bias), self.negative_slope * (input + self.bias)) * self.scale
        
        # print("FusedLeakyReLU: ", out.abs().mean())
        return out

### injecting noise layer for GAN model.
class InjectNoise(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.weight = nn.Parameter(torch.zeros(1, channels))

    def forward(self, x):
        noise = torch.randn((x.shape[0], 1), device=x.device)

        # print(self.weight.shape)
        # print(noise.shape)
        return x + self.weight * noise

# Define FiLM layer
class FiLM(nn.Module):
    def __init__(self, feature_dim, condition_dim):
        super(FiLM, self).__init__()
        self.gamma_fc = nn.Linear(condition_dim, feature_dim)
        self.beta_fc = nn.Linear(condition_dim, feature_dim)
        
    def forward(self, x, condition):
        gamma = self.gamma_fc(condition)
        beta = self.beta_fc(condition)
        return gamma * x + beta

# gradient penalty
def gradient_penalty(discriminator, real_data, fake_data, labels):
    batch_size = real_data.size(0)

    # adding epsilon error to the penalty as injecting the noise
    epsilon = torch.rand(batch_size, 1).to(device_ids[0])
    epsilon = epsilon.expand_as(real_data)

    interpolated = epsilon * real_data + (1 - epsilon) * fake_data
    interpolated = interpolated.to(device_ids[0])
    interpolated.requires_grad_(True)
    prob_interpolated = discriminator(interpolated, labels)
    
    gradients = torch.autograd.grad(
        outputs=prob_interpolated,
        inputs=interpolated,
        grad_outputs=torch.ones(prob_interpolated.size()).to(device_ids[0]),
        create_graph=True,
        retain_graph=True,
    )[0]
    gradients = gradients.view(batch_size, -1)
    gradient_penalty = ((gradients.norm(2, dim=1) - 1) ** 2).mean()
    return gradient_penalty

# gradient penalty using divergence.
def calculate_div_gp(prob_real_data, prob_fake_data, real_data, fake_data, k=2, p=2):
    """
    """    

    real_grad_outputs = torch.ones(prob_real_data.size()).to(real_data.device) if cuda else torch.ones(prob_real_data.size())

    fake_data.requires_grad_(True)

    fake_grad_outputs = torch.ones(prob_fake_data.size()).to(real_data.device) if cuda else torch.ones(prob_fake_data.size())

    real_gradient = torch.autograd.grad(
        outputs=prob_real_data,
        inputs=real_data,
        grad_outputs=real_grad_outputs,
        create_graph=True,
        retain_graph=True,
        only_inputs=True,
    )[0]
    
    fake_gradient = torch.autograd.grad(
        outputs=prob_fake_data,
        inputs=fake_data,
        grad_outputs=fake_grad_outputs,
        create_graph=True,
        retain_graph=True,
        only_inputs=True, 
    )[0]

    real_gradient_norm = real_gradient.view(real_gradient.size(0), -1).pow(2).sum(1) ** (p / 2)
    fake_gradient_norm = fake_gradient.view(fake_gradient.size(0), -1).pow(2).sum(1) ** (p / 2)

    gradient_penalty = torch.mean(real_gradient_norm + fake_gradient_norm) * k / 2
     
    return gradient_penalty

def generate_random_one_hot(input_vectors):
    """Generates random one-hot encoded vectors with different indices than the input.

    Args:
    input_vectors: A torch tensor of one-hot encoded vectors with shape (batch_size, num_classes).

    Returns:
    A torch tensor of random one-hot encoded vectors with shape (batch_size, num_classes).
    """

    batch_size, num_classes = input_vectors.shape
    output_vectors = torch.zeros_like(input_vectors)

    for i in range(batch_size):
        # Get a list of valid indices (not equal to the input's index)
        valid_indices = torch.where(input_vectors[i] == 0)[0].tolist()

        # Randomly choose an index from the valid indices
        random_index = torch.tensor(random.choice(valid_indices), dtype=torch.long)

        # Set the chosen index to 1 in the output vector
        output_vectors[i, random_index] = 1

    return output_vectors