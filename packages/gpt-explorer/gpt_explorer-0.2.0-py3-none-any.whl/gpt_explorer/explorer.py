import re
from typing import List, Tuple
import logging

import requests
from bs4 import BeautifulSoup
from googlesearch import search
import openai


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
_log = logging.getLogger("explorer_logger")
_log.setLevel(logging.DEBUG)


def explore(query: str):
    return Explorer.explore(query)

def explore_with_ref(query: str):
    return Explorer.explore_with_ref(query)

def set_resource_limit(resource_limit: int):
    Explorer.resource_limit = resource_limit

def set_request_timeout(request_timeout: float):
    Explorer.request_timeout = request_timeout

def set_openai_api_key(openai_api_key: str):
    Explorer.openai_api_key = openai_api_key

def set_openai_gpt_model(openai_gpt_model: str):
    models = [
        "gpt-3.5-turbo",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4o-mini"
    ]
    if openai_gpt_model in models:
        Explorer.openai_gpt_model = openai_gpt_model
    
    else:
        _log.debug(f"The {openai_gpt_model} is not support by Explorer!")


class Explorer:
    openai_api_key = ""
    openai_gpt_model = "gpt-3.5-turbo" # support gpt-3.5-turbo, gpt-4-turbo, gpt-4o, and gpt-4o-mini
    resource_limit = 3
    request_timeout=10.0

    @staticmethod
    def fetch_search_results(query):
        search_results = list(search(query, num_results=Explorer.resource_limit))
        return search_results

    @staticmethod
    def get_text_from_url(url):
        response = requests.get(url, timeout=Explorer.request_timeout, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text()
        else:
            return ""

    @staticmethod
    def process_with_openai(text_content, user_ask):
        if Explorer.openai_api_key == "":
            return ""
        
        openai.api_key = Explorer.openai_api_key

        sys_text = f"""
            Answer the question based on the context below.
            Add "[tag.language.<google_language_code>]" to the end of the response \
            by replacing <google_language_code> which the google translate code that correspond to the output text.
            Keep the answer short and concise. Respond \"Information not found\" if not sure about the answer.

            Context: {text_content}
            """
        
        response = openai.ChatCompletion.create(
            model=Explorer.openai_gpt_model,
            messages=[
                {"role": "system", "content": sys_text},
                {"role": "user", "content": user_ask}
            ]
        )
        return response['choices'][0]['message']['content']
    
    @staticmethod
    def filter_tags(input_string: str) -> Tuple[str, bool, List[str]]:
        regex = r'\[tag\.(.+?)]'
        matches = re.findall(regex, input_string)
        found_match = len(matches) > 0
        filtered_string = re.sub(regex, '', input_string)
        return filtered_string, found_match, matches
    
    @staticmethod
    def process_search(query, is_with_ref = False):
        links = Explorer.fetch_search_results(query)
        
        results = []
        for i, link in enumerate(links):
            text_content = Explorer.get_text_from_url(link)
            processed_result = Explorer.process_with_openai(text_content, query)
            text_only, found_match, matches = Explorer.filter_tags(processed_result.replace("[[\"tag.", "").replace("\"]]", ""))
            language_code = []
            for lang_code in matches:
                language_code.append(lang_code.replace("language.", ""))
            if is_with_ref:
                results.append({
                    "ref": link,
                    "language_code": language_code,
                    "result": text_only
                })
            
            else:
                results.append({
                    "language_code": language_code,
                    "result": text_only
                })

            if processed_result.find("Information not found") == -1:
                break
            
        return results
    
    @staticmethod
    def explore_with_ref(query):
        try:
            results = Explorer.process_search(query, True)
            for result in results:
                if "result" in result:
                    if result["result"].find("Information not found") == -1:
                        return result
        
        except Exception as e:
            _log.error(f"explore_with_ref error {e}")
        
        return {}

    @staticmethod
    def explore(query):
        try:
            results = Explorer.process_search(query)
            for result in results:
                if "result" in result:
                    if result["result"].find("Information not found") == -1:
                        return result
        
        except Exception as e:
            _log.error(f"explore error {e}")
        
        return {}


if __name__ == "__main__":
    # Test error keyword "About abgel"
    _log.debug("You cannot execute this module directly! module exited!")
    exit()
    # set_openai_api_key("")
    set_openai_gpt_model("gpt-4o-mini")
    search_query = input("Enter your search query: ")
    output = explore(search_query)
    print(output)
