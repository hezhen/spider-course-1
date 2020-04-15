# -*- coding: utf-8 -*-  
import scipy as sp  
import numpy as np  
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.datasets import load_files  
from sklearn.cross_validation import train_test_split  
from sklearn.feature_extraction.text import  TfidfVectorizer  
from sklearn.feature_extraction.text import  TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
import jieba
  
movie_reviews = load_files('comment')

f = open('stopwords.txt', 'rb')
stop_words_raw = f.read()
f.close()

stop_words = stop_words_raw.split('\n')

# BOOL型特征下的向量空间模型
count_vec = CountVectorizer(binary = False, decode_error = 'ignore', tokenizer=jieba.cut, stop_words=stop_words)  
x_train_vec = count_vec.fit_transform(movie_reviews.data)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(x_train_vec)

# 构造 Linear Kernel 的 SVC
linear_svc = SVC(kernel='linear')
# 构造 rbf 的 SVC，rbf 是默认kernel，因此等价于 SVN()
rbf_svc = SVC(kernel='rbf')
# 构造 sigmoid 的 SVC
sigmoid_svc = SVC(kernel='sigmoid')
# 构造 poly 的 SVC
poly_svc = SVC(kernel='poly')

# 用基于 tfidf 的特征词表与训练数据的标签来训练模型
linear_svc.fit(X_train_tfidf, movie_reviews.target)
rbf_svc.fit(X_train_tfidf, movie_reviews.target)
sigmoid_svc.fit(X_train_tfidf, movie_reviews.target)
poly_svc.fit(X_train_tfidf, movie_reviews.target)

# 构造测试样本
ratings_new = ['电影很好看','不好看','很不错的电影，太棒了','太赞了，很值得看的电影','烂','好让我失望']
X_new_counts = count_vec.transform(ratings_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

# 预测
print linear_svc.predict(X_new_tfidf)

print rbf_svc.predict(X_new_tfidf)

print sigmoid_svc.predict(X_new_tfidf)

print poly_svc.predict(X_new_tfidf)