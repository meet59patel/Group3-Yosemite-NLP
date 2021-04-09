import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize  
import nltk
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer 
from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
from nltk.corpus import stopwords
import re
import language_tool_python
from itertools import chain, product 
import os   
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))

def grammar_error(list1):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(list1)
    grammar_score = max(0,1 - len(matches)/len(list1))
    os.system("ps aux | grep 'languagetool-server.jar' | awk '{print $2}' | xargs kill -9")
    return float(grammar_score)

def bigram_similarity(ref,ans):
    bigram_ref = [b for b in zip(ref.split(" ")[:-1], ref.split(" ")[1:])] 
    bigram_ans = [b for b in zip(ans.split(" ")[:-1], ans.split(" ")[1:])]
    bigram_ref = set(bigram_ref)
    bigram_ans = set(bigram_ans)
    count=0
    for i in bigram_ref:
        if i in bigram_ans:
            count=count+1
    avg_length = (len(bigram_ans) + len(bigram_ref))/2
    return float(count/avg_length)

def synonym_similarity(ref_filtered , ans_filtered , ans_synonym):

    count = 0
    ref_set = set(ref_filtered)
    ans_set = ans_filtered
    for i in ans_set:
        if i in ref_set:
            count=count+1
        else:
            temp_set = ans_synonym[i]
            if i in temp_set:
                count=count+1
                break
        avg_length = float((len(ref_filtered) + len(ans_filtered))/2)
    return count/avg_length

def assess_answer(ref,ans,marks):
    
    # initialize
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    stop_words = set(stopwords.words('english'))
    
    # pre-process
    ref = re.sub(r'[^A-Za-z0-9]+', ' ', ref)
    ans= re.sub(r'[^A-Za-z0-9]+', ' ', ans)
    a= word_tokenize(ans)
    b = word_tokenize(ref)

    ref_filtered = [w for w in b if not w in stop_words]
    ans_filtered = [w for w in a if not w in stop_words] 
    ans_filtered1 = list(set(ans_filtered))
    ans_synonym = {}
    for i in ans_filtered1:
        synonyms = wn.synsets(i)
        lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
        ans_synonym.update({i:lemmas})

    ref1 = sbert_model.encode(ref)
    ans1 = sbert_model.encode(ans)
    
    # Compute Metrics
    # cosine similarity
    cosine_value = 1- distance.cosine(ref1,ans1)
    # jaccard similarity
    jaccard_value = jaccard_similarity(a,b)
    # grammar check
    grammar_score = grammar_error(ans)
    # bigrams for structural similarity
    bigram_value = bigram_similarity(ref,ans)
    # synonym similarity
    synonym_value = synonym_similarity(ref_filtered,ans_filtered,ans_synonym)

    final_marks=0
    if(marks==5):
        final_marks = 1.8*synonym_value + 1.2*bigram_value + 0.5*grammar_score + 0.4*cosine_value + 1.1*jaccard_value
    if(marks==10):
        final_marks = 4.2*synonym_value + 3.8*bigram_value + 0.5*grammar_score + 0.7*cosine_value + 0.8*jaccard_value
    if(marks==15):
        final_marks = 7.3*synonym_value + 4.7*bigram_value + 0.6*grammar_score + 1.0*cosine_value + 1.4*jaccard_value
    print(final_marks)
    return final_marks

# if __name__ == "__main__":
#     ref = "Jesus is always around us"
#     ans = "Jesus is my god"
#     marks = 5
#     assess_answer(ref,ans,marks)
    
