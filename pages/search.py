import streamlit as st
import sys
import os

# Add parent directory to path to import web.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from web import search_external_game, format_search_results
    WEB_SCRAPER_AVAILABLE = True
except ImportError:
    WEB_SCRAPER_AVAILABLE = False


def search_page():
    """Live Game Search - Search for games not in the database"""
    
    # Apply consistent styling with rest of app
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #4b9cd3;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1.5rem;
        }
        iframe {
            border: 1px solid #ddd;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🔍 Live Game Search</h1>', unsafe_allow_html=True)
    
    if not WEB_SCRAPER_AVAILABLE:
        st.error("Web scraper module not available. Please ensure web.py exists and dependencies are installed.")
        st.info("Install required packages: `pip install selenium webdriver-manager beautifulsoup4 requests`")
        return
    
    # Search Section
    st.markdown("### Search for Games on Metacritic")
    
    game_name = st.text_input(
        "Enter Game Name",
        placeholder="e.g., The Last of Us, Cyberpunk 2077, Elden Ring...",
        key="game_search_input"
    )
    c1,c2,c3=st.columns(3)
    search_button = c2.button("Search Game", use_container_width=True,type="primary")
    
    # Display search results
    if search_button and game_name:
        with st.spinner(f"Searching Metacritic for '{game_name}'..."):
            try:
                results = search_external_game(game_name, source='metacritic')
                
                if results.get('success') and results.get('games_found'):
                    st.success("Results found")
                    
                    st.markdown("---")
                    
                    # Get URLs from results
                    urls_to_display = []
                    for game in results['games_found']:
                        if 'link' in game and game['link'] and game['link'] != 'N/A' and game['link'].startswith('http'):
                            urls_to_display.append({
                                'title': game.get('title', 'Unknown'),
                                'url': game['link']
                            })
                    
                    if urls_to_display:
                        # Let user select which game to view
                        selected_game = st.selectbox(
                            "Select a game to preview:",
                            options=[g['title'] for g in urls_to_display],
                            key="selected_game_iframe"
                        )
                        
                        # Find the URL for selected game
                        selected_url = next(g['url'] for g in urls_to_display if g['title'] == selected_game)
                        
                        # Display iframe
                        st.components.v1.iframe(selected_url, height=800, scrolling=True)
                        
                    else:
                        # Show search results page directly in iframe
                        if results.get('url'):
                            st.components.v1.iframe(results['url'], height=800, scrolling=True)
                    
                    # Show raw data option
                    with st.expander("View Raw Data"):
                        st.json(results)
                
                elif results.get('success'):
                    st.warning(f"No games found for '{game_name}' on Metacritic. Try a different search term.")
                else:
                    error_msg = results.get('error', 'Unknown error occurred')
                    st.error(f"Search failed: {error_msg}")
                    
                    st.info("Suggestions:\n- Check your spelling\n- Try a different search term\n- Make sure you have internet connection")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Make sure all dependencies are installed and you have a stable internet connection.")
    
    elif search_button:
        st.warning("Please enter a game name to search.")
    
    # Info section
    with st.expander("About Live Search"):
        st.markdown("""
        ### How It Works
        
        Search for games on Metacritic and view game pages directly in this app.
        
        **Features:**
        - Live game search from Metacritic
        - View game ratings and scores
        - Browse game pages in embedded view
        - Direct links to open in browser
        
        **Note:** Enter the exact or partial game title for best results.
        """)


if __name__ == "__main__":
    search_page()
