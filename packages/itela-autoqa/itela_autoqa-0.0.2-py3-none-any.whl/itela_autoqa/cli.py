import argparse
from .utils import capture_screenshot
from .ai import analysis
from .config import VERSION


def main() -> None:
    """
    Entry point for the CLI tool.
    Sets up argparse to handle command-line arguments and executes the QA task
    by capturing a screenshot of the URL and analyzing it with AI.
    """
    # Setup argparse for CLI arguments
    parser = argparse.ArgumentParser(
        description=f"iTelaSoft AI QA Automation Tool {VERSION}"
    )
    parser.add_argument("-v", "--version", action="version", version=f"CLI {VERSION}")
    parser.add_argument(
        "-u", "--url", type=str, required=True, help="The web URL to capture"
    )
    parser.add_argument(
        "-d",
        "--description",
        type=str,
        required=False,
        help="Optional description to associate with the QA task",
    )
    parser.add_argument("--apikey", type=str, required=True, help="OpenAI Api Key")

    try:
        args = parser.parse_args()

        # Capture screenshot
        screenshot_path = capture_screenshot(args.url)

        # Run AI analysis
        result = analysis(args.apikey, screenshot_path, args.description)
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
