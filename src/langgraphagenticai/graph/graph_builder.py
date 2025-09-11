from langgraph.graph import StateGraph,START,END
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools,create_tool_node
from langgraph.prebuilt import ToolNode,tools_condition
from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.langgraphagenticai.nodes.news_summarizer_node import NewsSummarizerNode

class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)
        
    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using Langgraph.
        This method initializes a chatbot node using the 'BasicChatbotNode' class
        and integrates it into the graph. The chatbot is set as both the 
        entry and exit point of the graph.
        """
        self.basic_chatbot_node=BasicChatbotNode(self.llm)
        
        
        self.graph_builder.add_node("Chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"Chatbot")
        self.graph_builder.add_edge("Chatbot",END)
    
    def chatbot_with_tools_build_graph(self):
        """
        Build an advanced chatbot graph with tools integration.
        This method creates a chatbot graph that includes both a chatbot node
        ND  tool node. It defines tools,initializes the Chatbot with tool
        capabilities, and sets up the graph structure accordingly.
        The chatbot node is set as the entry point
        """
        ## Define tool and toolnode
        tools=get_tools()
            
        tool_node=create_tool_node(tools)

        ## Define the LLM
        llm=self.llm
        ## Define the chatbot nodes
        obj_chatbot_with_node=ChatbotWithToolNode(llm)
        chatbot_node=obj_chatbot_with_node.create_chatbot(tools)



        ## ADD nodes
        self.graph_builder.add_node("Chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        ## ADD edges
        self.graph_builder.add_edge(START,"Chatbot")
        self.graph_builder.add_conditional_edges("Chatbot",tools_condition)
        self.graph_builder.add_edge("tools","Chatbot")

    def news_summarizer_build_graph(self):
        """
        Build an AI News Summarizer graph.
        This method creates a specialized graph for fetching and summarizing
        AI/ML/Tech news using Tavily API and LLM capabilities.
        The news summarizer node handles the entire workflow.
        """
        # Initialize the news summarizer node
        self.news_summarizer_node = NewsSummarizerNode(self.llm)
        
        # Add the node to the graph
        self.graph_builder.add_node("NewsSummarizer", self.news_summarizer_node.process)
        
        # Set up the graph flow
        self.graph_builder.add_edge(START, "NewsSummarizer")
        self.graph_builder.add_edge("NewsSummarizer", END)

    def setup_graph(self,usecase:str):
        """Sets up the graph by building the appropriate graph based on usecase."""
        if usecase=="Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase=="Chatbot with Web":
            self.chatbot_with_tools_build_graph()
        elif usecase=="AI News Summarizer":
            self.news_summarizer_build_graph()
        
        return self.graph_builder.compile()
