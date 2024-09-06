
import argparse
import asyncio

from useful_forks.api import UsefulForks


async def app(args):
    api = UsefulForks(args.token, args.repo)
    forks = await api.print_fork_analysis()
    print(forks)  # noqa: T201


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", required=True, help="GitHub access token")
    parser.add_argument("-r", "--repo", required=True, help="GitHub repository")
    args = parser.parse_args()

    asyncio.run(app(args))

if __name__ == "__main__":
    main()
