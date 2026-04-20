#  YouTube RAG Chatbot

An AI-powered chatbot that can understand and answer questions about any YouTube video using **Retrieval-Augmented Generation (RAG)**.

---

##  Overview

This project allows users to paste a YouTube video URL and interact with its content using natural language.

Instead of watching the full video, users can directly ask questions and get **accurate, timestamped answers** from the video transcript.

---

##  Features

- 📺 Input any YouTube video URL  
- 📝 Automatically extracts video transcript  
- 🔍 Splits transcript into chunks for better retrieval  
- 🧠 Uses embeddings + FAISS for semantic search  
- 🤖 Answers questions using LLM (Llama 3 via Groq API)  
- ⏱ Provides timestamps for each answer  
- 🔗 Clickable timestamps to jump to exact video moments  
- ⚡ Fast and interactive Streamlit UI  

---

##  Why RAG?

Large Language Models like ChatGPT:
- Don’t have access to custom video content  
- Cannot retrieve real-time or private data  
- May generate hallucinated answers  

### RAG solves this by:
- Retrieving relevant context from your data first  
- Then generating answers using that context  

👉 This ensures more accurate and grounded responses.

---

##  Tech Stack

- Python  
- Streamlit  
- LangChain  
- FAISS (Vector Database)  
- HuggingFace Embeddings  
- Llama 3 (via Groq API)  
- Supadata API (for transcripts)  

---

##  How It Works

1. User enters YouTube URL  
2. Transcript is fetched using API  
3. Transcript is split into chunks  
4. Embeddings are generated and stored in FAISS  
5. User asks a question  
6. Relevant chunks are retrieved  
7. LLM generates final answer with timestamps  

---

##  Example Use Case

- “What is this video about?”  
- “Explain the part at 3:20”  
- “What does the speaker say about neural networks?”  

---
