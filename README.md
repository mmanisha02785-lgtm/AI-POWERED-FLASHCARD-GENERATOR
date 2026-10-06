#  AI-Powered Flashcard Generator

An AI-powered web application that automatically generates study flashcards from a topic, notes, or PDF file.

##  Features

* Generate flashcards using AI
* Enter a study topic or notes
* Upload PDF study material
* Generate questions and answers automatically
* Display flashcards interactively
* Reveal answers when needed
* Navigate between flashcards
* Simple and user-friendly Streamlit interface
* Runs locally using Ollama

##  Technologies Used

* Python
* Streamlit
* Ollama
* Llama 3.2
* PyPDF

##  Project Structure

```text
AI-Flashcard-Generator/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/mmanisha02785-lgtm/AI-POWERED-FLASHCARD-GENERATOR.git
```

### 2. Open the project folder

```bash
cd AI-Flashcard-Generator
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install required packages

```bash
pip install -r requirements.txt
```

##  Ollama Setup

Install Ollama and download the Llama 3.2 model.

```bash
ollama pull llama3.2
```

Make sure Ollama is running before starting the application.

##  Run the Application

Run:

```bash
streamlit run app.py
```

The application will open in your browser.

Usually:

```text
http://localhost:8501
```

##  How It Works

1. User enters a topic or study notes.
2. User can optionally upload a PDF.
3. The application extracts the required text.
4. The text is sent to the local Llama 3.2 model through Ollama.
5. AI generates flashcards.
6. The generated flashcards are displayed in the Streamlit interface.
7. Users can review the questions and answers.

##  Privacy

The project is designed to run locally using Ollama, so the AI model can process the study content on the user's computer.

##  Purpose

This project helps students create study flashcards quickly from their learning materials and makes revision easier and more interactive.

##  Author

M.Manisha

##  License

This project is created for educational purposes.
