#https://www.kaggle.com/omarhanyy/500-greatest-songs-of-all-time
#This dataset was scraped from www.rollingstone.com by Omar Hany and uploaded to Kaggle
#Interesting graph could be a bar chart of each artists and how many songs they had on the list 
#Another could be a histogram of the streak column, which shows how long the song stayed on the charts 

import pandas as pd, re, json, requests
from pandas import DataFrame, read_csv
from flask import Flask, request, jsonify, request, render_template 
from bs4 import BeautifulSoup
from markupsafe import escape

app = Flask(__name__)
df = pd.read_csv("main.csv")
n = 0 
visited = 0
a = 0
b = 0
first_visited = None 
color = None
count_a = 0 
count_b = 0

@app.route('/')
def home():
    global visited
    global a 
    global b 
    if visited < 10:
        if visited % 2 == 0:         
            with open("index.html") as f:        
                html = f.read()
                html = html.format("?from=A","'Color:red'")
                visited += 1 
            return html

        else:         
            with open("index.html") as f:        
                html = f.read()
                html = html.format("?from=B","'Color:green'")
                visited += 1
            return html 
    else:
        if count_a > count_b:
            with open("index.html") as f:        
                html = f.read()
                html = html.format("?from=A","'Color:red'")
            return html 
        else:
            with open("index.html") as f:        
                html = f.read()
                html = html.format("?from=B","'Color:green'")
            return html     
        
@app.route('/donate.html')
def donations_page():
    global visited
    global first_visited
    global color 
    global count_a
    global count_b
    if visited:
        ref = request.url
        ref = ref[31:]
        first_visited = ref
        if first_visited == "?from=A":
            count_a += 1 
        else:
            count_b += 1 
        return "<html><h1>{}</h1>{}<html>".format("Donate", "Please Donate - It's for a GOOD Cause") 

@app.route('/browse.html')
def browse_page():
    browse_df = df.to_html(classes="df", header = "True", table_id = "Browse")
    return "<html><h1>{}</h1>{}<html>".format("Browse", browse_df)

@app.route('/email', methods=["POST"])
def email():
    global n 
    email = str(request.data, "utf-8")
    suffix = r"\.(edu|com|org|net|io)"
    at = r"@"
    if re.match(r"(\w+)\s*" + at  + r"\s*(\w+)" + suffix, email): # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") 
            n += 1                         
        return jsonify("thanks, you're subscriber number {}!".format(n))
    return jsonify("quit being so careles!!!!") 

@app.route('/api.html')
def api_page():
    return """<html><h1>{}</h1><h3>To get column information, do this:</h3>
            <p1><pre>/topsongscols.json</pre>
            </p2><h3>To get all top 500 greatest songs, use this endpoint:</h3>
            <p1><pre>/topsongs.json</pre></p2>
            <h3>To get songs charting over 10 weeks, use this endpoint:</h3>
            <p1><pre>/topsongs.json?artist=U2</pre></p2><html>""".format("API")

#https://stackoverflow.com/questions/41087887/is-there-a-way-to-generate-the-dtypes-as-a-dictionary-in-pandas
#Apply function copied from stack exchange link above
@app.route('/topsongscols.json')
def top_songs_cols_page():
    global df 
    dic = df.dtypes.apply(lambda x: x.name).to_dict()
    return jsonify(dic)
 
#example in api is Artist = U2    
@app.route('/topsongs.json')
def top_songs_page():
    list_containing_artist = []
    if "artist" not in request.args:
        return jsonify(df.to_dict("records"))
    else:
        for row in df.loc[df["artist"] == "U2"].to_dict("index"):
            times_in_dataset = [row, df.loc[df["artist"] == "U2"].to_dict("index")]
            list_containing_artist.append(times_in_dataset)                                             
        return jsonify(list_containing_artist)
         
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True) # don't change this line!
    
# THE SOURCE OF MY DATA WAS KAGGLE, WHICH WAS UPLOADED BY OMAR HANY AND SCRAPED FROM WWW.ROLLINGSTONE.COM
