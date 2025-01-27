
FROM python:3.12


WORKDIR /app

RUN pip install gunicorn==20.1.0 

COPY requirements.txt /app/

RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
