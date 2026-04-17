"""
Generate a sample PDF for testing the Voice-Powered Q&A Agent.
Run this script once to create 'sample.pdf' in the project directory.
"""

from fpdf import FPDF


def create_sample_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Page 1: Introduction to Artificial Intelligence
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 15, "Artificial Intelligence", ln=True, align="C")
    pdf.set_font("Helvetica", "I", 14)
    pdf.cell(0, 10, "A Comprehensive Overview", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "1. What is Artificial Intelligence?", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 7,
        "Artificial Intelligence (AI) is a branch of computer science that focuses on creating "
        "intelligent machines that can perform tasks that typically require human intelligence. "
        "These tasks include learning, reasoning, problem-solving, perception, language understanding, "
        "and decision making. AI was founded as an academic discipline in 1956, and since then it has "
        "experienced several waves of optimism, followed by periods of disappointment known as 'AI winters', "
        "followed by new approaches, success, and renewed funding."
    )
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "2. Types of Artificial Intelligence", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 7,
        "AI can be categorized into three main types:\n\n"
        "a) Narrow AI (Weak AI): This is AI that is designed and trained for a specific task. "
        "Virtual assistants like Siri, Alexa, and Google Assistant are examples of Narrow AI. "
        "They operate within a limited context and cannot perform tasks outside their designated function.\n\n"
        "b) General AI (Strong AI): This refers to AI that has the ability to understand, learn, "
        "and apply knowledge across a wide range of tasks, similar to human intelligence. "
        "General AI does not yet exist but is a goal of many AI researchers.\n\n"
        "c) Super AI: This is a hypothetical form of AI that would surpass human intelligence "
        "in virtually every field, including creativity, problem-solving, and social skills. "
        "Super AI remains a theoretical concept."
    )
    pdf.ln(5)

    # Page 2: Machine Learning & Deep Learning
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "3. Machine Learning", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 7,
        "Machine Learning (ML) is a subset of AI that enables systems to learn and improve from "
        "experience without being explicitly programmed. ML algorithms use historical data as input "
        "to predict new output values. There are three main types of machine learning:\n\n"
        "a) Supervised Learning: The algorithm learns from labeled training data. Examples include "
        "classification (spam detection) and regression (price prediction).\n\n"
        "b) Unsupervised Learning: The algorithm finds patterns in unlabeled data. Examples include "
        "clustering (customer segmentation) and dimensionality reduction.\n\n"
        "c) Reinforcement Learning: The algorithm learns by interacting with an environment and "
        "receiving rewards or penalties. Examples include game playing (AlphaGo) and robotics."
    )
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "4. Deep Learning", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 7,
        "Deep Learning is a subset of machine learning that uses artificial neural networks with "
        "multiple layers (deep neural networks) to model and understand complex patterns in data. "
        "Key architectures include:\n\n"
        "a) Convolutional Neural Networks (CNNs): Used primarily for image recognition and "
        "computer vision tasks.\n\n"
        "b) Recurrent Neural Networks (RNNs): Used for sequential data like text and time series.\n\n"
        "c) Transformers: The architecture behind modern language models like GPT, BERT, and Gemini. "
        "Transformers use self-attention mechanisms to process entire sequences simultaneously, "
        "making them highly effective for natural language processing tasks."
    )
    pdf.ln(5)

    # Page 3: NLP, Gen AI, and Applications
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "5. Natural Language Processing (NLP)", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 7,
        "Natural Language Processing (NLP) is a field of AI that focuses on the interaction between "
        "computers and humans through natural language. Key NLP tasks include:\n\n"
        "- Sentiment Analysis: Determining the emotional tone of text\n"
        "- Named Entity Recognition: Identifying names, places, and organizations in text\n"
        "- Machine Translation: Translating text between languages\n"
        "- Text Summarization: Creating concise summaries of longer documents\n"
        "- Question Answering: Finding answers to questions from a given context\n\n"
        "Modern NLP is largely powered by transformer-based models like BERT, GPT-4, and Gemini."
    )
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "6. Generative AI", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 7,
        "Generative AI refers to AI systems that can create new content, including text, images, "
        "music, and code. Key concepts include:\n\n"
        "- Large Language Models (LLMs): Models like GPT-4, Gemini, and Claude that generate "
        "human-like text based on training data.\n"
        "- RAG (Retrieval Augmented Generation): A technique that combines information retrieval "
        "with text generation. RAG first retrieves relevant documents from a knowledge base, "
        "then uses an LLM to generate answers based on the retrieved context. This reduces "
        "hallucination and provides more accurate, grounded responses.\n"
        "- Prompt Engineering: The practice of designing effective prompts to guide AI models "
        "toward desired outputs.\n"
        "- Fine-tuning: Adapting a pre-trained model to a specific task or domain using "
        "additional training data."
    )
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "7. Applications of AI", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 7,
        "AI has transformative applications across many industries:\n\n"
        "- Healthcare: Disease diagnosis, drug discovery, and personalized treatment\n"
        "- Finance: Fraud detection, algorithmic trading, and risk assessment\n"
        "- Education: Personalized learning, automated grading, and intelligent tutoring\n"
        "- Transportation: Self-driving cars, traffic optimization, and route planning\n"
        "- Manufacturing: Quality control, predictive maintenance, and supply chain optimization\n"
        "- Customer Service: Chatbots, virtual assistants, and sentiment analysis\n"
        "- Entertainment: Content recommendation, game development, and music generation"
    )

    # Save the PDF
    pdf.output("sample.pdf")
    print("✅ sample.pdf created successfully!")


if __name__ == "__main__":
    create_sample_pdf()
