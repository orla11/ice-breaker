from wrappers.serpapi_wrapper import CustomSerpAPIWrapper


def get_profile_url(text: str) -> str:
    """Searches for social profile pages"""
    search = CustomSerpAPIWrapper()
    res = search.run(f"{text}")
    return res
