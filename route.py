import pandas as pd
import operator
import json
from flask import jsonify, request, render_template, url_for
from flask import Flask

app = Flask(__name__)
df = pd.read_csv("data.csv", engine='python', encoding='utf-8-sig')

@app.route('/')
def front():

    index1 = list(df.groupby('발생시').count()['주야'].index)
    value1 = list(df.groupby('발생시').count()['주야'])
    overall=[]
    for i in range(len(index1)):
        overall.append([index1[i], value1[i]])

    index2=(df[df['법규위반']=='과속'].groupby('발생시').count()['주야'].index)
    value2=(df[df['법규위반']=='과속'].groupby('발생시').count()['주야'])
    speeding=[]
    for i in range(len(index2)):
        speeding.append([index2[i], value2[i]])

    index3=(df[df['법규위반']=='신호위반'].groupby('발생시').count()['주야'].index)
    value3=(df[df['법규위반']=='신호위반'].groupby('발생시').count()['주야'])
    signal=[]
    for i in range(len(index3)):
        signal.append([index3[i], value3[i]])


    index4=(df[df['법규위반']=='보행자 보호의무 위반'].groupby('발생시').count()['주야'].index)
    value4=(df[df['법규위반']=='보행자 보호의무 위반'].groupby('발생시').count()['주야'])
    pedestrian=[]
    for i in range(len(index4)):
        pedestrian.append([index4[i], value4[i]])

    index5=(df[df['법규위반']=='중앙선 침범'].groupby('발생시').count()['주야'].index)
    value5=(df[df['법규위반']=='중앙선 침범'].groupby('발생시').count()['주야'])
    center=[]
    for i in range(len(index5)):
        center.append([index5[i], value5[i]])

    every=[]
    for i in range(len(index2)):
        every.append([index2[i], value2[i], value3[i], value4[i], value5[i]])


    key = (df.groupby('법규위반').count()['주야'].index)
    val = (df.groupby('법규위반').count()['주야'])
    type = []
    for i in range(len(key)):
        if key[i] == '안전운전 의무 불이행':
            continue
        type.append([key[i], val[i]])

    return render_template('line.html.j2',overall=overall, speeding=speeding, signal=signal,center=center, every=every, type=type)

@app.route('/day')
def day():
    day = ['월','화','수','목','금','토','일']
    data =[]
    for i in day:
        noon = df[((df['주야']=='주')|(df['주야']=='주간'))&(df['요일']==i)].count()['주야']
        night = df[((df['주야']=='야')|(df['주야']=='야간'))&(df['요일']==i)].count()['주야']
        data.append([i, night, noon])

    return render_template('day.html.j2', data=data)


@app.route('/tree')
def tree():
    data = []
    for car in df['피해자_당사자종별_대분류'].unique():
        if car =='00':
            continue
        data.append([car, 'global', 0 , 0])

    for car in df['피해자_당사자종별_대분류'].unique():
        if car =='00':
            continue
        index = list(df[df['피해자_당사자종별_대분류']==car].groupby('사고유형').count()['주야'].index)
        index_named = list(df[df['피해자_당사자종별_대분류']==car].groupby('사고유형').count()['주야'].index.map(lambda x: car+'_'+x))
        df2 = df[df['피해자_당사자종별_대분류']==car].groupby('사고유형').count()['주야']
        for i, index in enumerate(index):
            casualty = df[(df['피해자_당사자종별_대분류']==car)&(df['사고유형']==index)].mean()['사상자수']
            
            data.append([index_named[i], car ,df2[index], casualty])
    return render_template('tree.html.j2', data=data)
    