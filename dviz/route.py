import pandas as pd
import operator
import json
from flask import jsonify, request, render_template, url_for
from dviz import app

# initialize data

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
df['시'] = df['시'].map(lambda x: "광주광역시" if x == "광주" else x)
df['시'] = df['시'].map(lambda x: "대전광역시" if x == "대전" else x)
print("df load done!")


@app.route('/')
def google_pie_chart():

	return render_template('index.html.j2')

@app.route('/year')
def year():
    myyear=[]
    yr = (2012,2013,2014,2015,2016,2017,2018)
    for i in yr:
        tmp = [i, df[df['사고년도']==i].shape[0], df[df['사고년도']==i].sum()['사망자수']]
        myyear.append(tmp)

    return render_template('year.html.j2', year_cnt=myyear)
    
@app.route('/district')
def index():

    tmp = {}
    for i in range(10365):
        if df.iloc[i]['시'] in tmp:
            tmp[df.iloc[i]['시']] += int(df.iloc[i]['사상자수'])
        else:
            tmp[df.iloc[i]['시']] = int(df.iloc[i]['사상자수'])
    tmp = sorted(tmp.items(), key=operator.itemgetter(1), reverse=True)

    data={}
    data['header'] ="교통사고 사망자수"
    for i in tmp:
        data[i[0]]=i[1]
        
    return render_template('district.html.j2', data=data)

@app.route('/type')
def typeofaccident():
    accident_type = ['스쿨존어린이', '보행어린이', '보행노인', '자전거', '무단횡단']
    count = df['사고유형구분'].value_counts()
    
    tmp = {}
    for i in accident_type:
        tmp[i] = [count[i], df[df['사고유형구분']==i].sum()['사망자수']]
    tmp = sorted(tmp.items(), key=operator.itemgetter(1), reverse=True)
    
    type_data={}
    death_cnt={}
    type_data['header'] = "교통사고 종류"
    for i in tmp:
        type_data[i[0]]=i[1]
        death_cnt[i[0]]=i[1]


    return render_template('type.html.j2', type_data=type_data, death_cnt = death_cnt)
