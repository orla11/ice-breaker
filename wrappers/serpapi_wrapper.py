from langchain.utilities import SerpAPIWrapper


class CustomSerpAPIWrapper(SerpAPIWrapper):
    def __init__(self):
        super(CustomSerpAPIWrapper, self).__init__()

    @staticmethod
    def _process_response(res: dict):
        """Process response from SerpAPI"""
        snippets = []
        if "knowledge_graph" in res.keys():
            knowledge_graph = res["knowledge_graph"]
            title = knowledge_graph["title"] if "title" in knowledge_graph else ""
            if "description" in knowledge_graph.keys():
                snippets.append(knowledge_graph["description"])
            for key, value in knowledge_graph.items():
                if (
                    type(key) == str
                    and type(value) == str
                    and key not in ["title", "description"]
                    and not key.endswith("_stick")
                    and not key.endswith("_link")
                    and not value.startswith("http")
                ):
                    snippets.append(f"{title} {key}: {value}.")
        if "organic_results" in res.keys():
            first_organic_result = res["organic_results"][0]
            if "snippet" in first_organic_result.keys():
                snippets.append(first_organic_result["link"])
            elif "snippet_highlighted_words" in first_organic_result.keys():
                snippets.append(first_organic_result["snippet_highlighted_words"])
            elif "rich_snippet" in first_organic_result.keys():
                snippets.append(first_organic_result["rich_snippet"])
            elif "rich_snippet_table" in first_organic_result.keys():
                snippets.append(first_organic_result["rich_snippet_table"])
            elif "link" in first_organic_result.keys():
                snippets.append(first_organic_result["link"])
        if "buying_guide" in res.keys():
            snippets.append(res["buying_guide"])
        if "local_results" in res.keys() and "places" in res["local_results"].keys():
            snippets.append(res["local_results"]["places"])

        if len(snippets) > 0:
            return str(snippets)
        else:
            return "No good search result found"
