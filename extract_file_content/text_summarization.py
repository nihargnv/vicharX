from transformers import pipeline

# Initialize the summarization pipeline with the Falconsai/text_summarization model
summarizer = pipeline("summarization", model="Falconsai/text_summarization")

# Example article to summarize
ARTICLE = """
Hugging Face: Revolutionizing Natural Language Processing
Introduction
In the rapidly evolving field of Natural Language Processing (NLP), Hugging Face has emerged as a prominent and innovative force. This article will explore the story and significance of Hugging Face, a company that has made remarkable contributions to NLP and AI as a whole. From its inception to its role in democratizing AI, Hugging Face has left an indelible mark on the industry.
The Birth of Hugging Face
Hugging Face was founded in 2016 by Clément Delangue, Julien Chaumond, and Thomas Wolf. The name "Hugging Face" was chosen to reflect the company's mission of making AI models more accessible and friendly to humans, much like a comforting hug. Initially, they began as a chatbot company but later shifted their focus to NLP, driven by their belief in the transformative potential of this technology.
Transformative Innovations
Hugging Face is best known for its open-source contributions, particularly the "Transformers" library. This library has become the de facto standard for NLP and enables researchers, developers, and organizations to easily access and utilize state-of-the-art pre-trained language models, such as BERT, GPT-3, and more. These models have countless applications, from chatbots and virtual assistants to language translation and sentiment analysis.
Key Contributions:
1. **Transformers Library:** The Transformers library provides a unified interface for more than 50 pre-trained models, simplifying the development of NLP applications. It allows users to fine-tune these models for specific tasks, making it accessible to a wider audience.
2. **Model Hub:** Hugging Face's Model Hub is a treasure trove of pre-trained models, making it simple for anyone to access, experiment with, and fine-tune models. Researchers and developers around the world can collaborate and share their models through this platform.
3. **Hugging Face Transformers Community:** Hugging Face has fostered a vibrant online community where developers, researchers, and AI enthusiasts can share their work, ask questions, and collaborate on projects. This sense of community has accelerated progress in NLP research and development.
Democratizing AI
One of Hugging Face's core missions is to democratize AI. By open-sourcing their tools and models, they have lowered the barrier to entry for individuals and organizations interested in NLP. This approach has empowered a diverse range of users, from startups to large enterprises, to leverage AI in their applications without the need for extensive resources.
Conclusion
Hugging Face's journey from a chatbot company to a leading force in NLP exemplifies the power of innovation and community collaboration. Their contributions have not only advanced the field of Natural Language Processing but have also made AI more accessible to all. As NLP continues to evolve, Hugging Face remains at the forefront, driving progress and shaping the future of AI.
"""

# Generate the summary
def summarize(text):
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']
# Print the summary

