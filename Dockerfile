FROM python:3.9
ENV TZ=Asia/Taipei
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
VOLUME /app/log
CMD ["python", "main.py"]
