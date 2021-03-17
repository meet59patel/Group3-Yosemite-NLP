from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
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
from collections import OrderedDict
from copy import deepcopy
from itertools import chain
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

bert_model = SentenceTransformer('bert-base-nli-mean-tokens')
nlp = spacy.load('en_core_web_sm')


#remove stopwords and stemming
def preprocess(text1):
  stop_words = set(stopwords.words('english'))
  text1 = re.sub(r'[^A-Za-z0-9]+', ' ', text1)
  text1 = word_tokenize(text1)
  text = [w.lower() for w in text1 if not w in stop_words]
  ps = PorterStemmer()
  text = [ps.stem(w) for w in text]
  return text

#calculate cosine similarity
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



class TextRank4Keyword():
    
    
    def __init__(self):
        self.d = 0.85 
        self.min_diff = 1e-5 
        self.steps = 10 
        self.node_weight = None 

    
    def set_stopwords(self, stopwords):  
        
        for word in STOP_WORDS.union(set(stopwords)):
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True
    
    def sentence_segment(self, doc, candidate_pos, lower):
        sentences = []
        for sent in doc.sents:
            selected_words = []
            for token in sent:
                
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)
            sentences.append(selected_words)
        return sentences
        
    def get_vocab(self, sentences):
        
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab
    
    def get_token_pairs(self, window_size, sentences):
       
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i+1, i+window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs
        
    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())
    
    def get_matrix(self, vocab, token_pairs):
        
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1
            
        # Get Symmeric matrix
        g = self.symmetrize(g)
        
        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm!=0) # this is ignore the 0 element in norm
        
        return g_norm

    
    def get_keywords(self, number=10):
        
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        keywords=[]
        for i, (key, value) in enumerate(node_weight.items()):
           
            keywords.append(key)
            if i > number:
                break
        return keywords
        
        
    def analyze(self, text, 
                candidate_pos=['NOUN', 'PROPN'], 
                window_size=4, lower=False, stopwords=list()):
       
        
        # Set stop words
        self.set_stopwords(stopwords)
        
        # Pare text by spaCy
        doc = nlp(text)
        
        # Filter sentences
        sentences = self.sentence_segment(doc, candidate_pos, lower) # list of list of words
        
        # Build vocabulary
        vocab = self.get_vocab(sentences)
        
        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)
        
        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)
        
        # Initionlization for weight(pagerank value)
        pr = np.array([1] * len(vocab))
        
        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1-self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr))  < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]
        
        self.node_weight = node_weight

def compare_keyWords(x,y):
    
    x_tokens=[]
    for x1 in x :
        x1=x1.replace(".","")
        x1=x1.replace(",","")
        x1=x1.replace("'","")
        x1=x1.replace(";","")
        x_tokens+=word_tokenize(x1)
    y_tokens=[]
    for y1 in y:
        y1=y1.replace(".","")
        y1=y1.replace(",","")
        y1=y1.replace("'","")
        y1=y1.replace(";","")
        y_tokens+=word_tokenize(y1)
    
    sw = stopwords.words('english') 
    x_List={w for w in x_tokens if not w in sw}
    y_List={w for w in y_tokens if not w in sw}
    Y_List=list(deepcopy(y_List))
    for wordToken in y_List : 
        synonyms=wn.synsets(wordToken)
        
        Y_List+=list(set(chain.from_iterable([word.lemma_names() for word in synonyms])))
    
    ps = PorterStemmer()
    X_set = {ps.stem(w) for w in x_List}
    Y_set = {ps.stem(w) for w in Y_List}
    
    count=0
    for ak in X_set :
        if ak in Y_set :
            count+=1
    return count

Error_Threshold = 6
def predict_Marks(model_ans,student_ans,max_marks,threshold_similarity=0.3,accuracy=0.5):
  context_similarity = similarity(model_ans,student_ans)
  if context_similarity < threshold_similarity:
    return 0
  extracted_keywords_student=TextRank4Keyword()
  extracted_keywords_student.analyze(student_ans, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
  extracted_keywords_student=extracted_keywords_student.get_keywords(15)

  extracted_keywords_model=TextRank4Keyword()
  extracted_keywords_model.analyze(model_ans, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
  extracted_keywords_model=extracted_keywords_model.get_keywords(15)

  extracted_keywords_match=compare_keyWords(extracted_keywords_model,extracted_keywords_student)
  if (len(extracted_keywords_model)==0):
    return round(context_similarity*max_marks)
  
  no_of_errors = grammar_error(student_ans)
  if no_of_errors > Error_Threshold:
    return 0
  
  marks_Factor = extracted_keywords_match/len(extracted_keywords_model)
  marks_Factor=marks_Factor**(1/3)
  return round(marks_Factor*max_marks/accuracy)*accuracy

  


