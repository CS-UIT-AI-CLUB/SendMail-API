FROM python:3.7.11

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update 
RUN pip3 install -r requirements.txt 

COPY . /app/

EXPOSE 5000

CMD ["python3", "main.py"]