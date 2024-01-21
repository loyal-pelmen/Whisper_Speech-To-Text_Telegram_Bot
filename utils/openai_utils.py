from openai import OpenAI
from httpx import Client as web
from config import PROXY


async def transcribe_audio(audio_file, token: str, proxy: str = None):

    if proxy == '':
        client = OpenAI(
            api_key=token
        )
    else:
        client = OpenAI(
            api_key=token,
            http_client=web(proxy=proxy)
        )

    r = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        timeout=15)

    return dict(r)["text"]  # type: ignore
