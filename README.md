# 📚 Book Recommendation System

An intelligent, interactive book recommendation web app combining traditional collaborative filtering and modern AI (LLM) techniques to deliver personalized suggestions.

## 🚀 Features

- 🔥 **Popular Book Display** – Showcases trending books on the homepage.
- 🔍 **Collaborative Filtering Recommendations** – Suggests similar books based on user-selected titles.
- 🤖 **AI-Powered GPT Search** – Uses large language models to generate recommendations from natural language prompts.
- 🌐 **Web Interface** – Built with HTML, CSS and Bootstrap for a responsive UI.
- 📈 **Hybrid System** – Combines static data-driven filtering and dynamic AI responses.

## 🧠 Powered by
- **SambaNova**'s LLM model: `Llama-4-Maverick-17B-128E-Instruct`
- OpenAI-compatible API integration
- Pandas, NumPy, Flask, Sklearn, Google Colab.

---

## 🗂️ Project Structure
📁 project/
├── app.py # Main Flask web app


├── Book_Recommendation_ML.ipynb # Main ML logic that calculates similarity_score


├── gpt_search.py # GPT-powered recommendation logic


├── books.csv # Book metadata


├── pt.csv # Pivot table for collaborative filtering


├── popular1_df.csv # Precomputed popular books


├── similarity_score.csv # Similarity matrix for collaborative filtering


├── templates/


│ ├── index.html


│ ├── recommend.html


│ ├── gpt.html


│ └── gpt_search.html


├── .env # Environment variables (not committed)


└── README.md # You're here!







🟢Create and Activate a Virtual Environment(in Git-Bash)
python -m venv venv
source venv/Scripts/activate

📘Install Dependencies
pip install -r requirements.txt

🔖Set Environment Variables
Create a .env file in the root directory with:
SAMBANOVA_API_KEY=your_api_key_here
SAMBANOVA_BASE_URL=https://your-sambanova-endpoint.com/v1

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




GPT AI Assistant (/gpt_recommends) – Describe a genre, theme, or book and get AI-curated suggestions.

<img width="1783" height="904" alt="image" src="https://github.com/user-attachments/assets/dd0e8a7f-11b0-4b19-9314-d1077f4a948a" />














