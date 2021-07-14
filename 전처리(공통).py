#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import re
from hanspell import spell_checker
from konlpy.tag import Mecab
import konlpy


# In[4]:


trade_df = pd.read_excel('data/crawling/유통_무역_운송.xls')
edu_df = pd.read_excel('data/crawling/교육업.xls')
cons_df = pd.read_excel('data/crawling/건설업.xls')


# In[7]:


trade_df.drop('Unnamed: 0', axis = 1, inplace = True)
edu_df.drop('Unnamed: 0', axis = 1, inplace = True)
cons_df.drop('Unnamed: 0', axis = 1, inplace = True)


# In[8]:


trade_df.set_index('회사', inplace = True)
edu_df.set_index('회사', inplace = True)
cons_df.set_index('회사', inplace = True)


# In[10]:


trade_df.drop_duplicates(['요약','장점','단점','경영진에게 바라는 점'], inplace = True)
edu_df.drop_duplicates(['요약','장점','단점','경영진에게 바라는 점'], inplace = True)
cons_df.drop_duplicates(['요약','장점','단점','경영진에게 바라는 점'], inplace = True)


# In[11]:


# 영어와 한글만 남기는 함수 정의
def clean_text(df):
    for col in df.columns[2:]:
        df[col] = df[col].str.replace("[^a-zA-Z가-힇]", " ")


# In[12]:


# py-hanspell을 이용한 맞춤법 검사 함수 정의
def spelling(df):
    # [요약]부터 [경영진에게 바라는 점]까지
    for col in df.columns[2:]:
        for j in range(df.shape[0]):
            try:
                # 고칠 게 있으면 고치고 기존 데이터 대체
                result_train = spell_checker.check(df[col][j])
                df[col][j] = result_train.as_dict()['checked']
            except:
                # 없으면 pass
                pass


# In[17]:


clean_text(cons_df)


# In[ ]:


spelling(trade_df)


# In[26]:


# mecab 토큰화 및 불용어 처리
mecab = Mecab()
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

korean_stopwords_path='./stopword_수정.txt'

# 텍스트 파일 오픈
with open(korean_stopwords_path,encoding='utf-8') as f:
    stopwords=f.readlines()
stopwords=[x.strip() for x in stopwords]


# In[ ]:


df['요약토큰화'] = df['요약'].apply(mecab.morphs)
df['요약토큰화'] = df['요약토큰화'].apply(lambda x: [item for item in x if item not in stopwords])

