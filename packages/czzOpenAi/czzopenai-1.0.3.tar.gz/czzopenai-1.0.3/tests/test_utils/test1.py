from openai import OpenAI



def aaa():
    client = OpenAI(
        api_key="sk-CwTTksdjGSbhjQJvEdFe3eF4767a435aA10134172735D716",
        base_url="https://api.cpdd666.cn/v1",
    )

    completion = client.chat.completions.create(
        model="claude-3-5-sonnet-20240620",
        stream=False,
        # model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "你好"}
        ]
    )

    print(completion)


if __name__ == '__main__':
    aaa()