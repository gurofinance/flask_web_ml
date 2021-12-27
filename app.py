from flask import Flask , request , render_template ,Response, request, redirect
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import random
import io
from pymongo import MongoClient

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


if __name__ == "__main__":
    app.run(debug=True)