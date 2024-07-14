#!/bin/bash

# Installing the required GPU dependencies of paddleOCR model.
python -m pip install paddlepaddle-gpu==3.0.0b0 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/

# install torch and torchaudio used by TTS package. This is done here to install GPU version of torch.
# Installing TTS does not do this.
python -m pip install torch==2.3.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu118

# NOTE the cuda version of both torch and paddle (11.8). To prevent any incompatibilities, the version
#       of both torch and paddle cuda version must match.

# install rest of requirements
pip install -r requirements.txt 
