import os
import streamlit as st
from sentence_transformers import SentenceTransformer
import pickle
import faiss
import numpy as np
from sklearn.preprocessing import normalize

# Paths
save_folder = r"C:\Users\MuriloFarias\Documents\AI"
index_path = os.path.join(save_folder, "faiss_index.bin")
metadata_path = os.path.join(save_folder, "metadata.pkl")

# Load the model, FAISS index, and metadata
@st.cache_resource
def load_resources():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index(index_path)
    with open(metadata_path, "rb") as f:
        metadata = pickle.load(f)
    return model, index, metadata

model, index, metadata = load_resources()

# Normalize the FAISS index
def normalize_index(index):
    embeddings = []
    for i in range(index.ntotal):
        vec = index.reconstruct(i)
        embeddings.append(vec)
    embeddings = np.array(embeddings)
    embeddings = normalize(embeddings, axis=1)
    new_index = faiss.IndexFlatIP(embeddings.shape[1])
    new_index.add(embeddings)
    return new_index

index = normalize_index(index)

# Batch processing for large queries
def chunk_query(question, max_length=128):
    words = question.split()
    return [' '.join(words[i:i + max_length]) for i in range(0, len(words), max_length)]

# Query FAISS
def query_faiss(question, index, model, metadata, threshold=0.3, k=3):
    chunks = chunk_query(question)
    results = []
    seen_texts = set()  # Track unique matched texts
    seen_files = set()  # Track unique file names

    for chunk in chunks:
        question_embedding = model.encode([chunk], convert_to_tensor=True).cpu().numpy()
        question_embedding = normalize(question_embedding, axis=1)

        # Fetch a larger pool of candidates
        D, I = index.search(np.array(question_embedding), k=k * 10)

        for idx, distance in zip(I[0], D[0]):
            if idx != -1 and distance >= threshold:
                file_name = metadata[idx]["file"]
                matched_text = metadata[idx]["chunk"]

                # Ensure both unique files and unique chunks
                if (file_name not in seen_files) and (matched_text not in seen_texts):
                    results.append({
                        "relevant_file": file_name,
                        "file_path": metadata[idx]["path"],
                        "matched_text": matched_text,
                        "similarity_score": float(distance)
                    })
                    seen_files.add(file_name)
                    seen_texts.add(matched_text)

                # Stop if we have enough diverse results
                if len(results) >= k:
                    break
        if len(results) >= k:
            break

    # Sort by similarity score before returning
    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    return results if results else {"error": "No relevant information found."}

# Streamlit Interface
# Add the company logo or flag
# st.image("https://i.ibb.co/xX7dr3v/Logo-colorido1.png", use_container_width=False, width=150)

# Add the title
st.title("Kubik FolderSense")
st.write("Ask questions about your PDFs.")

question = st.text_input("Enter your question:")
if st.button("Ask"):
    if question:
        with st.spinner("Processing your query..."):
            result = query_faiss(question, index, model, metadata, k=3)
        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Top 3 Relevant Files Matched:")
            for idx, res in enumerate(result, start=1):
                st.markdown(f"**{idx}. Relevant File:** {res['relevant_file']}")
                st.write(f"**File Path:** {res['file_path']}")
                st.write(f"**Similarity Score:** {res['similarity_score']:.2f}")
                st.write(f"**Matched Text:** {res['matched_text']}")
                st.markdown("---")

# Footer
# st.markdown("<div class='footer'>Made with ❤️ using Streamlit</div>", unsafe_allow_html=True)
