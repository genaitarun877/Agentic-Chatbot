# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is an end-to-end Agentic AI Chatbot built using LangGraph, LangChain, and Streamlit. The project implements a modular architecture for creating stateful conversational AI agents with tool integration capabilities.

## Architecture

### Core Components

- **Entry Point**: `app.py` - Main application launcher
- **Main Module**: `src/langgraphagenticai/main.py` - Application orchestrator and UI controller
- **Graph Builder**: `src/langgraphagenticai/graph/graph_builder.py` - Constructs different types of conversational graphs
- **State Management**: `src/langgraphagenticai/state/state.py` - Defines the conversation state structure
- **Node Types**: 
  - Basic chatbot nodes (`src/langgraphagenticai/nodes/basic_chatbot_node.py`)
  - Tool-enhanced chatbot nodes (`src/langgraphagenticai/nodes/chatbot_with_tool_node.py`)
- **Tools**: `src/langgraphagenticai/tools/search_tool.py` - Tavily web search integration
- **LLM Integration**: `src/langgraphagenticai/LLMS/groqllm.py` - Groq API wrapper
- **UI Layer**: `src/langgraphagenticai/ui/streamlitui/` - Streamlit interface components

### Supported Use Cases

1. **Basic Chatbot** - Simple conversational AI without external tools
2. **Chatbot with Web** - Enhanced chatbot with web search capabilities via Tavily
3. **AI News** - Configured but not implemented in current codebase

## Development Commands

### Installation
```powershell
pip install -r requirements.txt
```

### Running the Application
```powershell
streamlit run app.py
```

### Environment Setup
Create a `.env` file with:
- `GROQ_API_KEY` - Your Groq API key for LLM access
- `TAVILY_API_KEY` - Your Tavily API key for web search functionality

## Configuration

### UI Configuration
The UI is configured through `src/langgraphagenticai/ui/uiconfigfile.ini`:
- `PAGE_TITLE` - Application title
- `LLM_OPTIONS` - Available LLM providers (currently Groq)
- `USECASE_OPTIONS` - Available chatbot use cases
- `GROQ_MODEL_OPTIONS` - Available Groq models

### Model Configuration
Currently supports Groq models:
- `llama-3.1-8b-instant`
- `openai/gpt-oss-20b`
- `meta-llama/llama-guard-4-12b`

## Key Dependencies

- **LangGraph**: State graph orchestration for agentic workflows
- **LangChain**: Core framework for building language model applications
- **Streamlit**: Web UI framework
- **Groq**: Fast LLM inference API
- **Tavily**: Web search API for tool integration
- **FAISS**: Vector database for potential future enhancements

## Development Notes

### Graph Construction Pattern
The application uses a modular graph construction pattern where:
1. `GraphBuilder` initializes with an LLM model
2. Different graph types are built based on selected use case
3. Nodes are added to the StateGraph with appropriate edges
4. Conditional edges handle tool calling logic

### State Management
The application uses LangGraph's message-based state management:
- Messages are accumulated using `add_messages` annotation
- State flows through graph nodes maintaining conversation context
- Tool calls are handled through conditional routing

### Error Handling
The main application implements comprehensive error handling for:
- Invalid user inputs
- LLM configuration failures
- Graph setup errors
- API key validation

### UI Flow
1. User selects LLM provider and model in sidebar
2. User chooses use case (Basic Chatbot or Chatbot with Web)
3. Required API keys are collected based on selection
4. Chat interface processes user messages through appropriate graph
5. Results are streamed back to the UI with proper message formatting
