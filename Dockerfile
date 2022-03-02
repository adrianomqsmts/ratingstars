FROM python:3

RUN apt-get update -y && \
  apt-get install -y python3-pip python3-dev

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

VOLUME [ ".:/app" ]

EXPOSE 5000


CMD ["gunicorn", "project.app:app"]