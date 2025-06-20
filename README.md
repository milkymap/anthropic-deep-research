# Anthropic Deep Research

A sophisticated AI research agent that combines Anthropic's Claude and OpenAI's capabilities to perform advanced web research and provide comprehensive, well-sourced answers to complex queries.

## 🌟 Features

### 🔍 **Dual Web Search Architecture**
- **Deep Iterative Web Search**: Multi-level research through successive search refinements with up to 10 iterations
- **Simple Web Search**: Parallel web searches with intelligent aggregation for quick lookups

### 🤖 **AI-Powered Agent System**
- Interactive conversational agent with streaming responses
- Cross-API integration (Anthropic Claude + OpenAI GPT-4)
- Intelligent tool selection based on query complexity
- Real-time thinking and response streaming

### 🛠️ **Advanced Research Capabilities**
- Automatic complexity assessment (low/medium/high)
- Comprehensive source verification across multiple credible sources
- Citation tracking and evidence summarization
- Knowledge gap identification and resolution
- Adaptive search strategies based on topic complexity

### 📊 **Structured Output**
- Executive summaries with key findings
- Detailed analysis organized by subtopic
- Evidence summaries with direct quotes and URLs
- Documentation of search process and methodology
- Identification of remaining questions and limitations

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Anthropic API key
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/milkymap/anthropic-deep-research.git
cd anthropic-deep-research

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install the package
pip install -e .
```

### Configuration

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
LOG_LEVEL=INFO
```

### Usage

Launch the interactive research agent:

```bash
python -m src launch-engine
```

## 🔬 Research Capabilities

### Deep Iterative Web Search

Perfect for complex research questions requiring comprehensive analysis:

```
Query: "What are the latest developments in quantum computing and their potential impact on cryptography?"
```

**Process:**
1. **Initial Broad Search**: Establishes baseline understanding
2. **Subtopic Identification**: Discovers key areas (hardware advances, algorithm development, security implications)
3. **Targeted Deep Dives**: Specific searches on each subtopic
4. **Cross-Reference Verification**: Validates information across multiple sources
5. **Synthesis**: Combines findings into comprehensive analysis
6. **Gap Analysis**: Identifies areas needing further investigation

**Output Includes:**
- Executive summary of key findings
- Detailed analysis by subtopic
- Evidence with direct quotes and source URLs
- Timeline of recent developments
- Expert opinions and conflicting viewpoints
- Remaining open questions

### Simple Web Search

Ideal for quick lookups and straightforward questions:

```
Query: "Current price of Bitcoin"
```

**Process:**
- Parallel searches across multiple queries
- Real-time data aggregation
- Quick synthesis and presentation

## 🏗️ Architecture

### Core Components

```
src/anthropic_openai/
├── agent_loop.py          # Main agent implementation
├── types.py              # Data models (Role, ChatMessage, StopReason)
├── definitions.py        # System prompts and tool definitions
├── log.py               # Logging configuration
└── settings/
    ├── __init__.py
    └── credentials.py    # API key management
```

### Tool System

The agent uses two primary research tools:

#### 1. Deep Iterative Web Search Tool
- **Complexity Levels**: Low (3 iterations), Medium (5 iterations), High (10 iterations)
- **Minimum Sources**: 7 credible sources per research session
- **Search Strategy**: Adaptive based on topic and available information
- **Quality Control**: Multi-source verification and citation tracking

#### 2. Simple Web Search Tool
- **Parallel Processing**: Multiple simultaneous queries
- **Context Sizes**: Low, Medium, High (determines search scope)
- **LLM Processing**: Intelligent aggregation and redundancy removal
- **Speed Optimized**: Single-pass processing for quick results

### Data Models

```python
class Role(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"

class ChatMessage(BaseModel):
    role: Role
    content: str | List[Dict]

class StopReason(str, Enum):
    END_TURN = "end_turn"
    MAX_TOKENS = "max_tokens"
    TOOL_USE = "tool_use"
    STOP_SEQUENCE = "stop_sequence"
```

## 🎯 Use Cases

### Academic Research
- Literature reviews and comprehensive topic analysis
- Fact-checking and source verification
- Historical context and timeline construction

### Business Intelligence
- Market research and competitive analysis
- Technology trend analysis
- Regulatory and compliance research

### Current Events
- Breaking news analysis with multiple source verification
- Political and economic development tracking
- Scientific breakthrough summaries

### Technical Research
- Technology comparison and evaluation
- Best practices and implementation guides
- Security and risk assessment

## 🔧 Development

### Adding New Tools

1. **Define Tool Schema** in `definitions.py`:
```python
your_new_tool = {
    "name": "your_tool_name",
    "description": "Tool description",
    "input_schema": {
        "type": "object",
        "properties": {
            "parameter": {"type": "string", "description": "Parameter description"}
        },
        "required": ["parameter"]
    }
}
```

2. **Implement Tool Function** in `agent_loop.py`:
```python
def your_tool_function(self, parameter: str) -> Dict:
    # Implementation logic
    return {"result": "tool output"}
```

3. **Register Tool** in the conversation handler

### Modifying System Prompts

System prompts are defined in `definitions.py` as enum values:

```python
class SystemPromptDefinitions(str, Enum):
    MAIN_AGENT_LOOP = "Your system prompt here..."
    DEEP_ITERATIVE_WEB_SEARCH = "Deep search instructions..."
```

### Logging Configuration

Logging is configured in `log.py` with support for different log levels via environment variables.

## 📈 Performance Considerations

### Search Optimization
- **Parallel Processing**: Simple web search uses ThreadPoolExecutor for concurrent queries
- **Iteration Limits**: Deep search has configurable maximum iterations to prevent infinite loops
- **Context Management**: Adaptive context size based on search complexity

### API Usage
- **Rate Limiting**: Built-in handling for API rate limits
- **Error Recovery**: Graceful degradation when individual searches fail
- **Token Management**: Optimized token usage across both Anthropic and OpenAI APIs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

**Author**: [milkymap](mailto:ibrahima.elmokhtar@gmail.com)

**Built with**:
- [Anthropic Claude](https://www.anthropic.com/) - Advanced AI reasoning and analysis
- [OpenAI GPT-4](https://openai.com/) - Web search capabilities and parallel processing
- [Pydantic](https://pydantic.dev/) - Data validation and settings management
- [Click](https://click.palletsprojects.com/) - Command line interface

## 🔗 Links

- [Repository](https://github.com/milkymap/anthropic-deep-research)
- [Issues](https://github.com/milkymap/anthropic-deep-research/issues)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

---

**Note**: This project requires valid API keys from both Anthropic and OpenAI. Please ensure you have appropriate access and understand the usage costs associated with these services before using this tool extensively.