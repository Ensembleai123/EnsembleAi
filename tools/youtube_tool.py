
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from .tools import Tool

class YouTubeTranscriptTool(Tool):
    def __init__(self, api_key, keyword, channel_name=None):
        self.api_key = api_key
        self.channel_name = channel_name
        self.keyword = keyword

    def use(self, agent):
        youtube = build('youtube', 'v3', developerKey=self.api_key)

        if self.channel_name:
            channel_response = youtube.search().list(
                q=self.channel_name,
                part='snippet',
                type='channel',
                maxResults=1
            ).execute()

            if not channel_response['items']:
                return "Channel not found!"

            channel_id = channel_response['items'][0]['id']['channelId']

            search_response = youtube.search().list(
                channelId=channel_id,
                q=self.keyword,
                part='snippet',
                type='video',
                maxResults=1,
                order='relevance'
            ).execute()
        else:
            search_response = youtube.search().list(
                q=self.keyword,
                part='snippet',
                type='video',
                maxResults=1,
                order='viewCount'
            ).execute()

        if not search_response['items']:
            return "No videos found for the keyword!"

        video = search_response['items'][0]
        video_id = video['id']['videoId']

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        except TranscriptsDisabled:
            return "Transcript is disabled for this video."
        except NoTranscriptFound:
            return "No transcript found for this video."
        except Exception as e:
            return f"An error occurred: {e}"

        transcript_text = " ".join(entry["text"] for entry in transcript[100:300])
        analysis_prompt = (
            f"Analyze the following transcript and provide key insights and summary:\n\n{transcript_text}. "
            "Do not give the text itself."
        )

        insights = agent.model_instance.generate(
            name=agent.name,
            llm=agent.llm,
            work=agent.work,
            role=agent.role,
            context=analysis_prompt
        )
        return insights
