from flask import Flask , request , render_template ,Response, request, redirect
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import random
import io
from pymongo import MongoClient
import pickle

import pandas as pd
from bson.objectid import ObjectId
import datetime

app = Flask(__name__)

client = MongoClient('mongodb+srv://root:1234@cluster0.il3ga.mongodb.net/guro?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true')

# print(db.list_database_names())
db = client['guro']
collection = db['dataframe']

@app.route('/', methods=['GET', 'POST'])
def index(): 
    f_name = "태경"
    results = list(collection.find())
    # print(results[0]['index'])
    results_index = []
    for x in results:
        results_index.append(x['index'])
        # print(x['index'])
    return render_template('index.html',results = results_index)

@app.route('/plot', methods=['GET', 'POST'])
def graph_image():
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    xs = range(100)
    ys = [random.randint(1,50) for x in xs]
    axis.plot(xs ,ys )
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue() , mimetype='image/png')

@app.route('/test', methods=['GET', 'POST'])
def chart_test():
    price= [['apple', 'banana' , 'lemon', 'strewberry'] , [1000, 500, 800,1500]]
    plt.plot(price[0], price[1])
    plt.savefig('static/image/price.png')
    return render_template('price.html' , name="과일가격", url="static/image/price.png")

from titanic_logistic import *
@app.route('/density',methods=['GET', 'POST'] )
def density_graph():
    if request.method == 'GET':
        return render_template('density.html', name=None , url=None)
    else:
        column = request.form['column']
        # print(column)
        density(column)
        return render_template('density.html', name=column, url=f'static/image/{column}.png')

@app.route('/preprocessing' , methods=['GET', 'POST'])
def data_preprocessing():
    if request.method == "POST":
        final_train , final_test = preprocessing()
        print(final_train)
        print(final_test)
        return "SUCCESS"
@app.route('/read_data', methods=['GET', 'POST'])
def read_data():
    if request.method == 'GET':
        results = list(collection.find())
        # print(len(results))
        results_index = []
        for x in results:
            results_index.append(x['index'])
        results_index = list(set(results_index))
        print(results_index)
        return render_template('read_data.html' ,results = results_index )
    else:
        # df = pd.read_csv('static/csv_file/final_test.csv', encoding='utf-8')
        index = request.form.get('index')
        print(index)
        result = collection.find_one({'index':index})
        name = result['index']
        data = result['data']

        column_name = list(data[0].keys())
        print(data[0].keys())
        # print(result)
        return  render_template('read_data_result.html', name=name,columns=column_name, data = data)

@app.route('/params/<int:data>', methods=['GET', 'POST'])
def params_test(data):
    index = data
    df = pd.read_csv('static/csv_file/final_test.csv', encoding='utf-8')
    result = df.iloc[index]
    describe = df.describe()
    print(describe)
    return render_template('params_test.html',name =index , result=result )

@app.route('/dataframe/<index>', methods=['GET', 'POST'])
def dataframe(index):
    if request.method == "GET":
        result = collection.find_one({"index":index})
        result_df = pd.DataFrame(result['data'])
        # print(result_df.columns)
        columns = result_df.columns
        data = result['data']
        # return result_df.to_html()
        return render_template('dataframe.html' , name =index, columns=columns,   data = data)

    else:
        print(request.form.getlist('column'))
        select_list = request.form.getlist('column')
        result = collection.find_one({"index":index})
        result_df = pd.DataFrame(result['data'])
        result_df = result_df.loc[:, select_list]
        result_list = result_df.to_dict('records')
        insert_data= {
            "index":f'{select_list[0]}_{datetime.datetime.utcnow()}',
            "data":result_list,
            "date":datetime.datetime.utcnow()

        }
        collection.insert_one(insert_data)
        print(list(result_list))
        return redirect('/read_data')
@app.route('/remove/<name>', methods=['POST'])
def data_remove(name):
    collection.delete_many({'index':name})
    return redirect('/read_data')


@app.route('/predict', methods=['POST'])
def predict():
    model_name = request.form.get('model_name')
    with open(f'models/{model_name}', 'rb') as f:
        model = pickle.load(f)
#         data = [[1.799e+01, 1.038e+01, 1.228e+02 ,1.001e+03 ,1.184e-01 ,2.776e-01, 3.001e-01,
#  1.471e-01, 2.419e-01 ,7.871e-02,1.095e+00, 9.053e-01, 8.589e+00, 1.534e+02,
#  6.399e-03 ,4.904e-0, 5.373e-02 ,1.587e-02 ,3.003e-02, 6.193e-03, 2.538e+01,
#  1.733e+01 ,1.846e+02, 2.019e+03, 1.622e-01 ,6.656e-01, 7.119e-01, 2.654e-01,
#  4.601e-01 ,1.189e-01]]
        income = request.form.get('Income')
        hage = request.form.get('House Age')
        rooms = request.form.get('Rooms')
        bedrooms = request.form.get('Bedrooms')
        population = request.form.get('Population')
        data = [[income, hage, rooms, bedrooms,population ]]
        pred = model.predict(data)
        print(pred)
        return render_template('predict.html', result=pred)
@app.route('/machine_learning/<name>', methods=['GET', 'POST'])
def machine_learning(name):
    input_list = request.form.getlist('input_column')
    label = request.form.get('label_column')
    print(input_list)
    result = collection.find_one({"index":name})
    
    return result

if __name__ == "__main__":
    app.run(debug=True)