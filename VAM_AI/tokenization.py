#pip install torch torchvision torchaudio
#pip sintall transformers matplotlib

# Tokenization using Hugging Face's Transformers
from transformers import AutoTokenizer

# Embedding and Processing with a Transformer Model
from transformers import AutoModel

# Replace "gpt-2" with "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")
phrase = "A young girl named Alice sits bored by a riverbank."
only_tokens = tokenizer.tokenize(phrase)
inputs = tokenizer(phrase, return_tensors="pt")
print(inputs)

outputs = model(**inputs)  
last_hidden_states = outputs.last_hidden_state
print(last_hidden_states.shape)  

# Visualization of Embeddings (Simplified Example)
# Visualization of Embeddings (Simplified Example)
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 5))  # Wider figure
plt.imshow(last_hidden_states.detach().numpy()[0], cmap='viridis', aspect='auto')
plt.colorbar()
plt.xlabel("Embedding Dimension")
plt.ylabel("Token Index")
plt.title("BERT Token Embeddings")
plt.show()