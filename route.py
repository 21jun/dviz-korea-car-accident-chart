import pandas as pd
import operator
import json
from flask import jsonify, request, render_template, url_for
from flask import Flask

app = Flask(__name__)
df = pd.read_csv("data.csv", engine='python', encoding='utf-8-sig')


@app.route('/test')
def test():

    data = []
    for i in range(3657):
        a, b, c = df[df['발생년']==2018][['위도','경도','사망자수']].iloc[i]
        data.append([a, b, c])

    return render_template('test.html.j2', data=data)

@app.route('/all')
def deckgl():

    data = []
    select = df[['경도','위도']]
    for i in range(len(select)):
        a, b = select.iloc[i]
        data.append([a, b])

    return render_template('all.html.j2', data=data)

@app.route('/walk')
def walk():
    
    """
    보행자_type 인코딩
    (array([0, 1, 2, ..., 2, 0, 1], dtype=int64),
    Index(['기타', '차도통행중', '횡단중', '길가장자리구역통행중', '보도통행중'], dtype='object'))
    """
    data = []
    df2 = df[df['피해자_당사자종별_대분류']=='보행자']
    df2['보행자_type'] = pd.factorize(df[df['피해자_당사자종별_대분류']=='보행자']['사고유형_중분류'])[0]
    select = df2[['경도','위도', '보행자_type']]
    for i in range(len(select)):
        a, b , c = select.iloc[i]
        if c != 0:
            data.append([a, b, c])

    return render_template('walk.html.j2', data=data)


@app.route('/dayandnight')
def nigth():
    """
    Index(['야간', '주간']
    """
    data = []
    df['주야']=df['주야'].map(lambda x: "주간" if x == '주' else x)
    df['주야']=df['주야'].map(lambda x: "야간" if x == '야' else x)
    df['주야_type'] = pd.factorize(df['주야'])[0]
    select =  df[['경도','위도','주야_type']]
    for i in range(len(select)):
        a, b, c = select.iloc[i]
        data.append([a, b, c])

    return render_template('walk.html.j2', data=data)

@app.route('/day')
def day():

    data = []
    select = df[(df['주야']=='주')|(df['주야']=='주간')][['경도','위도']][['경도','위도']]
    for i in range(len(select)):
        a, b = select.iloc[i]
        data.append([a, b])

    return render_template('day_map.html.j2', data=data)
