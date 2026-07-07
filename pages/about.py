import streamlit as st

def about_page():
    st.markdown("""
# TechWill x Game - Game Recommendation System 🎮

![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
                
A sophisticated content-based game recommendation system with advanced features including:
- Intelligent recommendations based on existing games or custom features
- Live web scraping for external game information
- Interactive data visualization and exploration
- Real-time visitor tracking

## Key Features ✨

### 🎯 Dual Recommendation Engine
- **By Game**: Select from 16,000+ games in database
- **By Features**: Create custom game profile with attributes
- **Two Algorithms**: 
  - KNN (K-Nearest Neighbors with Euclidean distance)
  - Cosine Similarity
- **Adjustable Results**: Get 1-10 recommendations

### 📊 Interactive Data Exploration
- **Visual Analytics**: 
  - Genre popularity trends
  - Release timeline analysis
  - Platform distribution
  - Sales and ratings insights
- **Interactive Catalog**: 
  - Browse 16,000+ games
  - Filter by genre, platform, rating, year
  - Search functionality
  - Detailed game metadata

### 🔍 Live Game Search
- **Metacritic Integration**: Web scraping powered by Selenium
- **Real-time Search**: Find games not in database
- **Embedded Preview**: View game pages directly in app

### 🎥 Video Tutorials
- **Step-by-step Guides**: Learn how to use all features
- **Local Video Support**: Fast loading from local storage

### 📈 Visitor Analytics
- **MySQL Integration**: Track site visitors
- **Real-time Stats**: View total visitor count
- **Database Management**: Automated visitor logging

### 🎨 Modern UI/UX
- **Custom Navigation Bar**: Streamlit-community-navigation-bar
- **Responsive Design**: Mobile-friendly interface
- **Interactive Charts**: Plotly visualizations
- **Custom Branding**: University project theme

## Project Structure 📂

```
GameRecommender/
├── data/
│   └── games.csv                       # 16,000+ game dataset
├── models/                             # Pre-trained ML models
│   ├── game_data_processed.pkl         # Processed game data
│   ├── game_names.pkl                  # List of game names
│   ├── cosine_sim_matrix.pkl           # Cosine similarity matrix
│   ├── game_recommender_knn_model.pkl  # KNN model
│   ├── minmax_scaler.pkl               # Feature scaler
│   └── one_hot_columns.pkl             # One-hot encoded columns
├── Videos/
│   └── video1.mp4                      # Tutorial video
├── pages/                              # Streamlit pages
│   ├── __init__.py
│   ├── home.py                         # Landing page
│   ├── recommend.py                    # Recommendation engine UI
│   ├── explore.py                      # Data visualization
│   ├── search.py                       # Live game search
│   ├── tutorial.py                     # Video tutorials
│   ├── about.py                        # This page
│   └── security_login.py               # Visitor tracking
├── .streamlit/
│   ├── config.toml                     # Theme configuration
│   └── secrets.toml                    # MySQL credentials
├── app.py                              # Main application & navigation
├── backend.py                          # ML functions & model loading
├── game_recommender.py                 # Core recommendation engine
├── web.py                              # Web scraping module
├── requirements.txt                    # Python dependencies
├── logo.gif                            # Animated logo
├── logo.svg                            # SVG logo
├── mdulogo.png                         # University logo
└── README.md
```

## Installation 🛠️

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aakash-test7/GameRecommender.git
   cd GameRecommender
   ```

2. **Set up Python environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  
   pip install -r requirements.txt
   ```

3. **Install ChromeDriver** (for web scraping):
   - Automatically handled by `webdriver-manager`
   - Ensures compatibility with your Chrome version

4. **Configure MySQL database** (optional for visitor tracking):
   - Create `.streamlit/secrets.toml` with MySQL credentials:
     ```toml
     [mysql]
     host = "host"
     user = "username"
     password = "********"
     port = 3306
     ```
   - Database and tables auto-created on first run

5. **Prepare data files**:
   - Ensure `data/games.csv` contains game dataset
   - Place pre-trained models in `models/` directory
   - Add tutorial video to `Videos/video1.mp4`

## Usage 🚀

1. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Navigation**:
   - **Home**: University project information and credits
   - **Recommend**: Get game recommendations
     - Choose between game-based or feature-based recommendations
     - Select KNN or Cosine Similarity algorithm
     - Adjust number of recommendations (1-10)
   - **Explore**: Interactive data visualization
     - View charts and statistics
     - Browse game catalog with filters
   - **Search**: Find games on Metacritic
     - Live web scraping
     - Embedded preview of game pages
   - **Tutorial**: Watch video guides
   - **About**: This page

3. **Using the Recommender**:
   
   **Option A: Game-based Recommendations**
   1. Click "Recommend by Game"
   2. Select a game from 16,000+ titles
   3. Choose recommendation method (KNN/Cosine)
   4. Set number of recommendations
   5. Click "Recommend"
   
   **Option B: Feature-based Recommendations**
   1. Click "Recommend by Features"
   2. Fill in game attributes:
      - Platform, Year, Genre
      - Sales data (NA, EU, JP, Other)
      - User Score, Rating, Publisher
   3. Choose recommendation method
   4. Get personalized recommendations

4. **Exploring Data**:
   - View genre popularity, release timelines, platform distribution
   - Filter games by genre, platform, year, rating
   - Search within the catalog
   - View detailed game information

5. **Live Search**:
   - Enter game name to search Metacritic
   - View results in embedded iframe
   - Discover games not in local database

## Configuration ⚙️

Customize the app by modifying `.streamlit/config.toml`:
```toml
[theme]
base = "light"
primaryColor = "#4b9cd3"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#31333f"
```

**Navigation Bar Customization:**
- Adjust colors, fonts, and layout in [app.py](app.py)
- Custom styling for hover and active states
- Mobile-responsive design

## Technical Details 🔧

### Machine Learning
- **Algorithms**: KNN (scikit-learn) and Cosine Similarity
- **Feature Engineering**:
  - Numerical features: MinMaxScaler normalization
  - Categorical features: One-hot encoding
  - Feature vector dimension: 100+ features
- **Data Processing**: Pandas for data manipulation
- **Model Persistence**: Joblib for serialization

### Web Technologies
- **Frontend**: Streamlit with custom CSS
- **Navigation**: streamlit-navigation-bar (v4.4.1)
- **Charts**: Plotly for interactive visualizations
- **Web Scraping**: 
  - Selenium WebDriver with ChromeDriver
  - BeautifulSoup4 for HTML parsing
  - Headless Chrome with custom user agents

### Database
- **System**: MySQL with PyMySQL connector
- **Schema**: Auto-created on first run
- **Features**: 
  - Visitor tracking with timestamps
  - Connection pooling
  - SSL support

### Performance Optimization
- **Caching**: Streamlit's @st.cache_resource and @st.cache_data
- **Local Storage**: Models loaded from local files (not cloud)
- **Lazy Loading**: Pages loaded on demand

## Dependencies 📦

```text
streamlit                          # Web framework
pandas                             # Data manipulation
numpy                              # Numerical computing
scikit-learn                       # Machine learning
plotly                             # Interactive charts
joblib                             # Model serialization
streamlit-community-navigation-bar # Custom navbar
selenium                           # Web automation
webdriver-manager                  # ChromeDriver management
beautifulsoup4                     # HTML parsing
requests                           # HTTP library
pymysql                            # MySQL connector
```

## Troubleshooting 🐛

**Issue**: "Failed to load models"
- Verify all `.pkl` files exist in `models/` directory
- Check file permissions
- Ensure sufficient memory for model loading

**Issue**: "Web scraper not available"
- Install Selenium: `pip install selenium webdriver-manager`
- Ensure Chrome browser is installed
- Check internet connection

**Issue**: "MySQL connection error"
- Verify `secrets.toml` has correct credentials
- Check MySQL server is running
- Ensure database port is accessible
- App works without MySQL (visitor tracking disabled)

**Issue**: "ChromeDriver version mismatch"
- Update Chrome browser to latest version
- Delete cached ChromeDriver: `~/.wdm/`
- Reinstall: `pip install --upgrade webdriver-manager`

**Issue**: "Video not found"
- Check `Videos/video1.mp4` exists
- Verify video format is supported
- Use MP4 format for best compatibility

## Project Context 📚

**University Project**  
- **Institution**: UIET, MDU Rohtak
- **Course**: PROJECT - II (PROJ-CSE-423G)
- **Semester**: 7th
- **Program**: B.Tech. AIML
- **Supervisor**: Dr. DheerDhwaj
- **Developer**: Aakash (7113655)

## Social Links 🔗

- **GitHub**: [@aakash-test7](https://github.com/aakash-test7/)
- **LinkedIn**: [Aakash Kharb](https://linkedin.com/in/aakash-kharb)
- **YouTube**: [@aakash5069](https://youtube.com/@aakash5069)
- **X/Twitter**: [@aakash_kharb](https://x.com/aakash_kharb)

## Future Enhancements 🚧

- [ ] Collaborative filtering hybrid approach
- [ ] User accounts and personalized history
- [ ] Dark mode toggle
- [ ] Social sharing of recommendations
- [ ] Advanced search filters
- [ ] Game comparison feature
- [ ] API endpoint for external integration
- [ ] Mobile app version

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Happy gaming!** 🎮 For questions or feedback, reach out via [GitHub](https://github.com/aakash-test7)

**© 2024 Aakash Kharb - TechWill x Game**
""",unsafe_allow_html=True)
if __name__ == "__main__":
    about_page()
