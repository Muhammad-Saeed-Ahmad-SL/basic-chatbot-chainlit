import chainlit as cl
from my_secrets import Secrets
from agents import Agent, Runner, AsyncOpenAI, set_default_openai_api, set_tracing_disabled, OpenAIChatCompletionsModel
@cl.on_message
async def main(msg: cl.Message):
    secrets= Secrets()
    external_client = AsyncOpenAI(
                api_key=secrets.get_api_key(),
                base_url=secrets.get_api_base_url(),)
    set_tracing_disabled(True)
    set_default_openai_api(external_client)
    agent = Agent(
        name="Assistant",
        instructions="Answer the question as best as you can.",
        model=OpenAIChatCompletionsModel(
            model=secrets.get_api_model(),
            openai_client = external_client,
        ),
    )
    result = Runner.run_sync(starting_agent=agent, input=msg.content)
    message = cl.Message(content=result.final_output)
    await message.send()