FROM python:3.10.5-alpine
ADD requirements.txt .
RUN pip install -r ./requirements.txt

COPY . ./
WORKDIR ./friends_service
RUN python manage.py migrate
CMD ["gunicorn", "friends_service.wsgi", "-b", "0.0.0.0:8000"]
