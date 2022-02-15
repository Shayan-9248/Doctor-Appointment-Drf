# Doctor Appointment

*This repo implement a Doctor Appointment that uses **Django Rest Framework** as a rest-api foundation on **Python***

### Usage

#### Installation

* [docker](https://docs.docker.com/engine/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

**Requirements**

*Python3.10*

``` 
    After you install docker you can run rabbitmq with this command:
        - docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
```

```
    Now you are able to run the project via this command:
        - docker-compose up -d
```

```
    If you want to run the project without docker you can this the below commands:
        1. Create a virtual environment via python3 -m venv venv.
        2. Activate venv through source venv/bin/activate.
        3. You must copy a sample of .env-sample in .env file with cp .env-sample .env.
        4. install all of the requirements package via command pip install -r requirements.txt.
        5. Run the following command to get the database ready to go:

            python manage.py migrate
```

*Now you can run the project with **python manage.py runserver** and this site will be available on localhost://8000*