"""
Web Scraper for Live Game Search
Uses Selenium WebDriver and BeautifulSoup to search for games on external sites
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import requests
from typing import Dict, List, Optional


def web_driver():
    """
    Initialize and configure Chrome WebDriver with headless options
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--verbose")
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1200")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def search_game_metacritic(game_name: str) -> Dict:
    """
    Search for a game on Metacritic using Selenium
    
    Args:
        game_name (str): Name of the game to search
        
    Returns:
        Dict: Dictionary containing game information and page source
    """
    driver = web_driver()
    results = {
        'success': False,
        'game_name': game_name,
        'url': '',
        'page_source': '',
        'games_found': []
    }
    
    try:
        # Metacritic search URL (parameterized)
        search_url = f"https://www.metacritic.com/search/{game_name.replace(' ', '%20')}/"
        results['url'] = search_url
        
        driver.get(search_url)
        time.sleep(5)  # Wait for page to load
        
        # Get page source
        page_source = driver.page_source
        results['page_source'] = page_source
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Try multiple selector patterns as Metacritic structure may vary
        game_items = []
        
        # Try common selectors
        selectors = [
            ('div', {'class': 'result_wrap'}),
            ('div', {'class': 'search_result'}),
            ('li', {'class': 'result'}),
            ('div', {'class': 'c-finderProductCard'}),
        ]
        
        for tag, attrs in selectors:
            items = soup.find_all(tag, attrs)
            if items:
                game_items = items
                break
        
        # If no specific items found, try to find any game-related content
        if not game_items:
            # Look for any links or text that might contain game info
            game_items = soup.find_all(['div', 'li', 'article'], limit=10)
        
        for item in game_items[:5]:  # Limit to first 5 results
            try:
                # Try multiple ways to extract game information
                title = None
                score = None
                platform = None
                
                # Try to find title
                for selector in ['h3', 'h2', 'a', 'span']:
                    if not title:
                        title = item.find(selector)
                        if title and len(title.text.strip()) > 2:
                            break
                
                # Try to find score
                score = item.find('div', class_='metascore_w') or \
                        item.find('div', class_='c-siteReviewScore') or \
                        item.find(lambda tag: tag.name == 'div' and 'score' in tag.get('class', []))
                
                # Try to find platform
                platform = item.find('span', class_='platform') or \
                          item.find('div', class_='platform')
                
                if title:  # Only add if we found at least a title
                    game_info = {
                        'title': title.text.strip() if title else 'N/A',
                        'score': score.text.strip() if score else 'N/A',
                        'platform': platform.text.strip() if platform else 'N/A'
                    }
                    results['games_found'].append(game_info)
            except Exception as e:
                continue
        
        results['success'] = True
        
    except Exception as e:
        results['error'] = str(e)
    finally:
        driver.quit()
    
    return results


def search_game_igdb(game_name: str) -> Dict:
    """
    Search for a game on IGDB using Selenium with form submission
    
    Args:
        game_name (str): Name of the game to search
        
    Returns:
        Dict: Dictionary containing game information
    """
    driver = web_driver()
    results = {
        'success': False,
        'game_name': game_name,
        'url': '',
        'page_source': '',
        'games_found': []
    }
    
    try:
        # Navigate to IGDB
        driver.get("https://www.igdb.com/")
        time.sleep(3)
        
        # Find search box and enter game name (try multiple selectors)
        search_box = None
        search_selectors = [
            (By.NAME, "search"),
            (By.ID, "search"),
            (By.CSS_SELECTOR, "input[type='search']"),
            (By.CSS_SELECTOR, "input[placeholder*='Search']"),
            (By.XPATH, "//input[@type='search']"),
        ]
        
        for by_type, selector in search_selectors:
            try:
                search_box = driver.find_element(by_type, selector)
                if search_box:
                    break
            except NoSuchElementException:
                continue
        
        if search_box:
            search_box.clear()
            search_box.send_keys(game_name)
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)  # Wait for results to load
        else:
            # If search box not found, use direct URL
            search_url = f"https://www.igdb.com/search?type=1&q={game_name.replace(' ', '+')}"
            driver.get(search_url)
            time.sleep(5)
        
        # Get page source
        page_source = driver.page_source
        results['page_source'] = page_source
        results['url'] = driver.current_url
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Try multiple selector patterns
        game_cards = []
        card_selectors = [
            ('div', {'class': 'game-card'}),
            ('div', {'class': 'card'}),
            ('article', {}),
            ('div', {'class': 'result'}),
        ]
        
        for tag, attrs in card_selectors:
            cards = soup.find_all(tag, attrs)
            if cards:
                game_cards = cards
                break
        
        for card in game_cards[:5]:
            try:
                # Try to find title
                title = card.find('h3') or card.find('h2') or card.find('a')
                rating = card.find('div', class_='rating') or card.find('span', class_='score')
                
                if title:
                    game_info = {
                        'title': title.text.strip() if title else 'N/A',
                        'rating': rating.text.strip() if rating else 'N/A'
                    }
                    results['games_found'].append(game_info)
            except Exception as e:
                continue
        
        results['success'] = True
        
    except Exception as e:
        results['error'] = str(e)
    finally:
        driver.quit()
    
    return results


def search_game_google(game_name: str) -> Dict:
    """
    Search for a game on Google using Selenium (general search)
    
    Args:
        game_name (str): Name of the game to search
        
    Returns:
        Dict: Dictionary containing game information
    """
    driver = web_driver()
    results = {
        'success': False,
        'game_name': game_name,
        'url': '',
        'page_source': '',
        'games_found': []
    }
    
    try:
        # Google search URL
        search_query = f"{game_name} game review rating"
        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        results['url'] = search_url
        
        driver.get(search_url)
        time.sleep(3)
        
        # Get page source
        page_source = driver.page_source
        results['page_source'] = page_source
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Extract search results
        search_results = soup.find_all('div', class_='g')
        
        for result in search_results[:5]:
            try:
                title_elem = result.find('h3')
                snippet_elem = result.find('div', class_='VwiC3b')
                link_elem = result.find('a')
                
                if title_elem:
                    game_info = {
                        'title': title_elem.text.strip(),
                        'snippet': snippet_elem.text.strip() if snippet_elem else 'N/A',
                        'link': link_elem['href'] if link_elem and 'href' in link_elem.attrs else 'N/A'
                    }
                    results['games_found'].append(game_info)
            except Exception as e:
                continue
        
        results['success'] = True
        
    except Exception as e:
        results['error'] = str(e)
    finally:
        driver.quit()
    
    return results


def search_game_steam(game_name: str) -> Dict:
    """
    Search for a game on Steam using Selenium
    
    Args:
        game_name (str): Name of the game to search
        
    Returns:
        Dict: Dictionary containing game information
    """
    driver = web_driver()
    results = {
        'success': False,
        'game_name': game_name,
        'url': '',
        'page_source': '',
        'games_found': []
    }
    
    try:
        # Steam search URL
        search_url = f"https://store.steampowered.com/search/?term={game_name.replace(' ', '+')}"
        results['url'] = search_url
        
        driver.get(search_url)
        time.sleep(5)  # Wait for page to load
        
        # Get page source
        page_source = driver.page_source
        results['page_source'] = page_source
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Extract game results
        game_items = soup.find_all('a', class_='search_result_row')
        
        for item in game_items[:5]:
            try:
                title = item.find('span', class_='title')
                price = item.find('div', class_='search_price')
                review = item.find('span', class_='search_review_summary')
                release_date = item.find('div', class_='search_released')
                
                game_info = {
                    'title': title.text.strip() if title else 'N/A',
                    'price': price.text.strip() if price else 'N/A',
                    'reviews': review['data-tooltip-html'] if review and 'data-tooltip-html' in review.attrs else 'N/A',
                    'release_date': release_date.text.strip() if release_date else 'N/A',
                    'link': item['href'] if 'href' in item.attrs else 'N/A'
                }
                results['games_found'].append(game_info)
            except Exception as e:
                continue
        
        results['success'] = True
        
    except Exception as e:
        results['error'] = str(e)
    finally:
        driver.quit()
    
    return results


def search_game_rawg_api(game_name: str, api_key: Optional[str] = None) -> Dict:
    """
    Search for a game using RAWG API (recommended approach - faster and more reliable)
    
    Args:
        game_name (str): Name of the game to search
        api_key (str, optional): RAWG API key (get free key from https://rawg.io/apidocs)
        
    Returns:
        Dict: Dictionary containing game information
    """
    results = {
        'success': False,
        'game_name': game_name,
        'games_found': []
    }
    
    if not api_key:
        results['error'] = "RAWG API key is required. Get a free key at https://rawg.io/apidocs"
        return results
    
    try:
        # RAWG API endpoint
        base_url = "https://api.rawg.io/api/games"
        params = {
            'key': api_key,
            'search': game_name,
            'page_size': 5
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            for game in data.get('results', []):
                game_info = {
                    'title': game.get('name', 'N/A'),
                    'rating': game.get('rating', 'N/A'),
                    'released': game.get('released', 'N/A'),
                    'platforms': [p['platform']['name'] for p in game.get('platforms', [])],
                    'genres': [g['name'] for g in game.get('genres', [])],
                    'metacritic': game.get('metacritic', 'N/A'),
                    'background_image': game.get('background_image', '')
                }
                results['games_found'].append(game_info)
            
            results['success'] = True
        elif response.status_code == 401:
            results['error'] = "Invalid or missing API key. Get a free key at https://rawg.io/apidocs"
        else:
            results['error'] = f"API returned status code: {response.status_code}"
            
    except Exception as e:
        results['error'] = str(e)
    
    return results


def search_external_game(game_name: str, source: str = 'google', api_key: Optional[str] = None) -> Dict:
    """
    Main search function that routes to different search methods
    
    Args:
        game_name (str): Name of the game to search
        source (str): Search source ('google', 'metacritic', 'igdb', 'steam', 'rawg')
        api_key (str, optional): API key if using RAWG API
        
    Returns:
        Dict: Dictionary containing search results
    """
    if source.lower() == 'google':
        return search_game_google(game_name)
    elif source.lower() == 'steam':
        return search_game_steam(game_name)
    elif source.lower() == 'metacritic':
        return search_game_metacritic(game_name)
    elif source.lower() == 'igdb':
        return search_game_igdb(game_name)
    elif source.lower() == 'rawg':
        return search_game_rawg_api(game_name, api_key)
    else:
        return {
            'success': False,
            'error': f"Unknown source: {source}. Use 'google', 'steam', 'metacritic', 'igdb', or 'rawg'"
        }


def format_search_results(results: Dict) -> str:
    """
    Format search results for display
    
    Args:
        results (Dict): Search results dictionary
        
    Returns:
        str: Formatted string for display
    """
    if not results.get('success', False):
        return f"❌ Search failed: {results.get('error', 'Unknown error')}"
    
    output = f"🎮 Search Results for: **{results['game_name']}**\n\n"
    
    if not results['games_found']:
        output += "No games found."
        return output
    
    for idx, game in enumerate(results['games_found'], 1):
        output += f"**{idx}. {game.get('title', 'N/A')}**\n"
        
        for key, value in game.items():
            if key != 'title' and value != 'N/A':
                if isinstance(value, list):
                    output += f"   - {key.capitalize()}: {', '.join(map(str, value))}\n"
                else:
                    output += f"   - {key.capitalize()}: {value}\n"
        
        output += "\n"
    
    return output


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("Testing Game Web Scrapers")
    print("="*60)
    
    game_to_search = "Elden Ring"
    
    # Test Google Search
    print(f"\n1. Testing Google Search for '{game_to_search}'...")
    print("-"*60)
    results = search_external_game(game_to_search, source='google')
    print(format_search_results(results))
    
    # Test Steam Search
    print(f"\n2. Testing Steam Search for '{game_to_search}'...")
    print("-"*60)
    results = search_external_game(game_to_search, source='steam')
    print(format_search_results(results))
    
    # Test Metacritic Search
    print(f"\n3. Testing Metacritic Search for '{game_to_search}'...")
    print("-"*60)
    results = search_external_game(game_to_search, source='metacritic')
    print(format_search_results(results))
    
    print("\n" + "="*60)
    print("Testing complete!")
    print("="*60)
