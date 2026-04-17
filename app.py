"""
Voice-Powered Q&A Agent — Main Application

A Gradio-based web application that lets users:
1. Upload a PDF document
2. Ask questions via voice or text
3. Get answers with audio playback

Pipeline: Voice → SpeechRecognition → RAG Agent → gTTS → Spoken Answer
"""

import gradio as gr
from rag_engine import RAGEngine
from voice_utils import speech_to_text, text_to_speech

# Initialize the RAG Engine
rag = RAGEngine()


def process_pdf(pdf_file):
    """Handle PDF upload and initialize the RAG pipeline."""
    if pdf_file is None:
        return "⚠️ Please upload a PDF file."
    
    # Gradio File with type="filepath" returns the path as a string
    status = rag.load_pdf(pdf_file)
    return status


def process_voice_question(audio_filepath):
    """Convert voice to text, get RAG answer, convert to speech."""
    if audio_filepath is None:
        return "⚠️ No audio received. Please record your question.", "", None

    # Step 1: Speech to Text
    question = speech_to_text(audio_filepath)
    if not question or question.startswith("⚠️") or question.startswith("❌"):
        return question, "", None

    # Step 2: Get answer from RAG
    answer = rag.get_answer(question)

    # Step 3: Convert answer to speech
    audio_path = text_to_speech(answer)

    return question, answer, audio_path


def process_text_question(question):
    """Get RAG answer for typed question and convert to speech."""
    if not question or not question.strip():
        return "⚠️ Please type a question.", None

    # Step 1: Get answer from RAG
    answer = rag.get_answer(question)

    # Step 2: Convert answer to speech
    audio_path = text_to_speech(answer)

    return answer, audio_path


# ═══════════════════════════════════════════════════
#  GRADIO UI
# ═══════════════════════════════════════════════════

# Custom CSS for a polished look
custom_css = """
.gradio-container {
    max-width: 900px !important;
    margin: auto !important;
}
.main-title {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5em;
    font-weight: 800;
    margin-bottom: 0;
}
.subtitle {
    text-align: center;
    color: #666;
    font-size: 1.1em;
    margin-top: 5px;
}
.pipeline-box {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    font-family: monospace;
    font-size: 0.95em;
    color: #000000 !important;
    margin: 10px 0;
}
"""

# Build the Gradio Interface
with gr.Blocks(css=custom_css, title="🎤 Voice-Powered Q&A Agent", theme=gr.themes.Soft()) as app:
    
    # Header
    gr.HTML("""
        <h1 class="main-title">🎤 Voice-Powered Q&A Agent</h1>
        <p class="subtitle">Ask questions about your PDF — by voice or text!</p>
    """)
    
    gr.HTML("""
        <div class="pipeline-box">
            🎤 Voice Input → 📝 SpeechRecognition → 🔍 RAG Agent (PDF Search) → 🔊 gTTS → 🗣️ Spoken Answer
        </div>
    """)

    # ── Step 1: PDF Upload ──
    with gr.Accordion("📄 Step 1: Upload Your PDF", open=True):
        gr.Markdown("Upload a PDF document that you want to ask questions about.")
        with gr.Row():
            pdf_input = gr.File(
                label="Upload PDF",
                file_types=[".pdf"],
                type="filepath"
            )
            pdf_status = gr.Textbox(
                label="Status",
                interactive=False,
                lines=3
            )
        pdf_btn = gr.Button("📤 Load PDF", variant="primary", size="lg")
        pdf_btn.click(fn=process_pdf, inputs=pdf_input, outputs=pdf_status)

    # ── Step 2: Ask Questions ──
    with gr.Accordion("💬 Step 2: Ask Questions", open=True):
        
        with gr.Tabs():
            # Tab 1: Voice Input
            with gr.TabItem("🎤 Voice Input"):
                gr.Markdown("Record your question using the microphone.")
                voice_input = gr.Audio(
                    label="Record Your Question",
                    sources=["microphone", "upload"],
                    type="filepath"
                )
                voice_btn = gr.Button("🎤 Ask by Voice", variant="primary", size="lg")
                
                voice_question_output = gr.Textbox(
                    label="🗣️ Your Question (recognized text)",
                    interactive=False
                )
                voice_answer_output = gr.Textbox(
                    label="📝 Answer",
                    interactive=False,
                    lines=5
                )
                voice_audio_output = gr.Audio(
                    label="🔊 Listen to Answer",
                    type="filepath",
                    autoplay=True
                )
                
                voice_btn.click(
                    fn=process_voice_question,
                    inputs=voice_input,
                    outputs=[voice_question_output, voice_answer_output, voice_audio_output]
                )

            # Tab 2: Text Input
            with gr.TabItem("⌨️ Text Input"):
                gr.Markdown("Type your question below.")
                text_input = gr.Textbox(
                    label="Type Your Question",
                    placeholder="e.g., What is the main topic of this document?",
                    lines=2
                )
                text_btn = gr.Button("📤 Ask by Text", variant="primary", size="lg")
                
                text_answer_output = gr.Textbox(
                    label="📝 Answer",
                    interactive=False,
                    lines=5
                )
                text_audio_output = gr.Audio(
                    label="🔊 Listen to Answer",
                    type="filepath",
                    autoplay=True
                )
                
                text_btn.click(
                    fn=process_text_question,
                    inputs=text_input,
                    outputs=[text_answer_output, text_audio_output]
                )

    # ── Architecture Info ──
    with gr.Accordion("ℹ️ How It Works", open=False):
        gr.Markdown("""
        ### Pipeline Architecture
        
        | Step | Component | What it does |
        |------|-----------|-------------|
        | 1️⃣ | **SpeechRecognition** | Converts your voice to text |
        | 2️⃣ | **PyPDF2 + FAISS** | Parses PDF and searches for relevant content |
        | 3️⃣ | **Groq Llama 3 LLM** | Generates a natural language answer |
        | 4️⃣ | **gTTS** | Converts the answer to spoken audio |
        
        ### Tech Stack
        - **Embeddings**: HuggingFace `all-MiniLM-L6-v2` (runs locally, free)
        - **Vector Store**: FAISS (Facebook AI Similarity Search)
        - **LLM**: Groq Llama 3 (8B)
        - **UI**: Gradio
        """)

    # Footer
    gr.HTML("""
        <div style="text-align: center; margin-top: 20px; padding: 15px; 
                    background: linear-gradient(135deg, #667eea22, #764ba222); 
                    border-radius: 10px;">
            <p style="color: #666; font-size: 0.9em; margin: 0;">
                Made By Keshav Gupta | Voice-Powered Q&A Agent
            </p>
        </div>
    """)

# Launch the app
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  🎤 Voice-Powered Q&A Agent")
    print("  Starting Gradio server...")
    print("=" * 60 + "\n")
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )
