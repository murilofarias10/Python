# warning
import warnings

warnings.filterwarnings("ignore")

import os
from together import Together
import faiss

from sentence_transformers import SentenceTransformer

"""
Do these steps:
1) Set up a Together API key from https://together.ai/
"""
together_api_key = os.environ.get("TOGETHER_API_KEY")


def run_rag(data_dict: dict, prompt: str):
    """
    Run RAG system: process documents, create embeddings, search, and generate answer.

    """

    # Stage 0: Initialize Together AI client for LLM completions
    client = Together(api_key=together_api_key)

    # Stage 1: Load sentence transformer model for creating embeddings
    # ------------------------------------------------------------
    embedding_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2",
        use_auth_token=os.environ.get("HUGGINGFACE_HUB_TOKEN"),
    )

    # Stage 2: Process documents into Vector Database
    # ------------------------------------------------------------
    documents = []
    filenames = []

    print(f"Processing {len(data_dict)} documents...")
    for key, content in data_dict.items():
        content = content.strip()
        if content:  # Only add non-empty documents
            documents.append(content)
            filenames.append(key)
            print(f"✅ Loaded: {key}")

    if not documents:
        return "No valid documents found in data dictionary!"

    # Create embeddings for all documents
    print("Creating embeddings...")
    embeddings = embedding_model.encode(documents)

    # Set up FAISS index for similarity search
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    print(f"✅ RAG system ready with {len(documents)} documents!")

    # Stage 3: Retrieve relevant documents
    # ------------------------------------------------------------
    query_embedding = embedding_model.encode([prompt])
    faiss.normalize_L2(query_embedding)

    # Get top similar documents
    scores, indices = index.search(query_embedding, min(3, len(documents)))

    # Stage 4: Build context from retrieved documents
    # ------------------------------------------------------------
    relevant_docs = []
    context_parts = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < len(documents):
            doc_info = {
                "content": documents[idx],
                "filename": filenames[idx],
                "score": float(score),
            }
            relevant_docs.append(doc_info)
            context_parts.append(f"[{doc_info['filename']}]\n{doc_info['content']}")

    if not relevant_docs:
        return "No relevant documents found for the query."

    # Combine context
    context = "\n\n".join(context_parts)

    # Stage 5: Augment by running the LLM to generate an answer
    # ------------------------------------------------------------
    llm_prompt = f"""Answer the question based on the provided context documents.

Context:
{context}

Question: {prompt}

Instructions:
- Answer based only on the information in the context
- Answer should beat least 10 words at max 20 words
- If the context doesn't contain enough information, say so
- Mention which document(s) you're referencing
- Start with According to [document name]
- Add brackets to the document name


Answer:"""

    try:
        # Generate answer using Together AI
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[{"role": "user", "content": llm_prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        answer = response.choices[0].message.content

        # Display source information
        print(f"\n📚 Most relevant source:")
        for doc in relevant_docs:
            print(f"  • {doc['filename']} (similarity: {doc['score']:.3f})")

        # Add source information to the answer
        sources_list = [doc["filename"] for doc in relevant_docs]
        sources_text = sources_list[0]
        full_answer = f"{answer}\n\n📄 Source Used: {sources_text}"

        return full_answer

    except Exception as e:
        return f"Error generating answer: {str(e)}"


if __name__ == "__main__":

    # Load dataset
    data_dict = {
        "octopus_facts": "Octopuses have three hearts and blue blood. Two hearts pump blood to the gills, while the third pumps blood to the rest of the body. Their blood is blue because it contains copper-based hemocyanin instead of iron-based hemoglobin.",
        "honey_facts": "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible. This is because honey has natural antibacterial properties and very low water content.",
        "space_facts": "A day on Venus is longer than its year. Venus takes 243 Earth days to rotate once on its axis, but only 225 Earth days to orbit the Sun. This means a Venusian day is longer than a Venusian year.",
        "banana_facts": "Bananas are berries, but strawberries aren't. Botanically speaking, berries must have seeds inside their flesh. Bananas qualify, but strawberries have seeds on the outside, making them aggregate fruits.",
        "shark_facts": "Sharks have been around longer than trees. Sharks first appeared around 400 million years ago, while the earliest trees appeared around 350 million years ago. This means sharks pre-date trees by about 50 million years.",
        "penguin_facts": "Emperor penguins can hold their breath for over 20 minutes and dive to depths of over 500 meters while hunting for fish. They have special adaptations including collapsible lungs and the ability to slow their heart rate.",
        "human_brain": "Your brain uses about 20% of your body's total energy despite being only 2% of your body weight. It consumes roughly 320 calories per day, which is equivalent to eating about 320 M&Ms.",
    }

    question = "What is interesting about a banana?"
    answer = run_rag(data_dict, question)
    print(f"\n🤖 Answer: {answer}\n")
    print("-" * 50)
