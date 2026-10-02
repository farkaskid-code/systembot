import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="System Bot CLI Parser")

    parser.add_argument("-u", "--url", type=str, required=False, help="Ollama host URL")
    parser.add_argument("-m", "--model", type=str, required=False, help="Model name")
    parser.add_argument("query", type=str, help="Query string")

    return parser.parse_args()
