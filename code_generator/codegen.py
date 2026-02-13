def generate_agent_code(architecture):
    agent_type = architecture.get("agent_type", "generic_agent")
    tools = architecture.get("tools", [])

    code = f'''
class {agent_type.capitalize()}:
    def __init__(self):
        self.tools = {tools}
    
    def run(self):
        print("Running {agent_type} with tools:", self.tools)

if __name__ == "__main__":
    agent = {agent_type.capitalize()}()
    agent.run()
'''
    return code

if __name__ == "__main__":
    architecture = {
        "agent_type": "monitoring_and_analysis_agent",
        "tools": ["twitter_api_client", "sentiment_analyzer", "pdf_generator"]
    }
    code = generate_agent_code(architecture)
    print(code)
