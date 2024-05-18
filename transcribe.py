from youtube_transcript_api import YouTubeTranscriptApi

def transcribe_video(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ''
        for segment in transcript:
            text += segment['text'] + '\n'
        return text
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def save_to_txt(text, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Transcript saved to {filename} successfully!")
    except Exception as e:
        print(f"Error saving transcript: {str(e)}")

if __name__ == "__main__":
    video_id = "yYa7ppvMbos"
    transcript = transcribe_video(video_id)
    if transcript:
        save_to_txt(transcript, f"{video_id}_transcript.txt")
