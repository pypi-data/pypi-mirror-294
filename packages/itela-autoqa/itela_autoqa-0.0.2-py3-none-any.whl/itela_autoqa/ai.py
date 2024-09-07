import base64
from openai import OpenAI
from typing import List, Union
from .config import MODEL_NAME, MAX_TOKENS, TEMPERATURE


SYSTEM_PROMPT = """You are an automated QA agent tasked with testing a web application as a software engineer assigned to manual testing would. Here are your instructions:

1. You will be given a screenshot  that map out the current behavior of the application. Your goal is to analyze the provided screenshot  to identify key features, interactions, and functionality.

2. Based on this analysis, you will formulate a series of test cases (specs) that validate important aspects of the user interface, navigation, and functionality. These test cases should focus on critical user interactions, such as:
    - Navigating between different sections or pages of the application.
    - Interacting with forms (input fields, dropdowns, buttons, etc.).
    - Ensuring clickable elements, such as buttons or links, perform the expected actions.


3. Your test cases should aim to cover a broad range of user journeys while MINIMIZING redundant steps. Focus on testing the intended functionality of the application, rather than specific behaviors you observe in the screenshot.

4.You must NOT change any names. If names are present in the UI, they should be kept EXACTLY as they appear, especially keeping them in UPPERCASE letters if they are originally in capital letters.

####Output 

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":
 
```json
[
{
 "test_case": [string]  // Each test case
    "steps": list[string]  // list of steps, Use dummy values for sensitive data such as PII, unless specific values are provided by the user.
}
]
```

"""


def prepare_prompt(
    image_data_url: str, user_prompt: Union[str, None] = None
) -> List[dict]:
    """
    Prepares the prompt for the AI model by embedding the image URL and optional user description.

    Args:
        image_data_url (str): Data URL of the captured screenshot.
        user_prompt (Union[str, None]): Optional text prompt to provide additional context.

    Returns:
        List[dict]: Formatted messages for the AI model to process.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    content = [
        {
            "type": "image_url",
            "image_url": {"url": image_data_url, "detail": "high"},
        }
    ]

    if user_prompt:
        content.insert(0, {"type": "text", "text": user_prompt})

    messages.append({"role": "user", "content": content})

    return messages


def generate_data_url(image_path: str) -> str:
    """
    Converts an image file into a base64-encoded data URL.

    Args:
        image_path (str): The file path of the image to be converted.

    Returns:
        str: The base64-encoded data URL.

    Raises:
        FileNotFoundError: If the image file cannot be found or accessed.
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return f"data:image/jpeg;base64,{encoded_string.decode('utf-8')}"
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Image file not found: {e}")


def analysis(
    apikey: str, screenshot_path: str, user_description: Union[str, None]
) -> str:
    """
    Performs AI analysis on the provided screenshot and description.

    Args:
        apikey (str): OpenAI Api Key.
        screenshot_path (str): The path to the screenshot file.
        user_description (Union[str, None]): Optional user description for the analysis task.

    Returns:
        str: The result of the AI analysis.
    """
    try:
        client = OpenAI(api_key=apikey)
        data_url = generate_data_url(screenshot_path)
        prompt = prepare_prompt(data_url, user_description)

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=prompt,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            stream=False,
        )

        return completion.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"Failed to perform AI analysis: {e}")
