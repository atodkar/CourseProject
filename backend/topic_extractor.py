"""
This core class holds logic for topic modelling using LDA.
"""
import re
import nltk
import gensim
from nltk.corpus import stopwords
from gensim.models.ldamodel import LdaModel
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
import spacy


class TopicExtractor(object):
    """
    This class extracts top topics from news articles
    """

    def __init__(self):
        nltk.download('stopwords')
        self.stop_words = stopwords.words('english')

    @staticmethod
    def sentenceToWords(sentences):
        for line in sentences:
            yield gensim.utils.simple_preprocess(str(line), deacc=True)

    @staticmethod
    def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        """
        Lemmatize the words, convert to normal words
        """
        nlp = spacy.load('en_core_web_sm')
        texts_out = []
        for sent in texts:
            doc3 = nlp(" ".join(sent))
            texts_out.append([token.lemma_ for token in doc3 if token.pos_ in allowed_postags])
        return texts_out

    @staticmethod
    def prepareLDAModel(lemmatized_data):
        """
        This method prepares the LDA Model based on lemmatized data
        """
        id2word = corpora.Dictionary(lemmatized_data)

        # Create Corpus
        corpus = [id2word.doc2bow(text) for text in lemmatized_data]

        lda_model = LdaModel(corpus=corpus,
                             id2word=id2word,
                             num_topics=5,
                             random_state=100,
                             update_every=1,
                             chunksize=100,
                             passes=10,
                             alpha='auto',
                             per_word_topics=True)
        return lda_model

    @staticmethod
    def parseTopTopics(lda_model):
        topics = lda_model.print_topics(5)
        top = []
        for t in topics:
            word_list = re.findall(r'"([^"]*)"', t[1])[1:6]
            main_topic = ' '.join(word_list)
            # remove char
            main_topic = main_topic.replace("char", "")
            top.append(main_topic.capitalize())
        return top

    def getTopTopicsForTheArticle(self, content):
        """
        This method extracts topics from the article
        """
        sentences = content.split('.')
        data_words = list(self.sentenceToWords(sentences))

        # using bigram language model for this modelling
        bigram = gensim.models.Phrases(data_words, min_count=10, threshold=500)

        # Faster way to get a sentence clubbed as a trigram/bigram
        bigram_mod = gensim.models.phrases.Phraser(bigram)

        # Remove Stopwords
        data_words_nostops = [[word for word in simple_preprocess(str(doc1)) if word not in self.stop_words] for doc1 in
                              data_words]

        # Prepare Bigrams
        bigram_data_words = [bigram_mod[doc2] for doc2 in data_words_nostops]

        # Do lemmatization keeping only noun, adj, vb, adv
        lemmatized_data = self.lemmatization(bigram_data_words, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

        lda_model = self.prepareLDAModel(lemmatized_data)

        return self.parseTopTopics(lda_model)
