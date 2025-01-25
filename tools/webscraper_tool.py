
import requests
from bs4 import BeautifulSoup
from .tools import Tool

class WebScrapingTool(Tool):
    def __init__(self, urls):
        """
        Scrapes webpages to extract the title, meta description, headings, and paragraphs.

        Parameters:
        - urls (list of str): The list of URLs of the webpages to scrape.

        Returns:
        - str: A formatted string containing the scraped data, or an error message if the scrape fails.
        """
        self.urls = urls

    def use(self, agent):
        """
        Wrapper method to provide a simple interface for scraping webpages.

        Parameters:
        - urls (list of str): The list of URLs of the webpages to scrape.

        Returns:
        - str: Scraped webpage data as a formatted string.
        """
        combined_result = ""

        for url in self.urls:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # Safe extraction with error handling
                title = soup.title.string.strip() if soup.title else 'No title found'
                meta = soup.find('meta', attrs={'name': 'description'})
                meta_description = meta['content'] if meta and 'content' in meta.attrs else 'No description found'

                # Safely get headings
                headings = {}
                for tag in ['h1', 'h2', 'h3']:
                    elements = soup.find_all(tag)
                    if elements:
                        headings[tag] = [h.get_text(strip=True) for h in elements]

                paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]

                # Format the result as a string
                result = f"URL: {url}\n"
                result += f"Title: {title}\n"
                result += f"Meta Description: {meta_description}\n"
                result += "Headings:\n"
                for level, texts in headings.items():
                    result += f"  {level.upper()}: {', '.join(texts)}\n"
                result += "Paragraphs:\n"
                result += "\n".join(paragraphs)
                result += "\n\n"

                combined_result += result

                # Wait for 30 seconds before processing the next URL
                time.sleep(30)

            except requests.exceptions.RequestException as e:
                combined_result += f"Error during the request for {url}: {e}\n\n"
            except Exception as e:
                combined_result += f"An unexpected error occurred for {url}: {e}\n\n"

        insights = agent.model_instance.generate(
            name=agent.name,
            llm=agent.llm,
            work=agent.work,
            role=agent.role,
            context=combined_result
        )
        return insights