FROM python:3

WORKDIR /app
COPY . .
RUN python3 -m pip install -r requirements.txt

CMD ["python3", "app.py"]

EXPOSE 8080/tcp
