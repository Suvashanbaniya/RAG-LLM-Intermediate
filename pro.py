import requests, json

from sklearn.metrics.pairwise import cosine_similarity

embed_url = "http://localhost:11434/api/embeddings"
llm_url = "http://localhost:11434/api/generate"

temperature = 0.3


def load_data():
    with open("family_data.json", "r") as f:
        return json.load(f)


info = json.dumps(load_data(), indent=2)
print(info)


def get_embedding(text):
    try:
        response = requests.post(embed_url, json={
            "model": "nomic-embed-text",
            "prompt": text,
        })

        data = response.json()

        if "embedding" not in data:
            return [0.0] * 768

        return data["embedding"]

    except:
        return [0.0] * 768


# ---------- PREPARE CHUNKS ----------
chunk_size = 10
lines = info.splitlines()

chunks = []

for i in range(0, len(lines), chunk_size):
    chunk = "\n".join(lines[i:i + chunk_size])

    if chunk.strip():
        chunks.append(chunk)


chunk_embeddings = []

for chunk in chunks:
    emb = get_embedding(chunk)
    chunk_embeddings.append(emb)


# ---------- MAIN FUNCTION FOR FLASK ----------
def ask_llm(user_input):

    query_embedding = get_embedding(user_input)

    similarities = []

    for i in range(len(chunk_embeddings)):

        score = cosine_similarity(
            [query_embedding],
            [chunk_embeddings[i]]
        )[0][0]

        similarities.append((score, chunks[i]))

    similarities.sort(reverse=True)

    top_chunks = similarities[:3]

    context = "\n".join([item[1] for item in top_chunks])
    
    print("\n===============CONTEXT=========")
    print(context)
    print("=====================\n")
    
    
    print("\nUSER:",user_input)
    
    for score, text in top_chunks:
        print("\nScore:",round(score,3))
        print(text)
    
    
    
    prompt = f"""
You are a family assistant.
Answser only from the family data below.
If the answer is not present in the family data, say:
"I dont know ."
Family Data:
{context}

User Question:
{user_input}


"""
    try:
        response = requests.post(llm_url, json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "temperature": temperature,
        })

        data = response.json()
        return data.get("response", "No response from model")

    except Exception as e:
        return f"LLM Error: {str(e)}"