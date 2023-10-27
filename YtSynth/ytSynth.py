from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import assemblyai as aai
from api import API_KEY
from api import OPEN_AI_API_KEY
import openai
from docx import Document
from docx2pdf import convert

openai.api_key = OPEN_AI_API_KEY
openai.Model.list()
aai.settings.api_key = API_KEY

def get_summary_openai(transcript):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "make a note from given transcript, state a title of the transcription, state the most important points of the transcription, add to that note a detailed explanation to the scientific topics or subjects included in transcription: " + transcript}])
    return response.choices[0].message.content

def is_valid_lang(lang):
    available_languages = ["en", "en_au", "en_uk", "en_us", "es", "fr", "de", "it", "pt", "nl", "hi", "ja", "zh", "fi", "ko", "pl", "ru", "tr", "uk", "vi"]
    return lang in available_languages

def is_valid_youtube_url(url):
    try:
        yt = YouTube(url)
        return yt.title is not None
    except Exception:
        return False

def is_valid_file_format(file_format):
    available_types = ["docx", "pdf", "txt", "md"]
    return file_format in available_types

def create_note_file(file_format, note, file_name):
    if file_format == "docx":
        doc = Document()
        doc.add_paragraph(note)
        doc.save(file_name + ".docx")
    if file_format == "pdf":
        doc = Document()
        doc.add_paragraph(note)
        doc.save(file_name + ".docx")
        convert(file_name + ".docx")
        if os.path.exists(file_name + ".docx"):
            os.remove(file_name + ".docx")
    if file_format == "txt":
        with open(file_name + ".txt", "w") as file_obj:
            file_obj.write(note)
    #markdown...

def download_video(yt_link, lang, file_format):
    while True:
        if not is_valid_youtube_url(yt_link):
            print("Your YouTube link is wrong")
            yt_link = input("Please enter a valid YouTube link: ")
            continue
        if not is_valid_lang(lang):
            print("Language code provided is wrong or not supported")
            lang = input("Please enter a valid language code: ")
            continue
        if not is_valid_file_format(file_format):
            print("Given file format is wrong or not supported")
            file_format = input("Please enter a valid file format: ")
            continue
        youtube_obj = YouTube(yt_link)
        video_file = youtube_obj.video_id + ".mp4"
        audio_url = youtube_obj.video_id + ".mp3"
        stream = youtube_obj.streams.get_highest_resolution()
        stream.download(filename=video_file)
        return video_file, audio_url, youtube_obj.video_id,lang, file_format

def extract_audio(video_file, audio_url):
    video = VideoFileClip(video_file)
    video.audio.write_audiofile(audio_url, codec="mp3")
    video.close()

def transcribe_audio(audio_url, lang):
    cfg_transcription = aai.TranscriptionConfig(
        language_code=lang,
    )
    transcriber = aai.Transcriber(config=cfg_transcription)
    transcript = transcriber.transcribe(audio_url)
    if transcript.text == "none":
        print("Transcript not available")
        return None
    return transcript

def main():
    yt_link = input("YouTube link: ")
    yt_lang = input("Language of the video: ")
    file_format = input("Type of file for your note: ")
    video_file, audio_url, file_name, lang, correct_file_format = download_video(yt_link, yt_lang, file_format)
    if video_file and audio_url:
        extract_audio(video_file, audio_url)
        transcript = transcribe_audio(audio_url, lang)
        if transcript:
            note = get_summary_openai(transcript.text)
            create_note_file(correct_file_format, note, file_name)
            if os.path.exists(audio_url):
                os.remove(video_file)
                os.remove(audio_url)

if __name__ == "__main__":
    main()