# pull official base image
FROM python:3.12-rc-alpine3.18

# set work directory
WORKDIR /usr/src/mysite

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./mysite/requirements.txt /usr/src/mysite/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY ./mysite /usr/src/mysite

# copy entrypoint.sh
COPY ./mysite/entrypoint.sh /usr/src/mysite/entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/mysite/entrypoint.sh
RUN chmod +x /usr/src/mysite/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["mysite/entrypoint.sh"]