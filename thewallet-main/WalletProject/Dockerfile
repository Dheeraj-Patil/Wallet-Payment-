FROM python:3.9-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install
RUN apt install -y python-psycopg2

RUN mkdir /usr/src/tachyon/
WORKDIR /usr/src/tachyon/
COPY requirements.txt /usr/src/tachyon/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /usr/src/tachyon/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]