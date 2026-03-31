from openai import OpenAI


def deepseek(question, config):
    client = OpenAI(
        api_key=config.deepseek_api,
        base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": question},
        ],
        stream=False
    )

    answer = response.choices[0].message.content
    return answer
