import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="systembot CLI Tool")
    parser.add_argument("user_prompt", type=str, help="The user prompt to process")
    parser.add_argument(
        "-m", "--model", type=str, help="The model name to use", required=False
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(f"User prompt: {args.user_prompt}")
    if args.model:
        print(f"Model name: {args.model}")
