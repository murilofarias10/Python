from huggingface_hub import InferenceClient

# Defina seu token
HUGGINGFACEHUB_API_TOKEN = "x"

# Cria o cliente de inferência da Hugging Face
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=HUGGINGFACEHUB_API_TOKEN
)

# Faz uma pergunta simples para testar a IA
response = client.text_generation(
    "Tell me something interesting about watter.",
    max_new_tokens=200,
    temperature=0.7
)

print("🚀 IA Response:", response)
