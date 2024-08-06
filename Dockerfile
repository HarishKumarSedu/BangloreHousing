FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD flask run --host=0.0.0.0 --port=$PORT app:app