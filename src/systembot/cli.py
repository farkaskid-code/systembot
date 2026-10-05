import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="System Bot CLI Parser")

    parser.add_argument(
        "-u", "--url", type=str, required=False, help="Inference server URL"
    )
    parser.add_argument("-m", "--model", type=str, required=False, help="Model name")
    parser.add_argument(
        "-p",
        "--provider",
        type=str,
        required=False,
        help="Provider name",
        choices=["ollama", "openai-compat"],
    )
    parser.add_argument(
        "-k",
        "--api_key",
        type=str,
        required=False,
        help="API key for remote inference servers",
    )
    parser.add_argument("query", type=str, help="Query string")

    return parser.parse_args()
