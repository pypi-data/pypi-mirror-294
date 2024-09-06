from openai import OpenAI, AzureOpenAI


def oai_client_with_openai():
    client = OpenAI(
        api_key='sk-xylx1.t!@#',
        base_url="https://xingchen-solution.cn-huabei-1.xf-yun.com/llm-api/v1",
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "what's your name?"}],
    )
    print(response.choices[0].message.content)


def oai_client_with_azure():
    client = AzureOpenAI(
        api_key="9f313a3f7b01472188508b9b64b5d469",
        api_version="2024-05-01-preview",
        azure_endpoint="https://gpt-4-rdg.openai.azure.com/"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "what's your name?"}],
    )
    print(response.choices[0].message.content)


if __name__ == '__main__':
    oai_client_with_openai()
    oai_client_with_azure()
