# EnsembleAI Agents

## Overview
EnsembleAI is a framework that allows multiple AI agents to collaborate and perform various tasks using different tools and models. This example demonstrates how to initialize agents with different roles, equip them with tools, and link them together in a processing pipeline using an environment.

## Installation
To use the `ensembleai` library, ensure you have it installed:
```sh
pip install ensembleai
```

## Usage
### Import Necessary Modules
```python
from ensembleai.agents import Agent
from ensembleai.environments import Environment
from ensembleai.tools import WikipediaTool, ImageAnalysisTool, WebScrapingTool, RAGTool, YouTubeTranscriptTool
from ensembleai.models import LLMModel
```

### Initialize Models and Tools
```python
# Initialize the model
model = LLMModel(name="test-model", api_key="your-api-key")

# Initialize tools
youtube_tool = YouTubeTranscriptTool(api_key="your-youtube-api-key", keyword="your-keyword")  # Add 'channel_name' for specific channel search.
wikipedia_tool = WikipediaTool(topic="your-topic")
image_tool = ImageAnalysisTool(text="your-text", urls=["your-image-urls"])
webscraper_tool = WebScrapingTool(urls=["your-urls"])
rag_tool = RAGTool(file_paths=["path/to/your/file.pdf"])
```

### Create Agents and Assign Tools
```python
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
```

### Define Agent Workflow
```python
agent1.give_to(agent2)
agent2.give_to(agent3)
agent3.give_to(agent4)
agent4.give_to(agent5)
```

### Create and Start the Environment
```python
env = Environment(agents=[agent1, agent2, agent3, agent4, agent5])
env.start()
```

## How It Works
- **Agent1** uses `YouTubeTranscriptTool` to fetch transcripts based on a keyword.
- **Agent2** uses `WikipediaTool` to gather topic-related information.
- **Agent3** utilizes `ImageAnalysisTool` to analyze images.
- **Agent4** employs `WebScrapingTool` to extract web-based information.
- **Agent5** leverages `RAGTool` for retrieval-augmented generation from PDFs.
- Agents communicate sequentially, passing results to the next agent in the pipeline.

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Feel free to open issues and submit pull requests.

## Contact
For any questions or suggestions, reach out to **[Your Name]** at **your.email@example.com**.
