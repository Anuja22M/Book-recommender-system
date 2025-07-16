# 📚 Book Recommendation System

An interactive book recommendation web app created using traditional collaborative filtering techniques to deliver personalized suggestions.

## 🚀 Features

- 🔥 **Popular Book Display** – Showcases trending books on the homepage.
- 🔍 **Collaborative Filtering Recommendations** – Suggests similar books based on user-selected titles.
- 🌐 **Web Interface** – Built with HTML, CSS and Bootstrap for a responsive UI.
- 📈 **Hybrid System** – Combines static data-driven filtering.

## 🧠 Powered by
- Pandas, NumPy, Flask, Sklearn, Google Colab.

## 🗂️ Project Structure
📁 project/
├── app.py # Main Flask web app


├── Book_Recommendation_ML.ipynb # Main ML logic that calculates similarity_score


├── books.csv # Book metadata


├── pt.csv # Pivot table for collaborative filtering


├── popular1_df.csv # Precomputed popular books


├── similarity_score.csv # Similarity matrix for collaborative filtering


├── templates/


│ ├── index.html


│ ├── recommend.html


│ └── gpt_search.html


└── README.md # You're here!



💻 Run the Application
flask run
Visit http://127.0.0.1:5000 in your browser.


✨ Usage
Home (/) – Displays 50 popular books.

<img width="1796" height="873" alt="image" src="https://github.com/user-attachments/assets/c609c715-2286-4ee0-b897-98bd26d04570" />




Collaborative Filtering (/recommend) – Enter a book name to get similar ones.

<img width="1062" height="585" alt="image" src="https://github.com/user-attachments/assets/c84bc161-ff1e-49f4-a7ed-8b03c150672a" />



After **Collaborative Filtering** (/recommend_books) 

<img width="1760" height="859" alt="image" src="https://github.com/user-attachments/assets/cff2278a-dd41-4581-9f6e-faf354d4c202" />


🔖Future Thoughts: - 
🤖 **AI-Powered GPT Search** – Uses large language models to generate recommendations from natural language prompts.








