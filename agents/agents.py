import time
class Agent:
    def __init__(self, name, model_instance, role, work):
        self.name = name
        self.model_instance = model_instance
        self.llm = model_instance.name
        self.role = role
        self.work = work
        self.messages = []
        self.interaction_history = []
        self.outputs = []
        self.next_agents = []
        self.tools = {}

    def add_tool(self, tool_name, tool_instance):
        self.tools[tool_name] = tool_instance

    def use_tool(self, tool_name):
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} is not available.")
        return self.tools[tool_name].use(self)

    def start(self, context=""):
        print(f"{self.name} ({self.role}) is starting its task.")

        if "youtube_transcript" in self.tools:
            analysis = self.use_tool("youtube_transcript")
            self.outputs.append(analysis)
            print(f"{self.name} ({self.role}) output: {analysis}")
            time.sleep(60)
            return analysis

        if "wikipedia" in self.tools:
            summary = self.use_tool("wikipedia")
            self.outputs.append(summary)
            print(f"{self.name} ({self.role}) output: {summary}")
            time.sleep(60)
            return summary

        if "image_analysis" in self.tools:
            analysis = self.use_tool("image_analysis")
            self.outputs.append(analysis)
            print(f"{self.name} ({self.role}) output: {analysis}")
            time.sleep(60)
            return analysis

        if "web_scraping" in self.tools:
            summary = self.use_tool("web_scraping")
            self.outputs.append(summary)
            print(f"{self.name} ({self.role}) output: {summary}")
            time.sleep(60)
            return summary

        if "RAG" in self.tools:
            summary = self.use_tool("RAG")
            self.outputs.append(summary)
            print(f"{self.name} ({self.role}) output: {summary}")
            time.sleep(60)
            return summary

        else:
            response = self.model_instance.generate(self.name, self.llm, self.work, self.role, context)
            self.outputs.append(response)
            print(f"{self.name} ({self.role}) output: {response}")
            time.sleep(60)
            return response

    def give_to(self, *agents):
        self.next_agents.extend(agents)