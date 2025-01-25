from .tools import Tool
import time
class ImageAnalysisTool(Tool):
    def __init__(self, text, urls):
        self.text = text
        self.urls = urls

    def use(self, agent):
        """
        Analyze the images from the given URLs with a 30-second gap between each reading.

        Parameters:
        - text (str): the text given to the client.

        Returns:
        - list: A list of descriptions for each given image.
        """

        descriptions = []

        for url in self.urls:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{self.text}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url
                            }
                        }
                    ]
                }
            ]

            completion = agent.model_instance.client.chat.completions.create(
                model=agent.llm,
                messages=messages,
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )

            descriptions.append(completion.choices[0].message)

            # Wait for 30 seconds before processing the next URL
            time.sleep(30)

        return descriptions