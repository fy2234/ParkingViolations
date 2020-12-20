FROM python:3.7

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY src/ /app

ENTRYPOINT ["python", "src/main.py"]


