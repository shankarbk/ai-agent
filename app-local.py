from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

# Initialize the Bedrock AgentCore app wrapper
app = BedrockAgentCoreApp()

# Define the foundation model using Amazon Nova Sonic
# You can also use "amazon.nova-2-sonic-v1:0" for the latest version
model = BedrockModel(model_id="amazon.nova-sonic-v1:0")

# Create the agent with a general system prompt
agent = Agent(
    model=model,
    system_prompt="You are a helpful, concise AI assistant. Answer general user prompts accurately."
)

# Mark this function as the entrypoint for the AgentCore runtime
@app.entrypoint
def invoke(payload: dict):
    # Extract the user's prompt from the incoming payload
    user_prompt = payload.get("prompt", "Hello!")
    
    # Process the prompt through the agent
    response = agent(user_prompt)
    
    # Return the result as a JSON-serializable dictionary
    return {
        "result": str(response)
    }

if __name__ == "__main__":
    # Allows you to test locally before deploying
    app.run()