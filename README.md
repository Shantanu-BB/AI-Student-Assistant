# 🎓 AI Student Assistant

**Learn Artificial Intelligence through conversation.**

AI Student Assistant is a web-based chatbot that acts as a friendly AI tutor for beginners. Students can ask questions about Artificial Intelligence and receive simple, example-based explanations powered by Google Gemini.

![App Screenshot](assets/screenshot.png)

## 📖 Project Description

I built this project after completing an Introduction to Artificial Intelligence course. It turns what I learned into a practical app: a chatbot that explains AI concepts in plain language, gives examples, and helps students understand instead of just giving answers.

## ✨ Features

- Clean, modern, student-friendly chat interface
- Chat history maintained during the session
- Clickable example questions when the chat is empty
- Loading indicator while the AI is responding
- "Clear Chat" button
- Sidebar with project info and technologies used
- Friendly error messages (missing API key, invalid key, network problems, quota limits)
- API key stored safely in `.env` and never exposed in the browser
- Responsive layout for desktop and mobile

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – web interface
- **Google Gemini API** (`google-genai` SDK) – AI responses
- **python-dotenv** – loads the API key from `.env`

## ⚙️ How the Chatbot Works

1. The student types a question (or clicks an example question).
2. Streamlit stores the message in the session's chat history.
3. The full conversation, plus a "friendly AI tutor" system prompt, is sent to the Gemini API.
4. Gemini generates a beginner-friendly answer.
5. The answer is displayed in the chat and added to the history.

The API key is read on the server from the `.env` file, so it is never visible in the browser.

## 📁 Project Structure

```
ai-student-assistant/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Template for environment variables
├── .gitignore          # Files Git should ignore (includes .env)
├── README.md           # Project documentation
└── assets/             # Screenshots and images
```

## 🚀 Installation

1. **Install Python 3.9+** from https://www.python.org/downloads/
2. **Unzip** the project and open the folder in a terminal (or in VS Code).
3. **(Recommended) Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🔑 Gemini API Key Setup

1. Go to [Google AI Studio](https://aistudio.google.com/apikey) and sign in with your Google account.
2. Click **Create API key** and copy it.
3. In the project folder, copy `.env.example` and rename the copy to `.env`.
4. Open `.env` and replace `your_api_key_here` with your real key:
   ```
   GEMINI_API_KEY=your_real_key_here
   ```
5. Save the file. **Never share or upload your `.env` file.**

## ▶️ Run the Application

```bash
streamlit run app.py
```

Your browser will open at `http://localhost:8501`.

## 💬 Example Questions

- What is Artificial Intelligence?
- What is Machine Learning?
- Explain supervised and unsupervised learning.
- What is Deep Learning?
- What is NLP?
- Give a simple example of a neural network.
- Explain AI in simple words.

## 🔮 Future Improvements

- Streaming responses (text appears word by word)
- Download chat as a text file
- Quiz mode to test understanding
- Difficulty levels (beginner / intermediate)
- Dark/light theme toggle
- Deploy online with Streamlit Community Cloud

## 👤 Author

**Your Name**
GitHub: [github.com/your-username](https://github.com/your-username)
LinkedIn: [linkedin.com/in/your-profile](https://linkedin.com/in/your-profile)
