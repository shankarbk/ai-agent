from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

# Initialize the Bedrock AgentCore wrapper
app = BedrockAgentCoreApp()

# Use Amazon Nova Sonic
model = BedrockModel(model_id="amazon.nova-sonic-v1:0")

# Define the agent logic
agent = Agent(
    model=model,
    system_prompt="You are a helpful, concise AI assistant. Answer general user prompts accurately."
)

# Production entrypoint for the AWS Runtime
@app.entrypoint
def invoke(payload: dict):
    user_prompt = payload.get("prompt", "Hello!")
    response = agent(user_prompt)
    
    return {
        "result": str(response)
    }