FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
  acpica-tools \
  python3-augeas \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY geco.py ./
COPY geco ./geco/

CMD [ "python", "./geco.py" ]
