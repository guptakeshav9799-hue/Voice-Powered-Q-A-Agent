"""
RAG Engine — PDF-based Retrieval Augmented Generation Pipeline

This module handles:
1. Loading and parsing PDF documents
2. Splitting text into searchable chunks
3. Creating embeddings and storing in FAISS vector store
4. Answering questions using Groq LLM (Llama 3) with retrieved context
"""

import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
# from langchain.chains import RetrievalQA
# from langchain.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
# Load environment variables
load_dotenv()


class RAGEngine:
    """RAG Engine that loads a PDF, creates a vector store, and answers questions."""

    def __init__(self):
        self.vector_store = None
        self.qa_chain = None
        self.embeddings = None
        self.is_ready = False

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract all text from a PDF file."""
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text

    def _split_text_into_chunks(self, text: str) -> list:
        """Split text into smaller chunks for better retrieval."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = text_splitter.split_text(text)
        return chunks

    def load_pdf(self, pdf_path: str) -> str:
        """
        Load a PDF, create embeddings, and set up the QA chain.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Status message indicating success or failure
        """
        try:
            # Step 1: Extract text from PDF
            print(f"📄 Loading PDF: {pdf_path}")
            text = self._extract_text_from_pdf(pdf_path)

            if not text.strip():
                return "❌ Error: Could not extract any text from the PDF. The PDF might be scanned/image-based."

            # Step 2: Split text into chunks
            print("✂️ Splitting text into chunks...")
            chunks = self._split_text_into_chunks(text)
            print(f"   Created {len(chunks)} text chunks")

            # Step 3: Create embeddings using HuggingFace (free, runs locally)
            print("🧠 Creating embeddings (this may take a moment on first run)...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"}
            )

            # Step 4: Create FAISS vector store
            print("📦 Building FAISS vector store...")
            self.vector_store = FAISS.from_texts(chunks, self.embeddings)

            # Step 5: Set up the QA chain with Groq (Llama 3)
            print("🤖 Setting up Groq LLM (Llama 3)...")
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key or api_key == "your_api_key_here":
                return "❌ Error: Please set your GROQ_API_KEY in the .env file!\nGet a free key at: https://console.groq.com/keys"

            llm = ChatGroq(
                model="llama-3.1-8b-instant",
                groq_api_key=api_key,
                temperature=0.3
            )

            # Custom prompt template for better answers
            prompt_template = """You are a helpful Q&A assistant. Use the following context from a PDF document to answer the question. 
If the answer is not found in the context, say "I couldn't find the answer in the provided document."

Context from PDF:
{context}

Question: {question}

Answer in a clear, concise, and helpful manner:"""

            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )

            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 4}),
                chain_type_kwargs={"prompt": PROMPT},
                return_source_documents=False
            )

            self.is_ready = True
            return f"✅ PDF loaded successfully! Created {len(chunks)} searchable chunks. You can now ask questions!"

        except Exception as e:
            return f"❌ Error loading PDF: {str(e)}"

    def get_answer(self, question: str) -> str:
        """
        Get an answer to a question based on the loaded PDF.
        
        Args:
            question: The question to answer
            
        Returns:
            The answer string
        """
        if not self.is_ready:
            return "⚠️ Please upload a PDF first before asking questions!"

        if not question.strip():
            return "⚠️ Please provide a question."

        try:
            print(f"🔍 Searching for answer to: {question}")
            result = self.qa_chain.invoke({"query": question})
            answer = result.get("result", "Sorry, I couldn't generate an answer.")
            print(f"✅ Answer generated successfully")
            return answer
        except Exception as e:
            return f"❌ Error generating answer: {str(e)}"
