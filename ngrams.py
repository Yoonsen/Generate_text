#!/usr/bin/env python
# coding: utf-8

# # Trying stuff

# In[6]:


import dhlab as dh
from IPython.display import HTML, Markdown
import os
import sqlite3
import pandas as pd



uni = "/mnt/disk2/NB-ngram-assoc/unigram-one-row.db"
bi = "/mnt/disk2/NB-ngram-assoc/bigram-one-row.db"
tri = "/mnt/disk2/NB-ngram-assoc/trigram-one-row.db"

def query(db, sql, params=()):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        res = cur.execute(sql, params).fetchall()
    return res

def search(expr, lang = 'nob', limit = 10):
    mapping = {0:"first", 1:"second", 2:"third"}
    func_map = {0:unigrams, 1:bigrams, 2:trigrams}
    kwargs = dict()
    for i,e in enumerate([x.strip() for x in expr.split()]):
        if i > 2:
            i = 2
            break
        if e != "*":
            kwargs[mapping.get(i)] = e
    return func_map[i](lang = lang, limit=limit, **kwargs)
            

def trigrams(first=None, second=None, third=None, limit = 10, lang='nob', order='assoc'):
    a = locals()
    lang = a['lang']
    limit = a['limit']
    order = a['order']
    qs = [f"{k} = '{a[k]}'" for k in a if a[k] is not None and k in ['first','second', 'third']]
    q = ' and '.join(qs)
    if q != "":
        q = " and " + q
    res = query(tri, f"""
        select first, second, third, freq, assoc 
        from trigram 
        where 
            lang = '{lang}' 
            {q} 
        order by {order} 
        desc 
        limit {limit}""")
    return pd.DataFrame(res, columns="first second third freq assoc".split())

def bigrams(first=None, second=None, limit = 10, lang='nob', order='pmi'):
    a = locals()
    lang = a['lang']
    limit = a['limit']
    order = a['order']
    qs = [f"{k} = '{a[k]}'" for k in a if a[k] is not None and k in ['first','second', 'third']]
    q = ' and '.join(qs)
    if q != "":
        q = " and " + q
    res = query(bi, f"""
        select first, second, freq, pmi 
        from bigram 
        where 
            lang = '{lang}' 
            {q} 
        order by {order} 
        desc 
        limit {limit}""")
    return pd.DataFrame(res, columns="first second freq pmi".split())

def unigrams(first=None, limit = 10, lang='nob', order='freq'):
    a = locals()
    lang = a['lang']
    limit = a['limit']
    order = a['order']
    qs = [f"{k} = '{a[k]}'" for k in a if a[k] is not None and k in ['first','second', 'third']]
    q = ' and '.join(qs)
    if q != "":
        q = " and " + q
    res = query(uni, f"""
        select first, freq 
        from unigram 
        where 
            lang = '{lang}' 
            {q} 
        order by {order} 
        desc 
        limit {limit}""")
    return pd.DataFrame(res, columns="first freq".split())


