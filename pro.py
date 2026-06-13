import requests, json
import sqlite3

from sklearn.metrics.pairwise import cosine_similarity

embed_url = "http://localhost:11434/api/embeddings"
llm_url = "http://localhost:11434/api/generate"

conn = sqlite3.connect("family.db",check_same_thread=False)
cursor = conn.cursor()

temperature = 0.3

messages = [ ]

# this is the sqlite data base for the LLM 
def get_family_data():
    cursor.execute("SELECT name , relation , details FROM family ")
    rows = cursor.fetchall()
    
    text = ""
    for row in rows:
        text += f"{row[0]} ({row[1]}) : {row[2]}\n"

    return text 


def get_embedding(text):
    try:
        response = requests.post(embed_url, json={
            "model": "nomic-embed-text",
            "prompt": text,
        })

        data = response.json()

        if "embedding" not in data:
            return [0.0] * 768

        return data.get("embedding",[0.0] * 768)

    except Exception as e :
        print("Embedding error :",e)
        return [0.0] * 768


# ---------- PREPARE CHUNKS ----------
chunk_size = 10
info = get_family_data()
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
    
    messages.append({"role":"user",
                     "content":user_input})
    print("\n===============CONTEXT=========")
    print(context)
    print("=====================\n")
    
    
    print("\nUSER:",user_input)
    
    for score, text in top_chunks:
        print("\nScore:",round(score,3))
        print(text)
    
    
    history_text = ""
    
    for msg in messages :
        history_text += f"{msg['role']}: {msg['content']}\n"
    
    
    prompt = f"""
You are a family assistant.
Answser only from the family data below.
If the answer is not present in the family data, say:
"I dont know ."
Family Data:
{context}
Conversation history:
{history_text}

User Question:
{user_input}
Answer naturally 

"""
    try:
        response = requests.post(llm_url, json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "temperature": temperature,
        })

        data = response.json()
        answer = data.get("response","No response from model ")
        messages.append({"role":"assistant","content":answer})
        return  answer
       
    except Exception as e:
        return f"LLM Error: {str(e)}"