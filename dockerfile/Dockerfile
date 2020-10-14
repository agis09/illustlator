FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04


RUN    apt update  -qy
RUN    apt upgrade -qy

RUN    apt install wget -qy
RUN    apt install tar -qy
RUN    apt install curl -qy
RUN    apt install python3-pip -qy
RUN    apt install -qy vim 
RUN    apt install -qy git

RUN    pip3 install -q pandas
RUN    pip3 install -q tensorflow-gpu
RUN    pip3 install -q keras
RUN    pip3 install -q scikit-learn
RUN    pip3 install -q jupyterlab
RUN    pip3 install -q matplotlib
RUN    pip3 install -q tqdm
