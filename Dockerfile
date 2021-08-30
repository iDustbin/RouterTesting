FROM python:3.8-slim-buster
COPY . .
RUN pip3 install -r requirements.txt
RUN apt update
RUN apt-get install -y iperf3
EXPOSE 5000
CMD python3 app.py