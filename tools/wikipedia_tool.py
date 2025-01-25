
import wikipediaapi
from .tools import Tool

class WikipediaTool(Tool):
    def __init__(self, topic, language="en"):
        self.wiki = wikipediaapi.Wikipedia(user_agent="english")
        self.topic = topic

    def use(self, agent):
        page = self.wiki.page(self.topic)

        if page.exists():
            print(f"Title: {page.title}")
            summary = f"Summary: {page.summary[:1000]}"
            summary_end = "...." if len(page.summary) > 1000 else ""
            summary = summary + summary_end
            return summary
        else:
            return f"The page '{self.topic}' does not exist."
