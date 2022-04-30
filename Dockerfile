FROM python:3.8-slim-buster

RUN mkdir fly-catch
ADD . /fly-catch
WORKDIR /fly-catch
RUN pip3 install -r requirments/product_detail_app.txt

EXPOSE 8080
CMD uvicorn product_detail_app.app:app --port 8080 --host 0.0.0.0