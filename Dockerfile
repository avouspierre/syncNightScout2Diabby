FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD NS2D.py .
ADD .env .

CMD [ "python", "./NS2D.py" ]
