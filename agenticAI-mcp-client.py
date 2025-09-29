import sys
import json
import asyncio
import os
from dotenv import load_dotenv
import kong_pdk.pdk.kong as kong  # Kong Python PDK

# Agent libraries
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from agents.model_settings import ModelSettings

# Load environment variables (e.g. OPENAI_API_KEY)
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Plugin schema
Schema = [
    {"instructions": {"type": "string"}},
    {"mcp_servers": {"type": "array", "elements": {"type": "string"}}},
    {"urls": {"type": "array", "elements": {"type": "string"}}},
    {"authorization": {"type": "string"}},
]

version = "0.3.0"
priority = 0


class Plugin:
    def __init__(self, config):
        self.config = config

    def access(self, kong_instance):
        instructions = self.config.get("instructions", "")
        mcp_servers = self.config.get("mcp_servers", ["Fraud MCP Server"])
        urls = self.config.get("urls", ["http://localhost:4000/mcp"])
        authorization = self.config.get("authorization", "")

        kong_instance.log.info(f"[agenticAI-mcp-client] Instructions: {instructions}")
        kong_instance.log.info(f"[agenticAI-mcp-client] MCP servers: {mcp_servers}, URLs: {urls}")

        # --- Capture request payload ---
        body, err = kong_instance.request.get_raw_body()
        if err:
            kong_instance.log.err(f"[agenticAI-mcp-client] Error reading request body: {err}")
            payload = {}
        else:
            try:
                payload = json.loads(body) if body else {}
            except json.JSONDecodeError:
                kong_instance.log.err("[agenticAI-mcp-client] Non-JSON payload received")
                payload = {"raw": body.decode("utf-8") if isinstance(body, bytes) else str(body)}

        # ✅ Message comes only from payload
        message = json.dumps({"payload": payload})

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            agent_response = loop.run_until_complete(
                self.run_agent_logic(message, instructions, mcp_servers, urls, authorization)
            )
        except Exception as e:
            kong_instance.log.err(f"[agenticAI-mcp-client] Error in agent logic: {e}")
            agent_response = "Agent execution failed."

        # --- Send response back to client ---
        kong_instance.response.exit(
            200,
            json.dumps({"agent_response": agent_response}),
            {"Content-Type": "application/json"},
        )

    async def run_agent_logic(self, message, instructions, mcp_servers, urls, authorization):
        if len(mcp_servers) != len(urls):
            raise ValueError("mcp_servers and urls must be the same length")

        servers = []
        for name, url in zip(mcp_servers, urls):
            server = MCPServerStreamableHttp(
                name=name,
                params={
                    "url": url,
                    "headers": {"Authorization": authorization},
                },
            )
            await server.__aenter__()
            servers.append(server)

        try:
            agent = Agent(
                name="Assistant",
                instructions=instructions,
                mcp_servers=servers,
                model_settings=ModelSettings(tool_choice="required"),
            )
            result = await Runner.run(starting_agent=agent, input=message)

            if not result.final_output:
                raise ValueError("Agent did not return a final_output")

            return result.final_output
        finally:
            for server in servers:
                await server.__aexit__(None, None, None)


# Dump plugin schema if Kong asks
if len(sys.argv) > 1 and sys.argv[1] in ("--dump", "--dump-all-plugins"):
    print(
        json.dumps(
            [
                {
                    "name": "agenticAI-mcp-client",
                    "version": version,
                    "priority": priority,
                    "phases": ["access"],
                    "schema": Schema,
                }
            ]
        )
    )
    sys.exit(0)

