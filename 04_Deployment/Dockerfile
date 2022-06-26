FROM agrigorev/zoomcamp-model:mlops-3.9.7-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app
COPY [ "model2.bin", "model.bin" ]


docker run -it agrigorev/zoomcamp-model:mlops-3.9.7-slim bash
