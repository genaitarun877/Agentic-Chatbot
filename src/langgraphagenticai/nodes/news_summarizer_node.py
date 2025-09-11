from langchain_core.messages import HumanMessage, AIMessage
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.utils.news_fetcher import NewsFetcher
import logging
from typing import Dict, Any

class NewsSummarizerNode:
    """
    Node for processing and summarizing AI/ML/Tech news articles
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.logger = logging.getLogger(__name__)
    
    def _create_summarization_prompt(self, articles: list, time_period: str) -> str:
        """
        Create a comprehensive prompt for news summarization
        """
        articles_text = ""
        for i, article in enumerate(articles[:15], 1):  # Limit to top 15 articles
            articles_text += f"""
Article {i}:
Title: {article.get('title', 'N/A')}
Content: {article.get('content', 'N/A')}
URL: {article.get('url', 'N/A')}
Published: {article.get('published_date', 'N/A')}
---
"""
        
        prompt = f"""
You are an expert AI/ML/Tech news analyst. Please provide a comprehensive summary of the latest AI, Machine Learning, and Technology news from the past {time_period}.

**INSTRUCTIONS:**
1. **Create a structured summary** organized by major themes/categories
2. **Highlight key developments** in AI, Machine Learning, Deep Learning, and emerging technologies
3. **Include important company news** (OpenAI, Google, Microsoft, Meta, etc.)
4. **Mention funding rounds, acquisitions, or major partnerships**
5. **Note any breakthrough research or technical innovations**
6. **Keep the summary engaging and informative**
7. **Use bullet points and clear headings for readability**
8. **Include relevant URLs for the most important stories**

**FORMAT YOUR RESPONSE AS:**

# 📰 AI & Tech News Summary ({time_period})

## 🚀 Major AI Developments
[Key developments in AI technology, model releases, etc.]

## 🔬 Research & Innovation  
[New research papers, breakthroughs, technical innovations]

## 💼 Business & Funding
[Company news, funding rounds, acquisitions, partnerships]

## 🛠️ Tools & Applications
[New AI tools, applications, product launches]

## 🌟 Notable Mentions
[Other interesting developments worth noting]

## 📊 Market Trends
[Industry trends, adoption patterns, market analysis]

**NEWS ARTICLES TO ANALYZE:**
{articles_text}

Please provide a comprehensive yet concise summary that would be valuable for someone wanting to stay updated on the latest AI/ML/Tech developments.
"""
        return prompt
    
    def process(self, state: State) -> State:
        """
        Main processing function for news summarization
        """
        try:
            self.logger.info("Starting news summarization process")
            
            # Handle both dict and State object types
            if isinstance(state, dict):
                messages = state.get('messages', [])
                user_controls = state.get('user_controls', {})
            else:
                messages = getattr(state, 'messages', [])
                user_controls = getattr(state, 'user_controls', {})
            
            if not user_controls:
                error_msg = "❌ No user controls found in state"
                self.logger.error(error_msg)
                messages.append(AIMessage(content=error_msg))
                if isinstance(state, dict):
                    state['messages'] = messages
                else:
                    state.messages = messages
                return state
            
            # Check if generate news summary button was clicked
            if not user_controls.get('generate_news_summary', False):
                return state
            
            days_selection = user_controls.get('selected_days', '3 days')
            tavily_api_key = user_controls.get('TAVILY_API_KEY')
            
            if not tavily_api_key:
                error_msg = "❌ TAVILY_API_KEY is required for news summarization"
                self.logger.error(error_msg)
                messages.append(AIMessage(content=error_msg))
                if isinstance(state, dict):
                    state['messages'] = messages
                else:
                    state.messages = messages
                return state
            
            # Initialize news fetcher
            news_fetcher = NewsFetcher(api_key=tavily_api_key)
            
            # Show progress message
            progress_msg = f"🔍 Fetching AI/ML/Tech news for the past {days_selection}... This may take a moment."
            messages.append(AIMessage(content=progress_msg))
            
            # Fetch news data
            news_data = news_fetcher.get_news_summary_data(days_selection)
            
            if not news_data['summary_ready']:
                error_msg = f"❌ Unable to fetch news articles for the past {days_selection}. Please check your API key and try again."
                self.logger.error(error_msg)
                messages.append(AIMessage(content=error_msg))
                if isinstance(state, dict):
                    state['messages'] = messages
                else:
                    state.messages = messages
                return state
            
            articles = news_data['articles']
            self.logger.info(f"Fetched {len(articles)} articles for summarization")
            
            if len(articles) == 0:
                no_news_msg = f"📰 No AI/ML/Tech news articles found for the past {days_selection}. Try a different time range."
                messages.append(AIMessage(content=no_news_msg))
                if isinstance(state, dict):
                    state['messages'] = messages
                else:
                    state.messages = messages
                return state
            
            # Create summarization prompt
            summarization_prompt = self._create_summarization_prompt(articles, days_selection)
            
            # Generate summary using LLM
            summary_progress_msg = f"🤖 Analyzing {len(articles)} articles and generating comprehensive summary..."
            messages.append(AIMessage(content=summary_progress_msg))
            
            try:
                # Invoke LLM for summarization
                llm_response = self.llm.invoke([HumanMessage(content=summarization_prompt)])
                
                summary_content = llm_response.content if hasattr(llm_response, 'content') else str(llm_response)
                
                # Add metadata footer
                footer = f"""

---
**📊 Summary Statistics:**
- **Total Articles Analyzed:** {len(articles)}
- **Time Period:** {days_selection}
- **Generated At:** {news_data['fetched_at'][:19].replace('T', ' ')} UTC
- **Powered By:** Tavily API + {user_controls.get('selected_llm', 'AI')} Model

*💡 Stay informed about the latest AI/ML/Tech developments!*
"""
                
                final_summary = summary_content + footer
                
                # Add the final summary to messages
                messages.append(AIMessage(content=final_summary))
                
                self.logger.info("News summarization completed successfully")
                
            except Exception as llm_error:
                error_msg = f"❌ Error generating summary with LLM: {str(llm_error)}"
                self.logger.error(error_msg)
                messages.append(AIMessage(content=error_msg))
            
        except Exception as e:
            error_msg = f"❌ Error in news summarization: {str(e)}"
            self.logger.error(error_msg)
            if isinstance(state, dict):
                messages = state.get('messages', [])
                messages.append(AIMessage(content=error_msg))
                state['messages'] = messages
            else:
                state.messages.append(AIMessage(content=error_msg))
        
        # Update state with messages
        if isinstance(state, dict):
            state['messages'] = messages
        else:
            state.messages = messages
            
        return state
