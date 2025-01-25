class Environment:
    def __init__(self, agents, num_rounds=1):
        self.agents = agents
        self.execution_order = []
        self.num_rounds = num_rounds

    def validate_pipeline(self):
        visited = set()

        def dfs(agent):
            if agent in visited:
                return
            visited.add(agent)
            for next_agent in agent.next_agents:
                dfs(next_agent)
            self.execution_order.append(agent)

        for agent in self.agents:
            if agent not in visited:
                dfs(agent)

        self.execution_order.reverse()
        for agent in self.execution_order:
            print(agent.name)

    def start(self):
        self.validate_pipeline()
        agent_contexts = {agent: "" for agent in self.agents}

        for round_num in range(1, self.num_rounds + 1):
            print(f"--- Starting Round {round_num} ---")
            for agent in self.execution_order:
                if self.num_rounds > 1 and round_num > 1:
                    context = agent_contexts[agent] + "\n".join(agent.outputs) + "\n"
                else:
                    context = agent_contexts[agent]

                output = agent.start(context)
                agent_contexts[agent] += output + "\n"

                for next_agent in agent.next_agents:
                    agent_contexts[next_agent] += output + "\n"
            print(f"--- End of Round {round_num} ---\n")