import secrets
import warnings

import openai
from decouple import config


OPENAI_API_KEY = config("OPENAI_API_KEY", default="")

client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)


async def fetch_description(prompt: str, system_prompt: str) -> str:
    try:
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
    except openai.RateLimitError:
        warnings.warn("Please renew your OpenAI API key. Rate limit reached.")
        return "OpenAI API rate limit reached. Please try again later."

    return completion.choices[0].message.content


async def dummy_fetch_description(prompt: str, system_prompt: str) -> str:
    """
    I'm not paid enough (read: I'm not Musk) to make API calls to OpenAI. This will have to do.

    The real function is `fetch_description`. It works, trust me.
    """

    random_sign = secrets.token_urlsafe(12)
    return f"Imagine a world where the description is actually fetched from OpenAI - {random_sign}"
