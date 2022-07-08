FROM python:3.9 AS build

COPY requirements.txt /requirements.txt

RUN \
    python3 -m pip install --upgrade pip && \
    pip install -r /requirements.txt && \
    pip uninstall -y pymongo==4.1.1 && \
    pip install pymongo[srv]==3.12.3

RUN \
    find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | \
    xargs rm -rf

FROM gcr.io/distroless/python3-debian11

ENV LOG_LEVEL=INFO

COPY --from=build \ 
    /usr/local/lib/python3.9/site-packages \
    /site-packages

ENV PYTHONPATH=/site-packages

WORKDIR /app

COPY ./application ./application
COPY ./cms ./cms
COPY ./static ./static
COPY ./templates ./templates
COPY manage.py kwlog.py ./

ENV PORT=8000

ENTRYPOINT ["python", "-m", "gunicorn", "application.wsgi", "--bind", "0.0.0.0:8000"]
