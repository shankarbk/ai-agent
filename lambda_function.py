import json
import os
import boto3

# Initialize the Bedrock Agent Runtime client
client = boto3.client('bedrock-agent-runtime')

def lambda_handler(event, context):
    try:
        # Parse incoming request from Lambda Function URL
        body_str = event.get('body', '{}')
        body = json.loads(body_str) if isinstance(body_str, str) else body_str
        
        user_prompt = body.get('prompt', 'Hello')
        # Session ID allows Bedrock to maintain conversation memory
        session_id = body.get('session_id', 'default-session-123') 
        
        agent_id = os.environ.get('AGENT_ID')
        alias_id = os.environ.get('ALIAS_ID')
        
        # Invoke the Bedrock Agent
        response = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=alias_id,
            sessionId=session_id,
            inputText=user_prompt
        )
        
        # Bedrock Agent returns an EventStream; parse the chunks
        completion = ""
        for event_chunk in response.get("completion"):
            if "chunk" in event_chunk:
                chunk = event_chunk["chunk"]
                completion += chunk["bytes"].decode()
                
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'response': completion})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }