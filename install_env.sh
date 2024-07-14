#!/bin/bash

# Upgrade pip
python -m pip install --upgrade pip

# install torch and torchaudio used by TTS package. This is done here to install GPU version of torch.
# Installing TTS does not do this.
python -m pip install torch==2.3.0 torchaudio==2.3.0 -i https://download.pytorch.org/whl/cu121

# Installing the required GPU dependencies of paddleOCR model.
python -m pip install paddlepaddle-gpu==2.6.0.post120 -f https://www.paddlepaddle.org.cn/whl/windows/mkl/avx/stable.html

: '
 NOTE: Using different versions of cuda for torch and paddle to prevent cuda version conflicts 
      or cuda overwrites by both libraries.
'

: '
Potential Issues encountered:
1- Environment variables: The installation order can affect how environment variables are set, 
which is crucial for the proper functioning of CUDA-enabled libraries

2- Potential conflicts: Installing one library after the other might overwrite or conflict with shared dependencies,
leading to issues like the one you encountered with the cudnn_adv_infer64_8.dll file
'

# install rest of requirements
pip install -r requirements.txt 
