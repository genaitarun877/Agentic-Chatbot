import os
from datetime import datetime, timedelta
from tavily import TavilyClient
from typing import List, Dict, Any
import logging

class NewsFetcher:
    """
    Utility class to fetch AI/ML/Tech news using Tavily API
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY is required")
        
        self.client = TavilyClient(api_key=self.api_key)
        self.logger = logging.getLogger(__name__)
    
    def _parse_days_selection(self, days_selection: str) -> int:
        """
        Parse the days selection string to get number of days
        """
        if "3 days" in days_selection:
            return 3
        elif "6 days" in days_selection:
            return 6
        elif "10-15 days" in days_selection:
            return 12  # Use 12 as middle ground
        else:
            return 7  # Default fallback
    
    def _get_date_filter(self, days: int) -> str:
        """
        Generate date filter string for the API
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        return start_date.strftime("%Y-%m-%d")
    
    def fetch_ai_news(self, days_selection: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Fetch AI/ML/Tech news articles for the specified time period
        
        Args:
            days_selection: String like "3 days", "6 days", "10-15 days"
            max_results: Maximum number of articles to fetch
            
        Returns:
            List of news articles with title, content, url, published_date
        """
        try:
            days = self._parse_days_selection(days_selection)
            since_date = self._get_date_filter(days)
            
            # Search queries for AI/ML/Tech news
            search_queries = [
                "artificial intelligence AI news",
                "machine learning ML breakthrough",
                "deep learning neural networks",
                "AI technology latest developments",
                "machine learning research",
                "AI startups funding",
                "OpenAI ChatGPT updates",
                "Google AI Gemini",
                "tech industry AI adoption",
                "AI tools applications"
            ]
            
            all_articles = []
            
            for query in search_queries:
                try:
                    # Search for recent AI/ML/Tech news
                    response = self.client.search(
                        query=query,
                        search_depth="advanced",
                        max_results=max_results // len(search_queries) + 2,
                        include_domains=["techcrunch.com", "venturebeat.com", "arstechnica.com", 
                                       "theverge.com", "wired.com", "mit.edu", "openai.com", 
                                       "google.com", "microsoft.com", "nvidia.com", "arxiv.org",
                                       "towards-data-science.com", "medium.com"],
                        days=days
                    )
                    
                    if response and 'results' in response:
                        for article in response['results']:
                            if len(all_articles) >= max_results:
                                break
                                
                            # Filter and clean article data
                            cleaned_article = {
                                'title': article.get('title', ''),
                                'content': article.get('content', '')[:1000] + '...' if len(article.get('content', '')) > 1000 else article.get('content', ''),
                                'url': article.get('url', ''),
                                'published_date': article.get('published_date', ''),
                                'score': article.get('score', 0)
                            }
                            
                            # Basic filtering for AI/ML/Tech relevance
                            title_content = (cleaned_article['title'] + ' ' + cleaned_article['content']).lower()
                            ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 
                                         'neural network', 'chatgpt', 'gpt', 'llm', 'gemini', 'claude', 'openai',
                                         'tech', 'technology', 'startup', 'algorithm', 'data science', 'automation']
                            
                            if any(keyword in title_content for keyword in ai_keywords):
                                all_articles.append(cleaned_article)
                
                except Exception as e:
                    self.logger.warning(f"Error fetching news for query '{query}': {str(e)}")
                    continue
            
            # Remove duplicates based on URL and sort by score
            seen_urls = set()
            unique_articles = []
            
            for article in sorted(all_articles, key=lambda x: x.get('score', 0), reverse=True):
                if article['url'] not in seen_urls and article['url']:
                    seen_urls.add(article['url'])
                    unique_articles.append(article)
                    if len(unique_articles) >= max_results:
                        break
            
            self.logger.info(f"Fetched {len(unique_articles)} unique AI/ML/Tech articles")
            return unique_articles
            
        except Exception as e:
            self.logger.error(f"Error fetching AI news: {str(e)}")
            return []
    
    def get_news_summary_data(self, days_selection: str) -> Dict[str, Any]:
        """
        Get formatted news data ready for summarization
        
        Args:
            days_selection: String like "3 days", "6 days", "10-15 days"
            
        Returns:
            Dictionary with articles and metadata
        """
        articles = self.fetch_ai_news(days_selection)
        
        return {
            'articles': articles,
            'total_articles': len(articles),
            'time_period': days_selection,
            'fetched_at': datetime.now().isoformat(),
            'summary_ready': len(articles) > 0
        }
