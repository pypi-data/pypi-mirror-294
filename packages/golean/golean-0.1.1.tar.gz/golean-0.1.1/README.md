# GoLean API Client

[![PyPI version](https://badge.fury.io/py/golean.svg)](https://badge.fury.io/py/golean)
[![Python Versions](https://img.shields.io/pypi/pyversions/golean.svg)](https://pypi.org/project/golean/)

GoLean is a powerful Python client for the GoLean API, offering efficient and customizable prompt compression services tailored for Large Language Models (LLMs). Optimize your LLM workflows with our state-of-the-art compression algorithms.

## Features

- **Efficient Prompt Compression:** Optimize LLM performance with customizable compression rates.
- **Flexible Model Support:** Compatible with a wide range of LLMs from OpenAI, Anthropic, and Cohere.
- **Cost Optimization:** Reduce token usage for various LLM APIs.
- **Secure Authentication:** Robust API key-based authentication system.
- **Easy Configuration:** Seamless setup with support for environment variables.
- **Comprehensive Documentation:** Detailed guides and API references to get you started quickly.

## Installation

Install the GoLean client using pip:

```bash
pip install golean
```

## Quick Start

```python
from golean import GoLean

# Initialize the GoLean client
golean = GoLean(api_key="your_api_key")

# Compress a prompt
result = golean.compress_prompt(
    context="The quick brown fox jumps over the lazy dog. The fox is known for its cunning and agility.",
    question="What animal is described?",
    compression_rate=0.5,
    model="gpt-4o"
)

print(f"Compressed Prompt: {result['compressed_prompt']}")
print(f"Compression Ratio: {result['ratio']}")
print(f"Compression Rate: {result['rate']}")
print(f"Token Savings: {result['saving']}")
```

## Usage

### Initialization

```python
from golean import GoLean

# Initialize with API key
golean = GoLean(api_key="your_api_key")

# Or, set GOLEAN_API_KEY as an environment variable and initialize without parameters
golean = GoLean()
```

### Compressing Prompts

```python
result = golean.compress_prompt(
    context="Large Language Models (LLMs) are revolutionizing various industries, from content creation to data analysis. These models, trained on vast amounts of text data, can generate human-like text, answer questions, and perform complex language tasks.",
    question="What are the key applications of LLMs in different sectors?",
    compression_rate=0.7,
    model="gpt-4o"
)

print(f"Compressed Prompt: {result['compressed_prompt']}")
print(f"Original Tokens: {result['origin_tokens']}")
print(f"Compressed Tokens: {result['compressed_tokens']}")
print(f"Compression Ratio: {result['ratio']}")
print(f"Compression Rate: {result['rate']}")
print(f"Token Savings: {result['saving']}")
```

## Supported Models

GoLean supports compression optimization for various LLM models:

### OpenAI Models

- gpt-3.5-turbo
- gpt-3.5-turbo-16k
- gpt-4-turbo
- gpt-4
- gpt-4o
- gpt-4o-2024-05-13

### Anthropic Models

- claude-3-sonnet
- claude-3-opus
- claude-3-haiku

### Cohere Models

- command-r

## Configuration

### API Key

Set your API key using one of these methods:

1. Environment variable:

   ```bash
   export GOLEAN_API_KEY=your_api_key_here
   ```

2. `.env` file in your project root:

   ```
   GOLEAN_API_KEY=your_api_key_here
   ```

3. Directly in your code (not recommended for production):
   ```python
   golean = GoLean(api_key="your_api_key_here")
   ```

## API Reference

### `GoLean` Class

```python
class GoLean:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GoLean client.

        Args:
            api_key (str, optional): Your GoLean API key. If not provided, reads from GOLEAN_API_KEY env variable.
        """

    def compress_prompt(self,
                        context: str,
                        question: str,
                        compression_rate: float = 0.5,
                        model: str = "gpt-4o") -> Dict[str, Any]:
        """
        Compress a prompt using the GoLean API.

        Args:
            context (str): The context for the prompt.
            question (str): The question to be compressed.
            compression_rate (float): Desired compression rate (0 < rate <= 1). Default is 0.5.
            model (str): Target model for compression optimization. Default is "gpt-4o".

        Returns:
            Dict[str, Any]: Dictionary containing the compressed prompt and metadata.
        """
```

For complete API documentation, please refer to our [official documentation](https://docs.golean.ai).

## Response Format

The `compress_prompt` method returns a dictionary with the following keys:

- `compressed_prompt` (str): The compressed version of the input prompt.
- `compressed_prompt_list` (list): A list containing the compressed prompt (for consistency with batch processing).
- `origin_tokens` (int): The number of tokens in the original prompt.
- `compressed_tokens` (int): The number of tokens in the compressed prompt.
- `ratio` (str): The compression ratio (e.g., "2.5x").
- `rate` (str): The achieved compression rate as a percentage.
- `saving` (str): A string indicating the potential token savings for the specified model.

## Support

For technical assistance, please contact our support team:

- Email: support@golean.ai
- Documentation: [https://golean.ai](https://golean.ai)

For enterprise support options and custom LLM optimization solutions, please contact our sales team at support@golean.ai.

## Legal

Copyright © 2024 GoLean, Inc. All rights reserved.

GoLean is a registered trademark of GoLean, Inc. All other trademarks are the property of their respective owners.

---

Empower your LLMs with GoLean - Compress, Optimize, Succeed.
