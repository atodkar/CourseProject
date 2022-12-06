# Trend Analysis using news articles

## Introduction
The idea of this project is to find trends on the market as well as business. Many times it is important to evaluate the market situation in just few sentences to get the high level idea of whether the market was positive or negative on the selected date. This particular exercise targets the same use case using LDA (Latent Dirichlet Analysis) for topic modelling.

## Technology and functionality
The algorithm is developed with two components. 

A server side python code and client side javascript single page application. Python code on server has three main tasks -
### Python
1. Connect to third party news vendors website such as NewsAPI, GNews and NewsData and fetch content based on date selection.
2. Apply LDA on the fetched news articles and extracts top topics.
3. Serve content of topic modeled over REST API using flask on python
4. Receive relevance feedback

On Javascript side, below tasks are done-
### Javascript (React)
1. The React application renders the webpage as single page application.
2. Based on date selection, fetches top topics as well as the content of all news article on that date.
3. Based on user's relevance selection, submit the relevance feedback to server


## Installation instructions
Run below commands to install all required packages for this project execution-

```shell
pip install -r ./backend/requirements.txt
cd frontend && npm install
```
First command installs all python libraries. the description of all libraries is given in libraries section.
We also need to install spacy language pack download with below command-

```shell
python -m spacy download en_core_web_sm
```

## Libraries

Python code runs on server side and requires below packages-
1. gensim - For LDA and related functions implementation
2. spacy - For lemmatization of words
3. flask - Python based webserver
4. pattern - This is being used for mining patterns
5. nltk - Natural language toolkit. Helpful as natural language utility


## Steps and time required
Below are the required tasks and respective time spent on the activities

1. API layer preparation for all three sources - 5 hours
2. Setup Flask Webserver to receive requests from UI - 1 hour
3. Prepare API on python webserver -
	a. Take date as input and respond with relevant articles trending that day with top trends - 1 hour
	b. Receive feedback on articles from user and use it as a validation - 30 minutes
4. Algorithm of LDA end to end implementation - 5 hours
5. Prepare React based UI to show a page which will call API and show top trending articles - 5 hours
6. Documentation and presentation - 4 hours

