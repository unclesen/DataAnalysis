from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

import csv, re, operator
# from textblob import TextBlob

app = Flask(__name__)

person = {
    'name':'彭佳诚',
    'address' : '中国',
    'job': '预备游戏设计师',
    'tel': '199999999',
    'email': 'JC@gmail.com',
    'description' : '彭佳诚（JiaCheng Peng），2000年6月3日出生于中国大陆，中国男大学生。2018年，彭佳诚开始学习软件工程，他在中国某大学中学习3年。2021年，彭佳诚作为中国某大学学生代表参加了第N届知名毕业设计，暂未获得名次。2021年之后，计划将自己的天赋带到游戏编程，目前在一个人自学unity。预计2030年，彭佳诚与某绘画专业同学合作的3d开放大世界追逐交互ARPG游戏《*******》上映，这也是彭佳诚第一部游戏作品',
    'social_media' : [
        {
            'link': 'https://www.facebook.com/nono',
            'icon' : 'fa-facebook-f'
        },
        {
            'link': 'https://github.com/nono',
            'icon' : 'fa-github'
        },
        {
            'link': 'linkedin.com/in/nono',
            'icon' : 'fa-linkedin-in'
        },
        {
            'link': 'https://twitter.com/nono',
            'icon' : 'fa-twitter'
        }
    ],
    'img': 'img/img_statham.jpg',
    'experiences' : [
        {
            'Project' : '基于C语言的人力管理系统开发',
            'teacher': '指导老师:陈**',
            'timeframe' : '2019'
        },
        {
            'Project' : '基于JavaWeb的商城购物功能设计',
            'teacher': '指导老师:杨*',
            'timeframe' : '2020'
        },
        {
            'Project' : 'Python数据分析',
            'teacher': '指导老师:李**',
            'timeframe' : '2020'
        },
        {
            'Project' : '基于pygame的飞机大战小游戏设计与开发',
            'teacher': '指导老师:李**',
            'timeframe' : '2021'
        }
    ],
    'educations' : [
        {
            'education': ' 小学 ',
            'time': '2006-2012'
        },
        {
            'education': '初中',
            'time': '2012-2015'
        },
        {
            'education': '高中 ',
            'time': '2015-2018'
        },
        {
            'education': '大学 ',
            'time': '2021-现在'
        }
    ],
    'programming_languages' : {
        'HMTL' : ['fa-html5', '100'], 
        'CSS' : ['fa-css3-alt', '100'], 
        'SASS' : ['fa-sass', '90'], 
        'JS' : ['fa-js-square', '90'],
        'Wordpress' : ['fa-wordpress', '80'],
        'Python': ['fa-python', '70'],
        'Mongo DB' : ['fa-database', '60'],
        'MySQL' : ['fa-database', '60'],
        'NodeJS' : ['fa-node-js', '50']
    },
    'languages' : {'French' : 'Native', 'English' : 'Professional', 'Spanish' : 'Professional', 'Italian' : 'Limited Working Proficiency'},
    'interests' : ['Dance', 'Travel', 'Languages']
}

@app.route('/')
def cv(person=person):
    return render_template('index.html', person=person)




@app.route('/callback', methods=['POST', 'GET'])
def cb():
	return gm(request.args.get('data'))
   
@app.route('/chart')
def index():
	return render_template('chartsajax.html',  graphJSON=gm(),graphJSON2=gm1_2(),graphJSON3=gm1_3(),graphJSON4=gm1_4(),graphJSON5=gm1_5())

@app.route('/chart2')
def index2():
    return render_template('chart2.html',  graphJSON=gm2_1(),graphJSON2=gm2_2(),graphJSON3=gm2_3(),graphJSON4=gm2_4(),graphJSON5=gm2_5())

def gm(Country='Italy'):
	df = pd.read_csv('./GREEN500.csv')

	fig = px.line(df[df['Country']==Country], x="Year", y="Total Cores")

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

def gm1_2():
    df = pd.read_csv('./GREEN500.csv')

    fig2 = px.scatter(df, x="TOP500 Rank", y="Rmax [TFlop/s]", color="Country", 
           marginal_y="rug", marginal_x="histogram")

    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON2

def gm1_3():
    df = pd.read_csv('./GREEN500.csv')

    fig3 = px.bar(df, x="Power Quality Level", y="Power Efficiency [GFlops/Watts]", color="Manufacturer")

    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON3

def gm1_4():
    df = pd.read_csv('./GREEN500.csv')

    fig4 = px.area(df, x="TOP500 Rank", y="Rpeak [TFlop/s]", color="Continent")

    graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON4

def gm1_5():
    df = pd.read_csv('./GREEN500.csv')

    fig5 = px.strip(df, x="TOP500 Rank", y="Rpeak [TFlop/s]", orientation="h", color="Operating System")

    graphJSON5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON5

def gm2_1():
    df = pd.read_csv('./water_potability.csv')

    # fig = px.scatter(df,x="ph", y="Potability")
    # fig = px.line(df,x="ph", y="Potability")
    fig = px.histogram(df,x="ph", y="Turbidity" , color="Potability")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def gm2_2():
    df = pd.read_csv('./water_potability.csv')

    # fig = px.scatter(df,x="ph", y="Potability")
    # fig = px.line(df,x="ph", y="Potability")
    # fig = px.histogram(df,x="ph", y="Turbidity" , color="Potability")
    fig2 = px.histogram(df,x="Sulfate", y="Conductivity" , color="Potability")

    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON2
    fig = px.pie(fruit,names="name",values="number")

def gm2_3():
    df = pd.read_csv('./water_potability.csv')

    fruit = pd.DataFrame({
        "name":["100-150","150-200","200-250","250-300","300-999"],
        "number":[
        len(df[(df['Hardness']>=100) & (df['Hardness']<150)]), \
        len(df[(df['Hardness']>=150) & (df['Hardness']<200)]), \
        len(df[(df['Hardness']>=200) & (df['Hardness']<250)]), \
        len(df[(df['Hardness']>=250) & (df['Hardness']<300)]), \
        len(df[(df['Hardness']>=300)])
        ]})

    fig3 = px.pie(fruit,names="name",values="number")

    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON3

def gm2_4():
    df = pd.read_csv('./water_potability.csv')

    fruit = pd.DataFrame({
        "name":["0-250","250-290","290-330","330-999"],
        "number":[
        len(df[(df['Sulfate']>= 0 ) & (df['Sulfate']<250)]), \
        len(df[(df['Sulfate']>=250) & (df['Sulfate']<290)]), \
        len(df[(df['Sulfate']>=290) & (df['Sulfate']<330)]), \
        len(df[(df['Sulfate']>=330) & (df['Sulfate']<999)])
        ]})

    fig4 = px.pie(fruit,names="name",values="number")

    graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON4

def gm2_5():
    df = pd.read_csv('./water_potability.csv')

    fig5 = px.scatter(df,x="Solids",y="Chloramines")

    graphJSON5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON5


@app.route('/senti')
def main():
	text = ""
	values = {"positive": 0, "negative": 0, "neutral": 0}

	with open('ask_politics.csv', 'rt') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
		for idx, row in enumerate(reader):
			if idx > 0 and idx % 2000 == 0:
				break
			if  'text' in row:
				nolinkstext = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', row['text'], flags=re.MULTILINE)
				text = nolinkstext

			blob = TextBlob(text)
			for sentence in blob.sentences:
				sentiment_value = sentence.sentiment.polarity
				if sentiment_value >= -0.1 and sentiment_value <= 0.1:
					values['neutral'] += 1
				elif sentiment_value < 0:
					values['negative'] += 1
				elif sentiment_value > 0:
					values['positive'] += 1

	values = sorted(values.items(), key=operator.itemgetter(1))
	top_ten = list(reversed(values))
	if len(top_ten) >= 11:
		top_ten = top_ten[1:11]
	else :
		top_ten = top_ten[0:len(top_ten)]

	top_ten_list_vals = []
	top_ten_list_labels = []
	for language in top_ten:
		top_ten_list_vals.append(language[1])
		top_ten_list_labels.append(language[0])

	graph_values = [{
					'labels': top_ten_list_labels,
					'values': top_ten_list_vals,
					'type': 'pie',
					'insidetextfont': {'color': '#FFFFFF',
										'size': '14',
										},
					'textfont': {'color': '#FFFFFF',
										'size': '14',
								},
					}]

	layout = {'title': '<b>意见挖掘</b>'}

	return render_template('sentiment.html', graph_values=graph_values, layout=layout)


if __name__ == '__main__':
  app.run(debug= True,port=5000,threaded=True)
