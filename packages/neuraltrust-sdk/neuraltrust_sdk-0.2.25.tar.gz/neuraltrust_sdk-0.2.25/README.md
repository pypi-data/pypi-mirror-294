# NeuralTrust SDK

The NeuralTrust SDK provides tools for generating test sets, creating knowledge bases, and running evaluations for language models.

## Table of Contents

- [Installation](#installation)
- [Key Components](#key-components)
- [Usage Example](#usage-example)
- [Key Classes](#key-classes)
  - [KnowledgeBase](#knowledgebase)
  - [GenerateTestset](#generatetestset)
  - [EvaluationSet](#evaluationset)
- [Advanced Usage](#advanced-usage)
- [License](#license)

## Installation

```bash
pip install neuraltrust-sdk
```


## Key Components

1. **KnowledgeBase**: Create and manage knowledge bases from various sources.
2. **GenerateTestset**: Generate test sets for evaluations.
3. **EvaluationSet**: Set up and run evaluations.

## Usage Example

Here's an example of how to use the NeuralTrust SDK:

```python
    import os
    from src.neuraltrust.api_keys.neuraltrust_api_key import NeuralTrustApiKey
    from src.neuraltrust.api_keys.openai_api_key import OpenAiApiKey
    from src.neuraltrust.evaluation_set import EvaluationSet
    from src.neuraltrust.generate_testset import GenerateTestset
    from src.neuraltrust.generators import KnowledgeVectorBase
    # Set API keys
    NeuralTrustApiKey.set_key(os.getenv('NEURALTRUST_API_KEY'))
    OpenAiApiKey.set_key(os.getenv('OPENAI_API_KEY'))
    # Create a Knowledge Base from PDF and upload to Azure AI Search
    knowledge_base = KnowledgeVectorBase.from_pdf(
        'data/banking/',
        search_service_name="neuraltrust-search",
        index_name="banking",
        api_key=os.getenv('AZURE_AI_SEARCH_API_KEY')
    )
    # Generate a test set
    testset = GenerateTestset(
        evaluation_set_id="faqs_ab6be3",
        num_questions=20,
        knowledge_base=knowledge_base
    )
    testset_id = testset.generate()
    # Create and run an evaluation set
    eval = EvaluationSet(id="faqs_ab6be3")
    eval.run()
```

## Key Classes

### KnowledgeBase

The `KnowledgeBase` class allows you to create and manage knowledge bases from various sources, including pandas DataFrames, Azure AI Search, and PDF files.

#### Methods:
- `from_pandas(df: pd.DataFrame, columns: Optional[Sequence[str]] = None, **kwargs) -> KnowledgeBase`
- `from_pdf(path: str, search_service_name: str, index_name: str, api_key: str, **kwargs) -> KnowledgeVectorBase`

### GenerateTestset

The `GenerateTestset` class is used to generate test sets for evaluations based on a knowledge base.

#### Methods:
- `generate() -> str`: Generates a test set and returns the testset ID.

### EvaluationSet

The `EvaluationSet` class is used to set up and run evaluations.

#### Methods:
- `run()`: Runs the evaluation set.

## Advanced Usage

For more advanced usage and configuration options, please refer to the individual class documentation.