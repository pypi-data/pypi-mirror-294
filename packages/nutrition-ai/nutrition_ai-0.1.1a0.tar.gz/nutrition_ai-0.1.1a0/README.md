
# Nutrition AI

Nutrition AI is a Python module that interfaces with the Passio Nutrition AI API. It provides functionalities for food product information retrieval, food searching, and interaction with an AI nutrition advisor.

## Features

- Authentication with the Passio API
- Fetching food product information by UPC, food ID, or reference code
- Searching for foods by name
- Interaction with an AI nutrition advisor, including:
  - Starting conversation threads
  - Sending messages and receiving responses
  - Handling complex queries requiring additional data
  - Utilizing content tool hints for enhanced responses
  - Visual food extraction from images

## Installation

You can install the Nutrition AI module using pip:

```
pip install nutrition-ai
```

You will need an API key from Passio to use this module. If you do not have one, you can obtain one [here](https://www.passio.ai/nutrition-ai#nutrition-ai-pricing)

## Configuration

Before using the module, you need to set up your [Passio API key](https://www.passio.ai/nutrition-ai#nutrition-ai-pricing) as an environment variable:

```
export PASSIO_API_KEY=your_api_key_here
```

## Usage

We've included a Jupyter notebook [here](tutorial.ipynb) which shows how to use the Nutrition AI module.

Here are some examples of how to use the Nutrition AI module:

### Authentication

```python
from nutrition_ai import auth

header, expiry = auth.get_header_and_expiry_time()
```

### Fetching Product Information

```python
from nutrition_ai import fetch

# Fetch by UPC
product = fetch.product_by_upc('698241110109', header)

# Fetch by food ID
product = fetch.product_by_food_id('1603211317047', header)

# Fetch by reference code
product = fetch.product_by_refCode('your_ref_code', header)
```

### Searching for Foods

```python
from nutrition_ai import search

results = search.food_matching('pepperoni pizza', header=header, limit=5)
```

### Interacting with the AI Advisor

```python
from nutrition_ai.advisor import conversation, tools

# Start a conversation thread
thread_response = conversation.start_thread(header)

# Send a simple message
message_response = conversation.send_message(
    thread_response.threadId, 
    'what does vitamin C do, briefly?', 
    header
)

# Handle complex queries
complex_response = conversation.send_message(
    thread_response.threadId,
    'what do you think of my food logs this week?',
    header
)

if complex_response.dataRequest:
    log_response = tools.detect_meal_logs_required(
        complex_response.threadId,
        complex_response.messageId,
        complex_response.dataRequest.toolCallId,
        complex_response.dataRequest.runId,
        "21 Pizzas",
        header
    )

# Use content tool hints
if 'SearchIngredientMatches' in response.contentToolHints:
    search_response = tools.search_ingredient_matches(
        response.threadId,
        response.messageId,
        header
    )

# Visual food extraction
from PIL import Image

img = Image.open("path/to/your/image.jpg").resize((512, 512))
response = tools.visual_food_extraction(
    thread_response.threadId,
    img,
    message="what did I have for lunch?",
    header=header
)
```

## Running Tests

To run the unit tests for this module:

1. Ensure you have set the `PASSIO_API_KEY` environment variable.
2. Run the following command from the root of the project:

```
python -m unittest tests/test_nutrition_ai.py
```

## License

MIT

## Contact

For any queries or support, please contact james@passiolife.com.