import boto3
import json
import time

def deploy_agent():
    iam = boto3.client('iam')
    bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

    role_name = "BedrockAgentRole-Phase1"
    
    # 1. Create IAM Role with Bedrock Trust Policy
    print("Creating IAM Role...")
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "bedrock.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    try:
        role = iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(trust_policy))
        iam.attach_role_policy(RoleName=role_name, PolicyArn="arn:aws:iam::aws:policy/AmazonBedrockFullAccess")
        time.sleep(10)  # Allow time for IAM propagation
        role_arn = role['Role']['Arn']
    except iam.exceptions.EntityAlreadyExistsException:
        print("Role already exists. Fetching ARN...")
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']

    # 2. Create the Bedrock Agent
    print("Deploying Bedrock Agent...")
    agent_response = bedrock_agent.create_agent(
        agentName="Phase1Agent",
        foundationModel="amazon.nova-2-sonic-v1:0", 
        instruction="You are a helpful, concise AI assistant. Answer general user prompts accurately.",
        agentResourceRoleArn=role_arn,
        idleSessionTTLInSeconds=1800
    )
    agent_id = agent_response['agent']['agentId']

    # 3. Prepare Agent
    print(f"Preparing Agent: {agent_id}")
    bedrock_agent.prepare_agent(agentId=agent_id)
    time.sleep(5) 

    # 4. Create Alias
    print("Creating Agent Alias...")
    alias_response = bedrock_agent.create_agent_alias(
        agentId=agent_id,
        agentAliasName="prod"
    )
    alias_id = alias_response['agentAlias']['agentAliasId']

    print("\n--- DEPLOYMENT SUCCESSFUL ---")
    print(f"Agent ID: {agent_id}")
    print(f"Alias ID: {alias_id}")

if __name__ == "__main__":
    deploy_agent()