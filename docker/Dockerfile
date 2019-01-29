FROM continuumio/miniconda3

RUN conda config --add channels conda-forge
RUN conda config --add channels usgs-astrogeology
ADD environment.yml /tmp/environment.yml

RUN conda env create -f /tmp/environment.yml
RUN echo "conda activate PDS-Pipelines" > ~/.bashrc
RUN echo "python $CONDA_PREFIX/scripts/isis3VarInit.py" > ~/.bashrc
RUN echo "conda activate PDS-Pipelines" > ~/.bashrc

ENV PATH /opt/conda/envs/PDS-Pipelines/bin:$PATH
ENV AIRFLOW_HOME ~/airflow
ADD airflow.cfg /root/airflow/airflow.cfg
ADD airflow_scheduler.sh /root/airflow/
RUN airflow initdb
RUN apt-get update

RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc
RUN echo "conda activate" >> ~/.bashrc
RUN apt-get install -y rsync libglu1 libgl1



