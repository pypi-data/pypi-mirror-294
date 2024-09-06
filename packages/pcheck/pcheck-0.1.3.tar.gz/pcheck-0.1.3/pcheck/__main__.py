import argparse
import asyncio
from .pcheck import main

parser = argparse.ArgumentParser(description='Test and save working proxies.')
parser.add_argument('-i', '--input', type=str, required=True, help='Path to the input file containing proxies.')
parser.add_argument('-o', '--output', type=str, required=True, help='Path to the output file to save working proxies.')
parser.add_argument('-u', '--url', type=str, default='http://httpbin.org/ip', help='URL to test proxies against.')
parser.add_argument('-t', '--timeout', type=int, default=5, help='Timeout for proxy requests in seconds.')

args = parser.parse_args()

if __name__ == '__main__':
    asyncio.run(main(args.input, args.output, args.url, args.timeout))
