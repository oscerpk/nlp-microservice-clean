FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 50051 7860

CMD ["python", "grpc_server.py"]
