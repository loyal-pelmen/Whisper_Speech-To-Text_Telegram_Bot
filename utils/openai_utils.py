import openai



async def transcribe_audio(audio_file):
    r = await openai.Audio.atranscribe("whisper-1", audio_file, timeout=15)
    return r["text"] # type: ignore