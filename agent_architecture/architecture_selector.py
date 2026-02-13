def select_architecture(parsed_goal):
    labels = parsed_goal['labels']
    if "social_media_monitoring" in labels:
        return {
            "agent_type": "monitoring_and_analysis_agent",
            "memory_system": "hybrid_memory",
            "tools": ["twitter_api_client", "sentiment_analyzer", "pdf_generator"]
        }
    elif "customer_service" in labels:
        return {
            "agent_type": "customer_support_agent",
            "memory_system": "episodic_memory",
            "tools": ["chat_api", "knowledge_base"]
        }
    else:
        return {
            "agent_type": "generic_agent",
            "memory_system": "working_memory",
            "tools": []
        }

if __name__ == "__main__":
    sample_parsed = {
        "labels": ["social_media_monitoring", "sentiment_analysis", "report_generation"]
    }
    architecture = select_architecture(sample_parsed)
    print("Selected Architecture:", architecture)
