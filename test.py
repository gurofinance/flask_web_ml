# import pandas as pd

# df = pd.read_csv('static/csv_file/final_test.csv', encoding='utf-8')

# print(df)

from pymongo import MongoClient

import pandas as pd
from bson.objectid import ObjectId

client = MongoClient('mongodb+srv://root:1234@cluster0.il3ga.mongodb.net/guro?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true')

# print(db.list_database_names())
db = client['guro']
collection = db['dataframe']

import datetime
post = {"author": "KIM",
        "text": "My second blog post!",
        "tag" :"data",
        "tags": ["mongodb", "python", "pymongo","fewfwefwefwefwef"],
        "date": datetime.datetime.utcnow()
        }
# collection.insert_one(post)
# data = list(collection.find())
# print(data)
# print(collection.find())

df = pd.read_csv('datasets/test.csv', encoding='utf-8')
# df.drop(['Unnamed: 0'] , axis=1, inplace=True)
# df_dict = df.to_dict('records')
# insert_data = {
#     "index":"titanic_test_preprocessing",
#     "data":df_dict,
#     "date":datetime.datetime.utcnow()
# }

# collection.insert_one(insert_data)
# print("Success")


# df = pd.read_csv('static/csv_file/final_train.csv', encoding='utf-8')
# df.drop(['Unnamed: 0'] , axis=1, inplace=True)
# df_dict = df.to_dict('records')
# insert_data = {
#     "index":"titanic_train_preprocessing",
#     "data":df_dict,
#     "date":datetime.datetime.utcnow()
# }

# collection.insert_one(insert_data)
# print("Success")

# result = collection.find_one({"_id":ObjectId("61c2a8ac46fa7adcbbb87701")})
# print(result)

# result = collection.find_one({"index":"titanic_test_preprocessing"})
# # print(result['data'])

# result_df = pd.DataFrame(result['data'])
# # print(result_df.head())
# print(result_df.info())

# df_age_fare_sex_male = df.iloc[:,[1 , 2,-1]]
df_dict = df.to_dict('records')
# print(df_age_fare_sex_male)
insert_data = {
    "index":"df_test",
    "data":df_dict,
    "date":datetime.datetime.utcnow()
}

collection.insert_one(insert_data)