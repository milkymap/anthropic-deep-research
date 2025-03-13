# Anthropic-OpenAI Integration

A powerful Python package that combines Anthropic's Claude and OpenAI's capabilities to create an advanced agent system with deep web search functionality.

## Features

- **Agent Loop System**: Interactive conversational agent system that processes user queries
- **Deep Iterative Web Search**: Multi-level research through successive search refinements
- **Simple Web Search**: Parallel web searches with intelligent aggregation of results
- **Cross-API Integration**: Seamlessly combines Anthropic and OpenAI APIs
- **Streaming Support**: Real-time streaming of AI responses with live thinking capabilities
- **Tool System**: Extensible tool framework for enhanced functionality
- **CLI Interface**: Simple command-line interface for interacting with the agent

## Installation

```bash
# Clone the repository
git clone https://github.com/milkymap/anthropic-deep-research.git 
cd anthropic-deep-research

# Install dependencies
python -m venv env 
source env/bin/activate
pip install -e .
```

## Requirements

- Python 3.12+
- Anthropic API key
- OpenAI API key

## Configuration

Create a `.env` file in the project root with the following content:

```
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
LOG_LEVEL=INFO
```

## Usage

### Start the Agent Loop

```bash
python -m src launch-engine 
```

This launches the interactive agent that accepts user queries and processes them.

### Using the Web Search Capabilities

The agent has two main web search tools:

1. **Simple Web Search**: For quick, parallel lookups across multiple queries
2. **Deep Iterative Web Search**: For comprehensive, multi-stage research on complex topics

The agent automatically determines which search approach to use based on your query complexity.

Example interaction:

```
query: What are the latest developments in quantum computing?
```

The agent will:
1. Analyze your query
2. Determine the appropriate search method
3. Extract relevant information from the web
4. Present a comprehensive, well-structured response

## Technical Implementation

### Architecture

- `agent_loop.py`: Core agent implementation with conversation handling
- `types.py`: Data models for messages, roles, and stop reasons
- `definitions.py`: System prompts and tool definitions
- `log.py`: Logging configuration
- `settings/`: Configuration management with Pydantic

### Web Search Tools

#### Deep Iterative Web Search

Performs comprehensive, multi-level research through:
- Successive search refinements
- Exploration with increasing depth
- Identification of key subtopics
- Resolution of knowledge gaps
- Cross-referencing across sources

#### Simple Web Search

Conducts parallel web searches with:
- Multiple simultaneous queries
- Intelligent aggregation of results
- Removal of redundancies
- Clear, organized formatting

## Development

### Adding New Tools

To extend the agent with new tools:

1. Define the tool schema in `definitions.py`
2. Implement the tool function in `agent_loop.py`
3. Register the tool in the agent loop's conversation handler

### Modifying System Prompts

System prompts define the agent's behavior and can be adjusted in `definitions.py`.

## License

[Specify License]

## Credits

Developed by [milkymap](mailto:ibrahima.elmokhtar@gmail.com)