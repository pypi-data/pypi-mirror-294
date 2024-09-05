import os
from openai import AzureOpenAI

client = AzureOpenAI(
    # api_version=os.environ["AZURE_OPENAI_API_KEY"],
    # api_key=os.environ["AZURE_OPENAI_ENDPOINT"],
    # api_version=os.environ["OPENAI_API_VERSION"],
)


def get_completion_from_prompt(prompt: str) -> str:
    """
    Function that creates a post against openAI chatGPT service
    in Azure AI from a string prompt and returns the first and
    most deterministic response/completion.

    :param prompt: A string prompt to be sent to the chatGPT service

    :return: A string representation of the first answer proposed by the algorithm  # noqa E501
    """
    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        messages=messages,
        temperature=0,
    )

    return response.choices[0].message.content
