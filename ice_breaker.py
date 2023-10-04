from typing import Tuple

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from output_parsers import person_intel_parser, PersonIntel

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent

# Due to recent changes in Twitter api pricing model, twitter apis
# are not completely free depending on the country
# For this reason we are using a stub to emualte the scraper
from third_parties.twitter_with_stubs import scrape_user_tweets
from third_parties.linkedin import scrape_linkedin_profile


def ice_break(name: str) -> PersonIntel:
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username)

    summary_template = """
        given the Linkedin information {linkedin_information} and twitter information {twitter_information} about a person, I want you to create:
        1. A short summary
        2. 2 interesting facts about this person
        3. A topic that may interest them
        4. 2 creative Ice breakers to open a conversation with them
        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result = chain.run(linkedin_information=linkedin_data, twitter_information=tweets)

    return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    name = "Michael Scott Dunder Mifflin"
    print(ice_break(name=name))
