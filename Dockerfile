FROM continuumio/miniconda

RUN apt-get update \
    && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /workspace
WORKDIR /workspace

RUN conda env create -f reqs3.yml
ENV PATH /opt/conda/envs/trading3/bin:$PATH