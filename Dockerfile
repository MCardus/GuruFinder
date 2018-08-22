FROM python:3.6-stretch

# Installing external dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Installing internal dependencies
COPY . ./gurufinder
RUN pip install gurufinder/
RUN pip install git+https://github.com/MCardus/text_models.git
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords