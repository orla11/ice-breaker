from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType

from tools.tools import get_profile_url


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = """
        Given the full name {name_of_person} of a person, I want you to find the url to their Twitter Page URL, and extract from it their username.
        In your Final answer only the person username.
    """

    tools_for_agent = [
        Tool(
            name="Crawl Google for Twitter Page URL",
            func=get_profile_url,
            description="Useful for when you need to find the Twitter Page URL",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    twitter_username = agent.run(prompt_template.format_prompt(name_of_person=name))

    return twitter_username
