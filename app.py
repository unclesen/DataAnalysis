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
    return render_template('index2.html', person=person)




@app.route('/callback', methods=['POST', 'GET'])
def cb():
	return gm(request.args.get('data'))
   
@app.route('/chart')
def index():
	return render_template('chartsajax.html',  graphJSON=gm())

def gm(country='United Kingdom'):
	df = pd.DataFrame(px.data.gapminder())

	fig = px.line(df[df['country']==country], x="year", y="gdpPercap")

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON


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
