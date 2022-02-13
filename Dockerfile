FROM python:3.9

LABEL maintainer="shayan.aimoradii@gmail.com"

WORKDIR /src/ 
COPY . /src/

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]