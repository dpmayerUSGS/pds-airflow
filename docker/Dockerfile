FROM continuumio/miniconda3

RUN apt-get update
RUN apt-get install -y rsync libglu1 libgl1

RUN conda config --add channels conda-forge
RUN conda config --add channels usgs-astrogeology
ADD environment.yml /tmp/environment.yml

RUN conda env create -f /tmp/environment.yml

ENV PATH /opt/conda/envs/PDS-Pipelines/bin:$PATH 
ENV AIRFLOW_HOME ~/airflow
ENV ISISROOT /opt/conda/envs/PDS-Pipelines/
ENV ISISDATA /opt/conda/envs/PDS-Pipelines/data
ADD img /img
ADD airflow.cfg /root/airflow/airflow.cfg
RUN airflow initdb

EXPOSE 8080

RUN echo "source activate PDS-Pipelines" >> /root/.bashrc
RUN echo "python /opt/conda/envs/PDS-Pipelines/scripts/isis3VarInit.py" >> /root/.bashrc
RUN echo "source activate PDS-Pipelines" >> /root/.bashrc

ADD entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh
ENTRYPOINT /root/entrypoint.sh && /bin/bash

RUN apt-get install -y wget zip
