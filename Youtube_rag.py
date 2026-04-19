# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
# from youtube_transcript_api._errors import IpBlocked
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os
# import json
# import streamlit as st
# load_dotenv()


# st.title("YouTube RAG Chatbot")

# # YOUTUBE VIDEO TRANSCRIPT SCRAPING

# def get_transcript(video_id):
#     cache_dir = "cache"
#     os.makedirs(cache_dir, exist_ok=True)

#     cache_file = f"{cache_dir}/{video_id}.json"

#     # LOAD FROM CACHE
#     if os.path.exists(cache_file):
#         st.write(" Loading from cache...")
#         with open(cache_file, "r", encoding="utf-8") as f:
#             return json.load(f)

#     # FETCH ONLY IF NOT CACHED
#     try:
#         st.write(" Fetching from YouTube...")

#         transcript_list = YouTubeTranscriptApi().fetch(video_id)

#         transcript = " ".join(chunk.text for chunk in transcript_list)

#         # SAVE TO CACHE
#         with open(cache_file, "w", encoding="utf-8") as f:
#             json.dump(transcript, f)

#         return transcript

#     except TranscriptsDisabled:
#         st.write("No captions available for this video.")
#         return None

#     except IpBlocked:
#         st.write("IP blocked by YouTube. Try hotspot.")
#         return None




# video_id = st.text_input("Enter video id: ")
# if st.button("Load Video"):

#     transcript = get_transcript(video_id)

#     if not transcript:
#         st.stop()

#         #  CHUNKING
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=300
#     )

#     docs = splitter.create_documents([transcript])


#       #   EMBEDDING

#     embedding = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
#     vector_store = FAISS.from_documents(docs, embedding)


#     retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 6})

#     llm = ChatOpenAI(
#         api_key=os.getenv("GROQ_API_KEY"),
#         base_url="https://api.groq.com/openai/v1",  
#         model="llama-3.3-70b-versatile",
#         temperature=0.2
#     )

#     prompt = PromptTemplate(
#         template="""
#             You are a helpful assistant.
#             Answer ONLY from the provided transcript context.
#             If the context is insufficient, just say you don't know.

#             {context}
#             Question: {question}
#         """,
#         input_variables = ['context', 'question']
#     )


#     question = st.text_input("Ask your question: ")
#     if question:

#         retrieved_docs = retriever.invoke(question)

#         context = "\n\n".join(docs.page_content for docs in retrieved_docs)

#         final_prompt = prompt.invoke({
#             "context": context,
#             "question": question
#     })

#         response = llm.invoke(final_prompt)

#         st.write(response.content)



# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
# from youtube_transcript_api._errors import IpBlocked
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os
# import json
# import streamlit as st

# load_dotenv()

# st.title("YouTube RAG Chatbot")

# # Init session state
# if "retriever" not in st.session_state:
#     st.session_state.retriever = None
# if "llm" not in st.session_state:
#     st.session_state.llm = None
# if "prompt" not in st.session_state:
#     st.session_state.prompt = None
# if "video_loaded" not in st.session_state:
#     st.session_state.video_loaded = False


# # Transcript helper
# def get_transcript(video_id):
#     cache_dir = "cache"
#     os.makedirs(cache_dir, exist_ok=True)
#     cache_file = f"{cache_dir}/{video_id}.json"

#     if os.path.exists(cache_file):
#         st.write("Loading from cache...")
#         with open(cache_file, "r", encoding="utf-8") as f:
#             return json.load(f)

#     try:
#         st.write("Fetching from YouTube...")
#         transcript_list = YouTubeTranscriptApi().fetch(video_id)
#         transcript = " ".join(chunk.text for chunk in transcript_list)
#         with open(cache_file, "w", encoding="utf-8") as f:
#             json.dump(transcript, f)
#         return transcript

#     except TranscriptsDisabled:
#         st.error("No captions available for this video.")
#         return None
#     except IpBlocked:
#         st.error("IP blocked by YouTube. Try a hotspot.")
#         return None


# # Video input 
# video_id = st.text_input("Enter video ID:")

# if st.button("Load Video"):
#     st.session_state.video_loaded = False          # reset on new load

#     transcript = get_transcript(video_id)
#     if not transcript:
#         st.stop()

#     # Chunking
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=300
#     )
#     docs = splitter.create_documents([transcript])

#     # Embedding + vector store
#     with st.spinner("Building embeddings..."):
#         embedding = HuggingFaceEmbeddings(
#             model_name="sentence-transformers/all-MiniLM-L6-v2"
#         )
#         vector_store = FAISS.from_documents(docs, embedding)


#     st.session_state.retriever = vector_store.as_retriever(
#         search_type="similarity", search_kwargs={"k": 6}
#     )
#     st.session_state.llm = ChatOpenAI(
#         api_key=os.getenv("GROQ_API_KEY"),
#         base_url="https://api.groq.com/openai/v1",
#         model="llama-3.3-70b-versatile",
#         temperature=0.2
#     )
#     st.session_state.prompt = PromptTemplate(
#         template="""
#             You are a helpful assistant.
#             Answer ONLY from the provided transcript context.
#             If the context is insufficient, just say you don't know.

#             {context}
#             Question: {question}
#         """,
#         input_variables=["context", "question"]
#     )
#     st.session_state.video_loaded = True
#     st.success("Video loaded! You can now ask questions.")


# if st.session_state.video_loaded:
#     question = st.text_input("Ask your question:")

#     if question:
#         retrieved_docs = st.session_state.retriever.invoke(question)


#         context = "\n\n".join(doc.page_content for doc in retrieved_docs)

#         final_prompt = st.session_state.prompt.invoke({
#             "context": context,
#             "question": question
#         })

#         with st.spinner("Thinking..."):
#             response = st.session_state.llm.invoke(final_prompt)

#         st.write(response.content)









from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api._errors import IpBlocked
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st

load_dotenv()



st.title("YouTube RAG Chatbot")

if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "llm" not in st.session_state:
    st.session_state.llm = None
if "prompt" not in st.session_state:
    st.session_state.prompt = None
if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False
if "video_id" not in st.session_state:
    st.session_state.video_id = None


def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS or HH:MM:SS format."""
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def get_transcript(video_id):
    """Fetch transcript and return list of {text, start} dicts."""
    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = f"{cache_dir}/{video_id}.json"

    if os.path.exists(cache_file):
        st.write("Loading from cache...")
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    try:
        st.write("Fetching from YouTube...")
        transcript_list = YouTubeTranscriptApi().fetch(video_id)
        transcript = [{"text": chunk.text, "start": chunk.start} for chunk in transcript_list]
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(transcript, f)
        return transcript

    except TranscriptsDisabled:
        st.error("No captions available for this video.")
        return None
    except IpBlocked:
        st.error("IP blocked by YouTube. Try a hotspot.")
        return None


def build_timestamp_docs(transcript_chunks, chunk_size=1000, chunk_overlap=300):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    windows = []
    current_text = ""
    current_start = transcript_chunks[0]["start"]

    for chunk in transcript_chunks:
        if len(current_text) + len(chunk["text"]) > chunk_size and current_text:
            windows.append({"text": current_text.strip(), "start": current_start})
            current_text = chunk["text"]
            current_start = chunk["start"]
        else:
            current_text += " " + chunk["text"]

    if current_text.strip():
        windows.append({"text": current_text.strip(), "start": current_start})


    docs = splitter.create_documents(
        texts=[w["text"] for w in windows],
        metadatas=[{"start": w["start"]} for w in windows]
    )

    return docs


video_id = st.text_input("Enter video ID:")

if st.button("Load Video"):
    st.session_state.video_loaded = False

    transcript = get_transcript(video_id)
    if not transcript:
        st.stop()

    # Build docs with timestamp metadata
    docs = build_timestamp_docs(transcript, chunk_size=1000, chunk_overlap=300)

    with st.spinner("Building embeddings..."):
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        vector_store = FAISS.from_documents(docs, embedding)

    st.session_state.retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 6}
    )
    st.session_state.llm = ChatOpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        model="llama-3.3-70b-versatile",
        temperature=0.2
    )
    
    st.session_state.prompt = PromptTemplate(
        template="""
            You are a helpful assistant answering questions about a YouTube video.
            Each excerpt below is prefixed with its timestamp (e.g. [2:14]).
            Answer ONLY from the provided transcript context.
            When referencing something from the video, cite the timestamp like: "at 2:14".
            If the context is insufficient, just say you don't know.

            {context}
            Question: {question}
        """,
        input_variables=["context", "question"]
    )
    st.session_state.video_id = video_id
    st.session_state.video_loaded = True
    st.success("Video loaded! You can now ask questions.")


if st.session_state.video_loaded:
    question = st.text_input("Ask your question:")

    if question:
        retrieved_docs = st.session_state.retriever.invoke(question)

        # Prefix each chunk with its formatted timestamp
        context_parts = []
        for doc in retrieved_docs:
            ts = format_timestamp(doc.metadata.get("start", 0))
            context_parts.append(f"[{ts}]\n{doc.page_content}")
        context = "\n\n".join(context_parts)

        final_prompt = st.session_state.prompt.invoke({
            "context": context,
            "question": question
        })

        with st.spinner("Thinking..."):
            response = st.session_state.llm.invoke(final_prompt)

        st.write(response.content)

        # show clickable YouTube links for source timestamps
        with st.expander("📍 Source timestamps & chunks"):
            for doc in retrieved_docs:
                start_sec = int(doc.metadata.get("start", 0))
                ts = format_timestamp(start_sec)
                yt_url = f"https://www.youtube.com/watch?v={st.session_state.video_id}&t={start_sec}s"
                st.markdown(f"**[{ts}]({yt_url})**")
                st.caption(f"[{ts}] {doc.page_content}")  
                st.divider()