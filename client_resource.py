import asyncio

from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    async with sse_client("http://127.0.0.1:3000/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            resources_result = await session.list_resources() #irá listar todos os recursos definidos em server.py
            print("Server resources: ", resources_result)

            print("resources_result.resources: ",  resources_result)
            
            for r in resources_result.resources:
               print(f" - {r.uri} (mime={r.mimeType})")
           
            content, mime_type = await session.read_resource("resource://food/pizza")
            print("\nRead 'resource://food/pizza':")
            print("  Content:", content)
            print("  MIME type:", mime_type)

            prompts_result = await session.list_prompts()
            print("\nServer prompts:")
            for p in prompts_result.prompts:
               print(f" - {p.name}: {p.description}")

            prompt_data = await session.get_prompt(
               "friendly_greeting", arguments={"name": "Alice"}
           )
            print("\nRetrieved 'friendly_greeting' prompt with argument name='Alice':")
            print("  Prompt messages:", prompt_data.messages)
#

if __name__ == "__main__":
    asyncio.run(main())