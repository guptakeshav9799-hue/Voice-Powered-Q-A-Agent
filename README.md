---
title: Voice Powered QA Agent
emoji: 🎤
colorFrom: blue
colorTo: purple
sdk: gradio
app_file: app.py
pinned: false
---

# Voice-Powered Q&A Agent

Hey! This is a project I built for my Gen AI Workshop assignment. It's a Python application that lets you talk to your PDF documents using your voice.

Basically, you upload a PDF, ask a question using your microphone, and the app searches through the document using Retrieval-Augmented Generation (RAG) to find the answer. It then reads the answer out loud back to you.

## What I used to build this
I wanted to combine Speech-to-Text, LLMs, and Text-to-Speech natively. Here is the tech stack I ended up using:
- **SpeechRecognition & gTTS:** For converting my voice to text, and the AI's generated text back to voice.
- **PyPDF2 & LangChain:** To read the PDFs and chunk the text so the AI can process it.
- **HuggingFace & FAISS:** I used `all-MiniLM-L6-v2` to create embeddings locally (to keep it free!) and FAISS to store and search them quickly.
- **Groq (Llama 3.1 8B):** Because it's extremely fast at generating the final answers from the context.
- **Gradio:** For the frontend web UI because it's super easy to prototype with.

## How to run it locally

If you want to run this on your own machine, follow these steps.

1. **Clone and install dependencies:**
```bash
git clone https://github.com/guptakeshav9799-hue/Voice-Powered-Q-A-Agent.git
cd Voice-Powered-Q-A-Agent
pip install -r requirements.txt
```

2. **Set up the Groq API Key:**
Go to the [Groq Console](https://console.groq.com/keys) and get a free API key. Create a `.env` file in the root folder and add your key like this:
```
GROQ_API_KEY=your_api_key_here
```

3. **Run the app:**
```bash
python app.py
```
The terminal will give you a local URL (usually `http://localhost:7861`). Open that in your browser.

## How my RAG Pipeline works
1. **Document Processing:** When you upload a PDF, `PyPDF2` extracts the text and `LangChain` splits it into smaller chunks (I set it to 1000 characters with some overlap).
2. **Vector Database:** Those chunks are converted to numerical vectors using the HuggingFace model and saved in a FAISS index.
3. **Voice Input:** When you speak, the `SpeechRecognition` library records your microphone and transcribes it to text using Google's speech API.
4. **Retrieval:** The app takes your transcribed question, searches the FAISS database for the most relevant textbook chunks, and sends that context to Llama 3.1.
5. **Voice Output:** Finally, Llama 3.1 figures out the answer, and `gTTS` turns that final string of text back into an `.mp3` audio file that plays automatically.

---
*Created by Keshav Gupta for the Gen AI Workshop.*
