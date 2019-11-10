import pandas as pd
import json
from flask import jsonify, request, render_template, send_file
from dviz import app

@app.route('/')
def google_pie_chart():
	data = {'Task' : 'Hours per Day', 'Work' : 11, 'Eat' : 55, 'Commute' : 2, 'Watching TV' : 2, 'Sleeping' : 7}
	#print(data)

	return render_template('index.html.j2', data=data)
    
@app.route('/data')
def index():
    df = pd.read_csv("./data.csv", engine='python')
    df['시'] = df['시도시군구명'].map(lambda x: x.split(' ')[0])
    df['시'] = df['시'].map(lambda x: "경기도" if x == "경기" else x)
    df['시'] = df['시'].map(lambda x: "강원도" if x == "강원" else x)
    df['시'] = df['시'].map(lambda x: "서울특별시" if x == "서울" else x)
    df['시'] = df['시'].map(lambda x: "부산광역시" if x == "부산" else x)
    df['시'] = df['시'].map(lambda x: "인천광역시" if x == "인천" else x)
    df['시'] = df['시'].map(lambda x: "경상북도" if x == "경북" else x)
    df['시'] = df['시'].map(lambda x: "경상남도" if x == "경남" else x)
    df['시'] = df['시'].map(lambda x: "제주특별자치도" if x == "제주" else x)
    df['시'] = df['시'].map(lambda x: "전라남도" if x == "전남" else x)
    df['시'] = df['시'].map(lambda x: "전라북도" if x == "전북" else x)
    df['시'] = df['시'].map(lambda x: "충청북도" if x == "충북" else x)
    df['시'] = df['시'].map(lambda x: "충청남도" if x == "충남" else x)


    df2 = df.iloc[:5000]
    mydata = {}
    mydata['header'] ="교통사고 사망자수"
    for i in range(5000):
        if df2.iloc[i]['시'] in mydata:
            mydata[df2.iloc[i]['시']] += int(df2.iloc[i]['사상자수'])
        else:
            mydata[df2.iloc[i]['시']] = int(df2.iloc[i]['사상자수'])
    
    return render_template('data.html.j2', data=mydata)
    