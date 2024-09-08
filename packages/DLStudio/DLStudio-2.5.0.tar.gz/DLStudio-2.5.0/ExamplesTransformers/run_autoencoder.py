#!/usr/bin/env python

##  run_autoencoder.py

"""
This script is for experimenting with the Autoencoder class in the TRansformers module of DLStudio.
module in DLStudio.
"""

"""
seed = 0           
random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
numpy.random.seed(seed)
torch.backends.cudnn.deterministic=True
torch.backends.cudnn.benchmarks=False
os.environ['PYTHONHASHSEED'] = str(seed)
"""

##  watch -d -n 0.5 nvidia-smi

from DLStudio import *
from Transformers import *
import os, sys


dataroot = "./data/CIFAR-10/"
#dataroot =  "/home/kak/ImageDatasets/CIFAR-10/"
#dataroot = "/mnt/cloudNAS3/Avi/ImageDatasets/CIFAR-10/"

embedding_size = 256

num_basic_encoders = num_basic_decoders = num_atten_heads = 4

epochs = 100
#epochs = 20

#batch_size = 8
batch_size = 48         

learning_rate = 1e-4

image_size = (32,32)                
#patch_size = (8,8)              
patch_size = (4,4)                    

# encoder_out_size = (16,16)
#encoder_out_size = (4,4)
encoder_out_size = (8,8)

decoder_out_size = (32,32)

dls = DLStudio(
                  dataroot = dataroot,
                  image_size = image_size,
                  path_saved_model = "./saved_VAE_model",
                  learning_rate = learning_rate,        
                  epochs = epochs,
                  batch_size = batch_size,
                  use_gpu = True,
              )

vit =  visTransformer( 
                  dl_studio = dls,
                  patch_size = patch_size,
                  embedding_size = embedding_size,
                  num_basic_encoders = num_basic_encoders,
                  num_basic_decoders = num_basic_decoders,
                  num_atten_heads = num_atten_heads,
                  encoder_out_size = encoder_out_size,
                  decoder_out_size = decoder_out_size,
                  save_checkpoints = True,
                  checkpoint_freq = 5         ## a checkpoint will be created every so many epochs
               )

autoenc  =  Autoencoder( vis_trans = vit  )           

vit.load_cifar_10_dataset()

## display network properties
number_of_learnable_params_in_autoencoder = sum(p.numel() for p in autoenc.parameters() if p.requires_grad)
print("\n\nThe number of learnable parameters in the autoencoder: %d" % number_of_learnable_params_in_autoencoder)

dls.load_cifar_10_dataset()

autoenc.run_code_for_training_autoencoder(vit, autoenc, display_train_loss=True, checkpoint_dir="checkpoints_VAE")

autoenc.run_code_for_evaluating_autoencoder(vit, autoenc)
