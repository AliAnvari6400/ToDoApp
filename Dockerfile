FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERE=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY ./core /app/
#EXPOSE 8000
#CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
