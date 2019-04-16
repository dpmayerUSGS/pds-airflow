// Setup instructions for tech demo.

// Build the airflow/isis3 docker image.

sudo docker build --tag airflow .

// Run the airflow docker image with an open port on 8080
// Binds to local folders for dags and out, change to appropriate folders on your machine

sudo docker run -it -p 8000:8080 --mount type=bind,source=/home/nick/drive/school/cs486c/pypline/in/,target=/root/airflow/dags/ --mount type=bind,source=/home/nick/drive/school/cs486c/pypline/out/,target=/out airflow

// In an alternate terminal find running container and open another terminal
sudo docker container ls
sudo docker exec -it suspicious_hellman bash

// Run the webserver and scheduler in the two open terminals
airflow webserver -p 8080
airflow scheduler

// Start up the flaskUI docker container
sudo docker run -it --net=host --expose 5001 -p 5050:5001 --mount type=bind,source=/home/nick/drive/school/cs486c/pypline/in/,target=/root/airflow/dags/ flaskui bash


sudo docker container ls

gllssical from_=5126r.cub gssi32.jpg
gllssi2isis gssi32.jpg
cam2map matchmap=default pixres=default from=5126r_cal.cub to=5126r.cub gssi32.jpg
spiceinit to=5126r_cal_map.cub defaultrange=default to=5126r_cal.cub from_=5126r.lbl gssi32.jpg
