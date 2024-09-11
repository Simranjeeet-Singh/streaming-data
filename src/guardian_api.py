import requests

def get_guardian_articles(api_key, search_term, date_from=None, page_size=10):
    """
    Fetches articles from the Guardian API based on a search term and optional date.
    
    Args:
        api_key (str): Your Guardian API key.
        search_term (str): Search term for querying articles.
        date_from (str, optional): Date from which to filter articles (format: YYYY-MM-DD). Defaults to None.
        page_size (int, optional): The number of articles to fetch. Defaults to 10.
    
    Returns:
        list: A list of articles in JSON format.
    """
    url = "https://content.guardianapis.com/search"
    params = {
        'q': search_term,
        'from-date': date_from,
        'api-key': api_key,
        'page-size': page_size
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get('response', {}).get('results', [])
    else:
        raise Exception(f"Guardian API request failed with status code {response.status_code}")
