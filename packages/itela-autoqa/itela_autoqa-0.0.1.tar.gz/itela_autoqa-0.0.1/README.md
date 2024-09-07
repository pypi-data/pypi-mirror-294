# iTelaSoft AutoQA

`itela-autoqa` is a CLI tool designed to help software QA engineers automate and accelerate their testing workflows using AI. The tool captures a screenshot of a webpage, sends it for analysis, and provides actionable insights to improve QA processes.

## Features
- **Automated QA Analysis**: Quickly analyze any webpage for potential QA issues.
- **AI-Powered**: Utilize the power of AI to enhance and speed up the testing process.
- **Fast Execution**: Get instant feedback for your test cases and page analysis.

## Installation

1. Clone this repository:

```bash
git clone git@git.itelasoft.com.au:chamara.herath/itelasoft-autoqa-tool.git
cd itelasoft-autoqa-tool
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure you have Playwright installed and configured:

```bash
playwright install
```

## Usage

To run the tool, use the following command:

```bash
itela-autoqa --url <website_url> --description "Description" --apikey YOUR_OPENAI_API_KEY
```

### Arguments:
- `--url`: The URL of the webpage you want to analyze.
- `--description`: A short description or context for the analysis. This could describe the type of tests being performed or what you expect from the result.
- `--apikey`: OpenAI api key.

### Example:

```bash
itela-autoqa --url https://example.com --description "Homepage accessibility test" --apikey YOUR_OPENAI_API_KEY
```

## Output

The tool will:
1. Capture a screenshot of the provided URL.
2. Send the screenshot for AI analysis.
3. Print out the analysis result.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contribution

Contributions, issues, and feature requests are welcome. Feel free to open a pull request or submit an issue.

---

**Created by iTelaSoft AI Team**  
Enhancing the future of QA testing with AI.