import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

@st.cache_data
def load_data():
    """Load and cache the games dataset"""
    df = pd.read_csv('data/games.csv')
    # Clean data
    df['Year_of_Release'] = pd.to_numeric(df['Year_of_Release'], errors='coerce')
    df['User_Score'] = pd.to_numeric(df['User_Score'], errors='coerce')
    df['Critic_Score'] = pd.to_numeric(df['Critic_Score'], errors='coerce')
    return df

def explore_page():
    """Explore Games - Data Visualization and Interactive Catalog"""
    
    st.markdown('<h1 style="text-align: center; color: #4b9cd3; font-size: 3rem;">Explore Games Database</h1>', 
                unsafe_allow_html=True)
    
    # Load data
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    # Initialize session state for explore view
    if 'explore_view' not in st.session_state:
        st.session_state.explore_view = 'charts'  # 'charts' or 'catalog'
    
    # Button layout
    col1, col2, col3 = st.columns([2, 1, 2])
    charts_btn = col1.button("Visual Trends & Charts", use_container_width=True,type="primary")
    catalog_btn = col3.button("Interactive Game Catalog", use_container_width=True,type="primary")
    
    # Update session state based on button clicks
    if charts_btn:
        st.session_state.explore_view = 'charts'
    if catalog_btn:
        st.session_state.explore_view = 'catalog'
    
    if st.session_state.explore_view == 'charts':
        # Key Metrics at the top
        con = st.container(border=True)
        with con:
            st.markdown('<h2 style="font-size: 2rem; color: #4b9cd3;">Overview Statistics</h2>', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Games", f"{len(df):,}")
            with col2:
                st.metric("Total Genres", df['Genre'].nunique())
            with col3:
                st.metric("Total Publishers", df['Publisher'].nunique())
            with col4:
                avg_score = df['Critic_Score'].mean()
                st.metric("Avg Critic Score", f"{avg_score:.1f}" if not pd.isna(avg_score) else "N/A")
        
        # Genre Popularity Chart
        con = st.container(border=True)
        with con:
            st.markdown('<h2 style="font-size: 2rem; color: #4b9cd3;">Genre Popularity</h2>', unsafe_allow_html=True)
            col1, col2 = st.columns([2, 1])
            
            with col1:
                genre_counts = df['Genre'].value_counts().head(15)
                fig_genre = px.bar(
                    x=genre_counts.values,
                    y=genre_counts.index,
                    orientation='h',
                    title='Top 15 Genres by Number of Games',
                    labels={'x': 'Number of Games', 'y': 'Genre'},
                    color=genre_counts.values,
                    color_continuous_scale='Blues'
                )
                fig_genre.update_layout(
                    showlegend=False,
                    height=500,
                    yaxis={'categoryorder':'total ascending'}
                )
                st.plotly_chart(fig_genre, use_container_width=True)
            
            with col2:
                st.markdown("**Top 5 Genres:**")
                for idx, (genre, count) in enumerate(genre_counts.head(5).items(), 1):
                    st.markdown(f"{idx}. **{genre}** - {count:,} games")
        
        # Release Timeline
        con = st.container(border=True)
        with con:
            st.markdown('<h2 style="font-size: 2rem; color: #4b9cd3;">Games Release Timeline</h2>', unsafe_allow_html=True)
            year_counts = df.groupby('Year_of_Release').size().reset_index(name='count')
            year_counts = year_counts[year_counts['Year_of_Release'] >= 1980]
            year_counts = year_counts[year_counts['Year_of_Release'] <= 2020]
            
            fig_timeline = px.line(
                year_counts,
                x='Year_of_Release',
                y='count',
                title='Number of Games Released Per Year (1980-2020)',
                labels={'Year_of_Release': 'Year', 'count': 'Number of Games'},
                markers=True
            )
            fig_timeline.update_traces(line_color='#4b9cd3', line_width=3)
            fig_timeline.update_layout(height=400)
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Platform Distribution
        con = st.container(border=True)
        with con:
            st.markdown('<h2 style="font-size: 2rem; color: #4b9cd3;">Platforms & Publishers</h2>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                platform_counts = df['Platform'].value_counts().head(10)
                fig_platform = px.pie(
                    values=platform_counts.values,
                    names=platform_counts.index,
                    title='Top 10 Gaming Platforms',
                    hole=0.4
                )
                fig_platform.update_layout(height=400)
                st.plotly_chart(fig_platform, use_container_width=True)
            
            with col2:
                # Publisher market share
                publisher_counts = df['Publisher'].value_counts().head(10)
                fig_publisher = px.bar(
                    x=publisher_counts.values,
                    y=publisher_counts.index,
                    orientation='h',
                    title='Top 10 Publishers',
                    labels={'x': 'Number of Games', 'y': 'Publisher'},
                    color=publisher_counts.values,
                    color_continuous_scale='Teal'
                )
                fig_publisher.update_layout(
                    showlegend=False,
                    height=400,
                    yaxis={'categoryorder':'total ascending'}
                )
                st.plotly_chart(fig_publisher, use_container_width=True)
        
        # Rating vs Popularity Analysis
        con = st.container(border=True)
        with con:
            st.markdown('<h2 style="font-size: 2rem; color: #4b9cd3;">Rating vs Popularity Analysis</h2>', unsafe_allow_html=True)
            
            # Filter for games with valid scores
            rating_df = df[(df['Critic_Score'].notna()) & (df['User_Score'].notna()) & (df['User_Count'] > 10)].copy()
            
            if len(rating_df) > 0:
                fig_rating = px.scatter(
                    rating_df,
                    x='Critic_Score',
                    y='User_Score',
                    size='User_Count',
                    color='Genre',
                    hover_data=['Name', 'Year_of_Release', 'Platform'],
                    title='Critic Score vs User Score (bubble size = number of user reviews)',
                    labels={'Critic_Score': 'Critic Score', 'User_Score': 'User Score'},
                    opacity=0.6
                )
                fig_rating.update_layout(height=500)
                st.plotly_chart(fig_rating, use_container_width=True)
            else:
                st.info("Not enough data for rating analysis")
        
        # Regional Sales Analysis
        con = st.container(border=True)
        with con:
            st.markdown('<h2 style="font-size: 2rem; color: #4b9cd3;">Global Sales Distribution</h2>', unsafe_allow_html=True)
            
            sales_by_region = pd.DataFrame({
                'Region': ['North America', 'Europe', 'Japan', 'Other'],
                'Sales': [
                    df['NA_Sales'].sum(),
                    df['EU_Sales'].sum(),
                    df['JP_Sales'].sum(),
                    df['Other_Sales'].sum()
                ]
            })
            
            fig_sales = px.bar(
                sales_by_region,
                x='Region',
                y='Sales',
                title='Total Sales by Region (in millions)',
                labels={'Sales': 'Sales (millions)'},
                color='Sales',
                color_continuous_scale='Viridis'
            )
            fig_sales.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_sales, use_container_width=True)
        
        # Top selling games
        con = st.container(border=True)
        with con:
            st.markdown('<h2 style="font-size: 2rem; color: #4b9cd3;">Top 10 Best-Selling Games</h2>', unsafe_allow_html=True)
            top_games = df.nlargest(10, 'Global_Sales')[['Name', 'Platform', 'Year_of_Release', 'Genre', 'Global_Sales']]
            
            fig_top = px.bar(
                top_games,
                x='Global_Sales',
                y='Name',
                orientation='h',
                title='Top 10 Games by Global Sales',
                labels={'Global_Sales': 'Sales (millions)', 'Name': 'Game'},
                color='Global_Sales',
                color_continuous_scale='RdYlGn',
                hover_data=['Platform', 'Year_of_Release', 'Genre']
            )
            fig_top.update_layout(
                height=450,
                yaxis={'categoryorder':'total ascending'},
                showlegend=False
            )
            st.plotly_chart(fig_top, use_container_width=True)
    
    if st.session_state.explore_view == 'catalog':
        st.markdown('<h2 style="font-size: 2rem; color: #4b9cd3;">Interactive Game Catalog</h2>', unsafe_allow_html=True)
        st.markdown("Filter and explore the complete games database")
        
        # Sidebar filters
        st.sidebar.markdown("### Filters")
        
        # Genre filter
        genres = ['All'] + sorted(df['Genre'].dropna().unique().tolist())
        selected_genres = st.sidebar.multiselect(
            "Select Genre(s)",
            options=genres[1:],  # Exclude 'All' from options
            default=[]
        )
        
        # Platform filter
        platforms = ['All'] + sorted(df['Platform'].dropna().unique().tolist())
        selected_platforms = st.sidebar.multiselect(
            "Select Platform(s)",
            options=platforms[1:],
            default=[]
        )
        
        # Year range filter
        min_year = int(df['Year_of_Release'].min()) if not pd.isna(df['Year_of_Release'].min()) else 1980
        max_year = int(df['Year_of_Release'].max()) if not pd.isna(df['Year_of_Release'].max()) else 2020
        
        year_range = st.sidebar.slider(
            "Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
        
        # Publisher filter
        publishers = sorted(df['Publisher'].dropna().unique().tolist())
        selected_publisher = st.sidebar.selectbox(
            "Select Publisher",
            options=['All'] + publishers
        )
        
        # Rating filter
        ratings = ['All'] + sorted(df['Rating'].dropna().unique().tolist())
        selected_rating = st.sidebar.selectbox(
            "Select Rating",
            options=ratings
        )
        
        # Apply filters
        filtered_df = df.copy()
        
        if selected_genres:
            filtered_df = filtered_df[filtered_df['Genre'].isin(selected_genres)]
        
        if selected_platforms:
            filtered_df = filtered_df[filtered_df['Platform'].isin(selected_platforms)]
        
        filtered_df = filtered_df[
            (filtered_df['Year_of_Release'] >= year_range[0]) &
            (filtered_df['Year_of_Release'] <= year_range[1])
        ]
        
        if selected_publisher != 'All':
            filtered_df = filtered_df[filtered_df['Publisher'] == selected_publisher]
        
        if selected_rating != 'All':
            filtered_df = filtered_df[filtered_df['Rating'] == selected_rating]
        
        # Display filtered results
        st.markdown(f"### Showing {len(filtered_df):,} games")
        
        # Search box
        search_term = st.text_input("Search by game name", "")
        if search_term:
            filtered_df = filtered_df[filtered_df['Name'].str.contains(search_term, case=False, na=False)]
            st.markdown(f"**Search results: {len(filtered_df):,} games**")
        
        # Sort options
        col1, col2 = st.columns([1, 3])
        with col1:
            sort_by = st.selectbox(
                "Sort by",
                options=['Name', 'Year_of_Release', 'Global_Sales', 'Critic_Score', 'User_Score']
            )
        with col2:
            sort_order = st.radio("Order", options=['Ascending', 'Descending'], horizontal=True)
        
        # Apply sorting
        ascending = (sort_order == 'Ascending')
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
        
        # Display dataframe in container
        con = st.container(border=True)
        with con:
            st.dataframe(
                filtered_df[[
                    'Name', 'Platform', 'Year_of_Release', 'Genre', 'Publisher',
                    'Global_Sales', 'Critic_Score', 'User_Score', 'Rating'
                ]],
                use_container_width=True,
                height=600,
                column_config={
                    "Name": st.column_config.TextColumn("Game Name", width="medium"),
                    "Platform": st.column_config.TextColumn("Platform", width="small"),
                    "Year_of_Release": st.column_config.NumberColumn("Year", format="%d"),
                    "Genre": st.column_config.TextColumn("Genre", width="small"),
                    "Publisher": st.column_config.TextColumn("Publisher", width="medium"),
                    "Global_Sales": st.column_config.NumberColumn(
                        "Global Sales",
                        format="%.2f M",
                        help="Sales in millions"
                    ),
                    "Critic_Score": st.column_config.NumberColumn(
                        "Critic Score",
                        format="%d",
                        help="Metacritic score"
                    ),
                    "User_Score": st.column_config.NumberColumn(
                        "User Score",
                        format="%.1f"
                    ),
                    "Rating": st.column_config.TextColumn("Rating", width="small")
                }
            )
        
        # Download filtered data
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        c1,c2,c3=st.columns([3,5,3])
        c2.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name="filtered_games.csv",
            mime="text/csv", use_container_width=True,type="primary"
        )
        
        # Quick stats for filtered data
        if len(filtered_df) > 0:
            con = st.container(border=True)
            with con:
                st.markdown('<h2 style="font-size: 2rem; color: #4b9cd3;">Filtered Data Statistics</h2>', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Games", f"{len(filtered_df):,}")
                with col2:
                    avg_sales = filtered_df['Global_Sales'].mean()
                    st.metric("Avg Global Sales", f"{avg_sales:.2f}M" if not pd.isna(avg_sales) else "N/A")
                with col3:
                    avg_critic = filtered_df['Critic_Score'].mean()
                    st.metric("Avg Critic Score", f"{avg_critic:.1f}" if not pd.isna(avg_critic) else "N/A")
                with col4:
                    avg_user = filtered_df['User_Score'].mean()
                    st.metric("Avg User Score", f"{avg_user:.1f}" if not pd.isna(avg_user) else "N/A")


if __name__ == "__main__":
    explore_page()
