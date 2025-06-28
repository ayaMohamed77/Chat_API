from openai import OpenAI

import os

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def ask_bot(prompt: str) -> str:
    import os
    print("API KEY ===>", os.getenv("OPENROUTER_API_KEY"))
    system_prompt = (
        "You are a helpful assistant that only answers questions about Alzheimer's disease. "
        "If the user asks about anything else, respond with 'I am sorry I'm a specialized Ai Assistant in Alzheimer's disease.'"
    )

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat:free",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

    )


    return response.choices[0].message.content
