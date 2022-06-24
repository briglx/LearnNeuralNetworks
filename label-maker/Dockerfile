FROM python:3.7-alpine
# RUN apt-get update -y
# RUN apt-get install -y python-pip python-dev build-essential
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["python"]
RUN chmod 644 app.py
CMD ["app.py"]