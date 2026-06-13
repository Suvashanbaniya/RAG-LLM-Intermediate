
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
       