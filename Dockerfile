FROM python:3.12-bullseye
WORKDIR /app
COPY requirements.txt .
COPY packages/ ./packages/
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-index --find-links=./packages -r requirements.txt
COPY . .
#COPY app .
EXPOSE 8501

