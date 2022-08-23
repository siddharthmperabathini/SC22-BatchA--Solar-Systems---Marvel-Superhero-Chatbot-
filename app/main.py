# import requirements needed
from flask import Flask, render_template, request, render_template_string
from utils import get_base_url
import pandas as pd
import plotly.express as px
import plotly.io as pi
import os

import numpy as np
import matplotlib.pyplot as plt
import statistics

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12222
base_url = get_base_url(port)


# ML Model setup

ml_data = pd.read_csv('./vgsales-12-4-2019.csv')
ml_data = ml_data[['Name', 'ESRB_Rating', 'Genre', 'Developer', 'Year', 'Platform']]
ml_data = ml_data.drop_duplicates(subset=['Name'], ignore_index=True)
ml_data = ml_data[~ml_data['ESRB_Rating'].isin(['EC', 'AO','RP'])]

ml_data = ml_data.dropna()
ml_data = ml_data.replace('KA', 'E10')
ml_data = ml_data.reset_index(drop=True)


def conversion(row):
    arr = ['E', 'E10', 'T', 'M']
    dic = {arr[i]: i for i in range(len(arr))}
    return dic[row['ESRB_Rating']]

def conversion2(row):
    arr = ['Education', 'Sports', 'Racing', 'Puzzle', 'Platform', 'Misc', 'Adventure',
           'Simulation', 'Party', 'Music', 'Strategy', 'Action', 'MMO', 'Fighting',
           'Role-Playing', 'Shooter', 'Visual Novel', 'Action-Adventure', 'Board Game']
    dic = {arr[i]: i for i in range(len(arr))}
    return dic[row['Genre']]

def conversion3(row):
    arr = ['Wii', 'GB', 'DS', 'X360', 'SNES', 'PS3', '3DS', 'PS2', 'NES',
       'GBA', 'PS4', 'NS', 'PC', 'N64', 'PS', 'WiiU', 'XB', 'PSP', 'GC',
       'GBC', 'XOne', 'DC', 'SAT', 'GEN', 'PSV', 'PSN', 'SCD', 'OSX',
       '3DO', 'XBL', 'DSiW', 'VC', 'WW', 'VB', 'GG', 'NGage', 'And', 'AJ',
       'Lynx', 'Linux', 'GIZ', 'Ouya', 'iOS']
    dic = {arr[i]: i for i in range(len(arr))}
    return dic[row['Platform']]


# E;   10811  <= common
# T;   6157   <= common
# M;   3314   <= common
# E10; 2897   <= uncommon
# RP;  368    <= rare
# EC;  54     <= epic
# AO;  19     <= legendary
# KA;  3      <= mythic
# note that this is the uncleaned data

ml_data['ESRB_Rating'] = ml_data.apply(lambda row : conversion(row), axis=1)
ml_data['Genre'] = ml_data.apply(lambda row : conversion2(row), axis=1)
ml_data['Platform'] = ml_data.apply(lambda row : conversion3(row), axis=1)

x = ml_data[['Genre', 'Platform', 'Year']].to_numpy()
y = ml_data['ESRB_Rating'].to_numpy()

E_idx = []
E10_idx = []
T_idx = []
M_idx = []
for i in range(len(y)):
    if y[i] == 0:
        E_idx.append(i)
    elif y[i] == 1:
        E10_idx.append(i)
    elif y[i] == 2:
        T_idx.append(i)
    elif y[i] == 3:
        M_idx.append(i)

usable_idxs = []
usable_idxs.extend(E_idx[:1600])
usable_idxs.extend(E10_idx[:1600])
usable_idxs.extend(T_idx[:1600])
usable_idxs.extend(M_idx[:1600])

new_x = []
new_y = []
for i in usable_idxs:
    new_x.append(x[i])
    new_y.append(y[i])
x = np.array(new_x)
y = np.array(new_y)
length = len(y)


idx = np.arange(length)
np.random.shuffle(idx)

split = int(length * 0.8)
traini = idx[:split]
testi = idx[split:]

trainx, trainy = x[traini], y[traini]
testx, testy = x[testi], y[testi]
trainy = trainy.reshape(-1, 1)


from sklearn.neighbors import KNeighborsClassifier

linr = KNeighborsClassifier(n_neighbors=8)
# linr = linear_model.Lasso(alpha=0.1)
linr.fit(trainx, trainy)


global out
out = 0




# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url + 'static')


# set up the routes and logic for the webserver
@app.route(f'{base_url}')
def home():
    return render_template('index.html')


# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page


@app.route(f'{base_url}/KNN_Model')
def KNN_Model():
    return render_template('pricing.html', result=out)


@app.route(f'{base_url}/Genre_Predictor')
def Genre_Predictor():
    return render_template('team2.html')


@app.route(f'{base_url}/Game_Recommender')
def Game_Recommender():
    return render_template('Game Recommender.html')


@app.route(f'{base_url}/KNN_Model', methods=['POST'])
@app.route(f'{base_url}/Genre_Predictor', methods=['POST'])
@app.route(f'{base_url}/Game_Recommender', methods=['POST'])
def my_form_post1():
    print(request.url)
    if "Game_Recommender" in request.url:
        print("POG")
        Genre = request.form['Genre']
        Platform = request.form['System']
        Rating = request.form['Rating']

        data = pd.read_csv('vgsales.csv')

        data = data[data['ESRB_Rating'].notna()]
        data = data[data['ESRB_Rating'].isin(['E', 'E10', 'T', 'M'])]


        # 1
        E_col = []
        score = []
        rating = []
        genre_list = []
        system = []
        E_games = data[data['ESRB_Rating'] == Rating]
        E_COL = []
        for i in range(0, 100):
            names = E_games[E_games['Critic_Score'] == i/10]

            if Genre != 'any':
                names = names[names['Genre'] == Genre]
            if Platform != 'any':
                names = names[names['Platform'] == Platform]

            names = names['Name'].to_numpy()

            if len(names) > 0:
                genre_list.append(Genre)
                rating.append(Rating)
                system.append(Platform)
                string = ''
                for i in range(len(names)):
                    string += str(names[i]) + ", "
                    if i % 10:
                        string += '<br>'
                E_col.append(string)
                score.append(i/10)

        test_df = pd.DataFrame({'Score': score, 'Rating': rating,'Games': E_col})

        fig = px.scatter(test_df, x='Rating' , y='Score',hover_data=['Games'], title = "Critic Score /10 to ERSB Rating")




        # 2
        E_col = []
        score = []
        rating = []
        genre_list = []
        for i in range(0, 100):
            names = E_games[E_games['User_Score'] == i/10]

            if Genre != 'any':
                names = names[names['Genre'] == Genre]
            if Platform != 'any':
                names = names[names['Platform'] == Platform]
            names = names['Name'].to_numpy()
            if len(names) > 0:
                system.append(Platform)
                genre_list.append(Genre)
                rating.append(Rating)
                score.append(i/10)
                string = ''
                for i in range(len(names)):
                    string += str(names[i]) + ", "
                    if i % 10:
                        string+='<br>'
                E_col.append(string)

        test3 = pd.DataFrame({'Score': score, 'Rating': rating, 'Games': E_col})

        fig3 = px.scatter(test3, x='Rating' , y='Score', hover_data=['Games'], title = "User Score /10 to ERSB Rating")



        # 3
        E_col = []
        score = []
        rating = []
        genre_list = []
        Total = []
        for i in range(0, 100):
            names = E_games[E_games['Critic_Score'] == i/10]

            if Genre != 'any':
                names = names[names['Genre'] == Genre]
            if Platform != 'any':
                names = names[names['Platform'] == Platform]
            names = names['Name'].to_numpy()
            if len(names) > 0:
                system.append(Platform)
                genre_list.append(Genre)
                rating.append(Rating)
                string = ''
                for i in range(len(names)):
                    string += str(names[i]) + ", "
                    if i % 10:
                        string+='<br>'
                E_col.append(string)
                Total.append(i)
        test2 = pd.DataFrame({'Rating': rating, 'Games': E_col, 'Total' : Total})

        fig2 = px.scatter(test2, x='Rating' , y='Total',hover_data=['Games'], title = "ESRB Rating to Global Sales(Millions)")
        

        
        fig.write_html("templates/t1_user_fig.html")
        fig2.write_html("templates/t1_user_fig2.html")
        fig3.write_html("templates/t1_user_fig3.html")
        
        return render_template('Game Recommender.html')

# document.getElementById('iframeid').src += '';

    
    
    
    
    elif "Genre_Predictor" in request.url:
        print('haha')
        Region = request.form['Region']
        Year = request.form['Year']
        Publisher = request.form['Publisher']
        Year = int(Year)
       

        t2data = pd.read_csv('./vgsales-12-4-2019.csv')

        #Make a list of what you want to drop
        columns_to_drop_vgsales = ['Rank', 'ESRB_Rating', 'Platform', 'Developer', 'VGChartz_Score', 'Critic_Score', 'Last_Update', 'Vgchartzscore', 'status', 'img_url', 'url', 'Name', 'basename', 'User_Score']

        #Drop the columns using drop()
        t2data.drop(columns_to_drop_vgsales, axis=1, inplace = True) #axis = 1 lets pandas know we are dropping columns, not rows.

        #Drop NAN values
        t2data = t2data[t2data[Region].notna()]
        t2data = t2data[t2data['Genre'].notna()]
        t2data = t2data[t2data['Year'].notna()]
        t2data = t2data[t2data['Publisher'].notna()]
        t2data = t2data[t2data['Year'] == Year]
        t2data = t2data[t2data['Publisher'] == Publisher]

        fig = px.scatter(t2data, x="Genre", y=Region, color="Genre", title="Your Data From Inputs", hover_data=['Genre', 'Publisher'])
        
        try:
            os.remove("templates/usergraph.html")
        except:
            print("File not found")
        fig.write_html("templates/usergraph.html")
        

        print(Region, Year, Publisher)
        # return render_template_string(pi.to_html(fig))
        return render_template('team2.html')
    
    elif "KNN_Model" in request.url:
        print("Test")
        
        Platform = request.form['Platform1']
        Year = int(request.form['Year1'])
        Genre = request.form['Genre1']
        
        rating_key = ['E', 'E10', 'T', 'M']
        
        genre_arr = ['Education', 'Sports', 'Racing', 'Puzzle', 'Platform', 'Misc', 'Adventure',
           'Simulation', 'Party', 'Music', 'Strategy', 'Action', 'MMO', 'Fighting',
           'Role-Playing', 'Shooter', 'Visual Novel', 'Action-Adventure', 'Board Game']
        genre_key = {genre_arr[i]: i for i in range(len(genre_arr))}
        
        platform_arr = ['Wii', 'GB', 'DS', 'X360', 'SNES', 'PS3', '3DS', 'PS2', 'NES',
       'GBA', 'PS4', 'NS', 'PC', 'N64', 'PS', 'WiiU', 'XB', 'PSP', 'GC',
       'GBC', 'XOne', 'DC', 'SAT', 'GEN', 'PSV', 'PSN', 'SCD', 'OSX',
       '3DO', 'XBL', 'DSiW', 'VC', 'WW', 'VB', 'GG', 'NGage', 'And', 'AJ',
       'Lynx', 'Linux', 'GIZ', 'Ouya', 'iOS']
        platform_key = {platform_arr[i]: i for i in range(len(platform_arr))}
        
        Platform = platform_key[Platform]
        Genre = genre_key[Genre]
        
        lst = [Platform, Genre, Year]
        out = linr.predict([lst])
        
        out = rating_key[out[0]]
        return render_template("pricing.html", result=out)

@app.route(f'{base_url}/render_fig1')
def render_fig1():
    return render_template('usergraph.html')


@app.route(f'{base_url}/render_fig')
def render_fig():
    return render_template('t1_user_fig.html')

@app.route(f'{base_url}/render_fig3')
def render_fig3():
    return render_template('t1_user_fig3.html')

@app.route(f'{base_url}/render_fig2')
def render_fig2():
    return render_template('t1_user_fig2.html')
        
    

@app.route(f'{base_url}/render_result')
def render_result():
    i = 2
    return render_template_string(f"<html><body><p>2</p></body></html>")
    
if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc5.ai-camp.dev'

    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)
