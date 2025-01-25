
import wikipediaapi
from .tools import Tool

class WikipediaTool(Tool):
    def __init__(self, topic ,language="en" ):
        """
        Initialize the Wikipedia tool with a specified language.
        Default language is English.
        """
        self.wiki = wikipediaapi.Wikipedia(user_agent = "english" )
        self.topic =topic


    def use(self,agent):
        """
        Fetch the summary of a given topic from Wikipedia.

        Parameters:
        - topic (str): The topic to search for on Wikipedia.

        Returns:
        - str: A summary of the topic or an appropriate error message.
        """
        page = self.wiki.page(self.topic)

        # Check if the page exists
        if page.exists():
            print(f"Title: {page.title}")
            summary =  f"Summary: {page.summary[:1000]}"   # First 500 characters of the summary
            summary_end = "...." if len(page.summary)>1000 else ""
            summary = summary + summary_end

            insights = agent.model_instance.generate(
            name=agent.name,
            llm=agent.llm,
            work=agent.work,
            role=agent.role,
            context=summary
        )
            return insights
        else:
            return (f"The page '{self.topic}' does not exist.")