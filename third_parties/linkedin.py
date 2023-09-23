import os
import requests


def scrape_linkedin_profile(linkedin_profile_url: str):
    """Scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    proxy_curl_api = os.getenv("PROXY_CURL_API_KEY")
    headers = {"Authorization": f"Bearer {proxy_curl_api}"}

    response = requests.get(
        api_endpoint,
        params={"linkedin_profile_url": linkedin_profile_url},
        headers=headers,
    )

    data = response.json()

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
