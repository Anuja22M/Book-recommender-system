from flask import Flask,render_template,request
import pandas as pd
import numpy as np

popular1_df = pd.read_csv(r'D:\Final_year_project\book-recommender-system-master\popular1_df.csv')
pt = pd.read_csv(r'D:\Final_year_project\book-recommender-System-master\pt.csv', index_col=0)
books = pd.read_csv(r'D:\Final_year_project\book-recommender-System-master\books.csv')
similarity_scores_df = pd.read_csv(r'D:\Final_year_project\book-recommender-System-master\similarity_score.csv', index_col=0)
similarity_score = similarity_scores_df.to_numpy()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular1_df['Book-Title'].values),
                           author=list(popular1_df['Book-Author'].values),
                           image=list(popular1_df['Image-URL-M'].values),
                           votes=list(popular1_df['num_ratings'].values),
                           rating=list(popular1_df['avg_ratings'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)