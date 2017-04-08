import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import datetime
from collections import Counter

# Customers
def get_customers_list(file_name):
    customers = set()
    with open(file_name, "rt", encoding='utf-16-le') as csvfile:
        datareader = csv.reader(csvfile, delimiter='\t')
        next(datareader, None)
        for row in datareader:
            customers.add(int(row[0]))
    
    return list(customers)

# Function for generating dates DataFrame
def get_all_dates(start, end):
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')
    days = (end - start).days + 1
    hours = days * 24
    date_list = [(start + datetime.timedelta(hours=h)).strftime('%Y-%m-%d %H') for h in range(0, hours)]
    
    return pd.DataFrame.from_items([('action_date_hour', date_list)])


# Get review for one client (list of words)
def get_review_from_raw_csv2(file_name, customer, dates_df):
    action_hour = []
    word = []

    with open(file_name, "rt", encoding='utf16') as csvfile:
        datareader = csv.reader(csvfile, delimiter='\t')
        next(datareader, None)
        for row in datareader:
            if int(row[0]) == customer:
                action_hour.append(row[1][:13])
                direction = 'INCOMING' if row[5] == '1' else 'OUTGOING'
                word.append(row[2] + '_' + direction + '_' + row[3] + '_' + row[4])

    df_dict = {}
    df_dict['action_hour'] = action_hour
    df_dict['word'] = word
    
    df = pd.DataFrame(df_dict)
    
    merged = df.merge(dates_df, left_on='action_hour', right_on='action_date_hour', how='outer')
    merged = merged.sort_values(by='action_date_hour').fillna('NOTHING')

    df = merged.groupby('action_date_hour')['word'].apply(list)
    
    out_list = []
    for i, d in df.iteritems():
        out_list.append(np.random.choice(d))

    return  out_list

def get_all_reviews(customers):
    all_reviews = []
    for cust in customers:
        all_reviews.append(get_review_from_raw_csv2(file_name=file_name, customer=cust, dates_df=dates))
    return all_reviews

def make_dictionary(reviews):
    l = [item for sublist in reviews for item in sublist]
    cnt = Counter(l)
    l = list(cnt)
    word_to_int = {w: i for i, w in enumerate(l)}
    return l, word_to_int

def encode_words(reviews, word_to_int):
    encoded_reviews = []
    for rev in reviews:
        encoded_reviews.append([word_to_int[w] for w in rev])
    
    return encoded_reviews

def get_labels(file, users):
    labels_list = []
    labels = pd.read_csv(file, sep='\t', encoding='utf-16-le')
    for user in users:
        labels_list.append(labels[labels['customer'] == user]['gone'].tolist()[0])
    return labels_list

def get_one_df(file_name, customer):
    action_hour = []
    word = []

    with open(file_name, "rt", encoding='utf-16-le') as csvfile:
        datareader = csv.reader(csvfile, delimiter='\t')
        next(datareader, None)
        for row in datareader:
            if int(row[0]) == customer:
                action_hour.append(row[1][:13])
                direction = 'INCOMING' if row[5] == '1' else 'OUTGOING'
                word.append(row[2] + '_' + direction + '_' + row[3] + '_' + row[4])

    df_dict = {}
    df_dict['action_hour'] = action_hour
    df_dict['word'] = word
    
    return pd.DataFrame(df_dict)

# Get review for one client (list of words)
def get_review_from_raw_csv_big(files, customer, dates_df):
    df1 = get_one_df(files[0], customer)
    df2 = get_one_df(files[1], customer)
    df3 = get_one_df(files[2], customer)
    
    df = pd.concat([df1, df2, df3])
    
    merged = df.merge(dates_df, left_on='action_hour', right_on='action_date_hour', how='outer')
    merged = merged.sort_values(by='action_date_hour').fillna('NOTHING')

    df = merged.groupby('action_date_hour')['word'].apply(list)
    
    out_list = []
    for i, d in df.iteritems():
        out_list.append(np.random.choice(d))

    return  out_list

# Customers
def get_customers_list_big(files):
    customers1 = get_customers_list(files[0])
    customers2 = get_customers_list(files[1])
    customers3 = get_customers_list(files[2])
    return list(set(customers1+customers2+customers3))


