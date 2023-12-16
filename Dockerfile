FROM python:3.11.7 

RUN mkdir /task_app 

WORKDIR /task_app 

COPY requirements.txt . 

RUN pip install -r requirements.txt

COPY . . 

RUN chmod a+x /task_app/docker/app.sh

RUN alembic upgrade head

CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
