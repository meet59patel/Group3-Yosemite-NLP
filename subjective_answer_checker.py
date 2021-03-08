import numpy as np
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize  
import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from scipy.spatial import distance
from sklearn.metrics.pairwise import cosine_similarity
import language_check
import language_tool_python
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

bert_model = SentenceTransformer('bert-base-nli-mean-tokens')



def preprocess(text1):
  stop_words = set(stopwords.words('english'))
  text1 = re.sub(r'[^A-Za-z0-9]+', ' ', text1)
  text1 = word_tokenize(text1)
  text = [w.lower() for w in text1 if not w in stop_words]
  ps = PorterStemmer()
  text = [ps.stem(w) for w in text]
  return text



def similarity(x,y):
  x = re.sub(r'[^A-Za-z0-9]+', ' ', x)
  y= re.sub(r'[^A-Za-z0-9]+', ' ', y)
  a = word_tokenize(x)
  b = word_tokenize(y)
  x1 = bert_model.encode(x)
  y1 = bert_model.encode(y)
  cosine_value = 1- distance.cosine(x1,y1)
  return cosine_value


#Calculate grammatical error
def grammar_error(list1):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(list1)
    return len(matches)


