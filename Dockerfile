FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
ADD flaskui /root/pds-airflow-techdemo
WORKDIR /root/pds-airflow-techdemo
RUN pip3 install flask flask-restful requests
RUN chmod +x /root/pds-airflow-techdemo/start.sh
EXPOSE 5000
EXPOSE 5001
CMD /root/pds-airflow-techdemo/start.sh
ENTRYPOINT /root/pds-airflow-techdemo/start.sh && /bin/bash
