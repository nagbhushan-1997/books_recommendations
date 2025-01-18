from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

popular_df = pickle.load(open('E:\\ML_Projects\\book_recommendation_system\\popular.pkl', 'rb'))  
pt = pickle.load(open('E:\\ML_Projects\\book_recommendation_system\\pt.pkl', 'rb'))
book_dict = pickle.load(open('E:\\ML_Projects\\book_recommendation_system\\books.pkl', 'rb')) 
cosine_sim = pickle.load(open('E:\\ML_Projects\\book_recommendation_system\\similarity_score.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', book_name = list(popular_df['Book-Title'].values), author_name = list(popular_df['Book-Author'].values), image_url = list(popular_df['Image-URL-M'].values), votes = list(popular_df['num_ratings'].values), ratings = list(popular_df['avg_rating'].values))


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommendations():
    user_input = request.form.get('user_input')
    # index fetch
    index = np.where(pt.index ==user_input)[0][0]
    similar_items = sorted(list(enumerate(cosine_sim[index])),key=lambda x:x[1], reverse=True)[1:6]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = book_dict[book_dict['Book-Title']== pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    print(data)
    
    return render_template('recommend.html', data = data)
    
if __name__ == '__main__':
    app.run(debug=True)