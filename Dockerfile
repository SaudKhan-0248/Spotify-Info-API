FROM python:3.11.5-alpine3.18
WORKDIR /src/
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python3", "run.py"]
