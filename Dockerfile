FROM ubuntu:24.04

SHELL ["/bin/bash", "-c"]

RUN apt update && apt install python3 python3-pip python3.12-venv -y

COPY . /home/ubuntu/visual_cryptography

WORKDIR /home/ubuntu/visual_cryptography

RUN python3 -m venv ./venv

RUN venv/bin/python3 -m pip install --upgrade pip
RUN venv/bin/pip install opencv-python-headless
RUN venv/bin/pip install gradio

EXPOSE 8080

CMD ["venv/bin/python3", "GUI.py"]
