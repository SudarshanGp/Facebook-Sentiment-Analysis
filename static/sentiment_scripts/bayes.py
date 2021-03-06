from __future__ import division

import sys
sys.path.insert(2, '/usr/local/lib/python2.7/site-packages')
import json
from dateutil.parser import parse
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.decomposition import NMF, LatentDirichletAllocation
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import pprint
import itertools

# Function to compute top topic terms from given model (i.e., LDA or NMF)

def get_topics(cv, model):
    # Number of terms per topic to display
    max_topics = 10

    # Number of terms per topic to retain
    max_labels = 5

    topics = []
    feature_names = cv.get_feature_names()

    # Iterate through the matrix components
    for idx, topic in enumerate(model.components_):

        # First we sort the terms in descending order ([::-1])
        # And then retiain only the top terms
        top_topics_idx = topic.argsort()[::-1][:max_topics]

        top_topics = [feature_names[jdx] for jdx in top_topics_idx]

        # Now extract out the terms themselves and display
        top_features = " ".join(top_topics)
        print('Topic {0:2d}: {1}'.format(idx, top_features).encode('utf-8').strip())
        topics.append(", ".join(top_topics[:max_labels]))

    return(topics)



with open('formatted.json') as data_file:
    data = json.load(data_file)
all_users = []
all_groups = []


for i, conversation in enumerate(data):
    # first_user = data[4]
    users = conversation['users'].split(',')
    print(users)

    messages = conversation['messages']  # 8418
    # month_text = ""
    for i, val in enumerate(messages):
        val['dates'] = parse(val['date'])

        # all_text.append(val['text'])
    # print(messages[0])
    # df = pd.DataFrame(all_text)
    messages.sort(key=lambda r: r['dates'])
    # pprint.pprint(messages)

    by_month = dict()
    for i, val in enumerate(messages):
        new_key = str(val['dates'].year) + ' ' + str(val['dates'].month)
        if new_key in by_month.keys():
            curr_list = by_month[new_key]
            curr_list.append(val['text'])
            by_month[new_key] = curr_list
        else:
            by_month[new_key] = [val['text']]
    # pprint.pprint(by_month)
    # blob = TextBlob(by_month[(2014, 7)])
#     month_sum = {}
    if len(by_month.keys())> 5:
        for key, value in by_month.iteritems():
            # df = pd.DataFrame(value)
            print(key)
            # pprint.pprint(df)
            if len(value) > 6:
                cv = TfidfVectorizer(stop_words = 'english',
                             lowercase=True,
                             # min_df=2,
                             max_features=5000)
                train_data = cv.fit_transform(value)
                # print(train_data)
                print(train_data.shape)
                num_topics = 6
                nmf = NMF(n_components = 6).fit(train_data)
                ret = get_topics(cv, nmf)
                print(ret)
#         # temp_arr = []
#         # print(value)
#         # print(key)
#         all_text = []
#         text_month = ""
#         for i, val in enumerate(value):
#             text_month += val
#             # print(val)
#             # print(blob.sentiment)
#
#             # print("here")
#             # temp_arr.append((blob.sentiment.p_pos, blob.sentiment.p_neg ))
#         # print(temp_arr)
#         blob = TextBlob(text_month, analyzer=NaiveBayesAnalyzer())
#         print(blob.sentiment)
#         print({'p_pos' :blob.sentiment.p_pos, 'p_neg' :blob.sentiment.p_neg, 'type' : blob.sentiment.classification })
#         month_sum[key] = {'p_pos' :blob.sentiment.p_pos, 'p_neg' :blob.sentiment.p_neg, 'type' : blob.sentiment.classification }
#         # if len(temp_arr) != 0:
#             # print(sum(temp_arr)/len(temp_arr))
#             # month_sum[key]= sum(temp_arr)/len(temp_arr)
#     if len(users) == 2:
#         all_users.append({'users': conversation['users'],'data': month_sum, 'len': len(list(month_sum.keys()))})
#     else:
#         all_groups.append({'users': conversation['users'],'data': month_sum, 'len': len(list(month_sum.keys()))})
#
#
# # pprint.pprint(all_users)
# new_all_users = filter(lambda user: user['len'] > 4, all_users)
# new_all_groups = filter(lambda user: user['len'] > 4, all_groups)
# # new_all_users_dict = {}
# # for item in new_all_users:
# #     name = item['users']
# #     new_all_users_dict[name] = item
# #
# # new_all_groups_dict = {}
# # for item in new_all_users:
# #     name = item['users']
# #     new_all_groups_dict[name] = item
#
#
# # json_data = [{type:'group', data:new_all_groups_dict }, {type:'user', data:new_all_users_dict}]
# with open('data_sentiment_group.json', 'w') as fp:
#     json.dump(new_all_groups, fp, )
#
# with open('data_sentiment_user.json', 'w') as fp:
#     json.dump(new_all_users, fp, )