FROM jjanzic/docker-python3-opencv:latest
WORKDIR /app
ADD Server /app
CMD ["python","scan.py"]