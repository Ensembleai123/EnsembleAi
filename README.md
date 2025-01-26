
# EnsembleAI

EnsembleAI is a framework for building intelligent agents that can perform various tasks such as summarizing Wikipedia articles, analyzing YouTube transcripts, scraping web pages, Advanced Image Analysis and much more.

## Features

- Wikipedia Summarizer
- YouTube Transcript Analysis
- Web Scraper
- Image Analysis
- Retrieval-Augmented Generation (RAG)
- Extensive Multiagent Interaction
- Customizable Agent Workflow Pipelines

## Installation

```bash
pip install ensembleai
```

## Usage

```python
from ensembleai.agents import Agent
from ensembleai.environments import Environment
from ensembleai.tools import WikipediaTool , ImageAnalysisTool , WebScrapingTool , RAGTool , YouTubeTranscriptTool
from ensembleai.models import LLMModel


# Initialize models and tools
model = LLMModel(name="test-model", api_key="your-api-key")
youtube_tool = YouTubeTranscriptTool(api_key="your-youtube-api-key", keyword="your-keyword") # add 'channel_name' for specific channel search.
wikipedia_tool = WikipediaTool(topic="your-topic")
image_tool = ImageAnalysisTool(text="your-text", urls=["your-image-urls]")
webscraper_tool = WebScrapingTool(urls=["your-urls"])
rag_tool = RAGTool(file_paths=["path/to/your/file.pdf"])

# Create agents
agent1 = Agent(name="Agent1", model_instance=model, role="role1", work="work1")
agent1.add_tool("youtube_transcript", youtube_tool)

agent2 = Agent(name="Agent2", model_instance=model, role="role2", work="work2")
agent2.add_tool("wikipedia", wikipedia_tool)

agent3 = Agent(name="Agent3", model_instance=model, role="role3", work="work3")
agent3.add_tool("image_analysis", image_tool)

agent4 = Agent(name="Agent4", model_instance=model, role="role4", work="work4")
agent4.add_tool("web_scraping", webscraper_tool)

agent5 = Agent(name="Agent5", model_instance=model, role="role5", work="work5")
agent5.add_tool("RAG", rag_tool)

# Define agent connections
agent1.give_to(agent2)
agent2.give_to(agent3)
agent3.give_to(agent4)
agent4.give_to(agent5)

# Create and start the environments
env = Environment(agents=[agent1, agent2, agent3, agent4, agent5])
env.start()
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
