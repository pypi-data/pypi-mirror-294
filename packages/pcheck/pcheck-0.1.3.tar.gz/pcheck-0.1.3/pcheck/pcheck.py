import asyncio
from typing import Any
import aiohttp
import re
import time
import sys


def return_unique(input_file: str) -> list:
    lines_seen = set()
    unique = []
    for line in open(input_file, "r"):
        if line not in lines_seen:
            unique.append(line)
            lines_seen.add(line)
    return unique


def parse_proxy(proxy: str) -> dict[str, str | int | Any] | dict[str, str | int | Any] | None:
    """Parse the proxy string and return a dictionary with the proxy details."""
    match1 = re.match(r'^(http://)?([^:]+):([^:]+):([^:]+):([^@]+)$', proxy)
    match2 = re.match(r'^(http://)?([^:]+):([^@]+)@([^:]+):([^/]+)$', proxy)

    if match1:
        return {
            'scheme': 'http',
            'host': match1.group(2),
            'port': int(match1.group(3)),
            'username': match1.group(4),
            'password': match1.group(5)
        }
    elif match2:
        return {
            'scheme': 'http',
            'host': match2.group(4),
            'port': int(match2.group(5)),
            'username': match2.group(2),
            'password': match2.group(3)
        }
    else:
        return None


async def check_proxy(session: aiohttp.ClientSession, proxy: str, test_url: str, timeout: int) -> tuple[str, bool]:
    """Check if the proxy is working."""
    proxy_info = parse_proxy(proxy)
    if proxy_info is None:
        return proxy, False

    proxy_url = f"http://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['host']}:{proxy_info['port']}"
    try:
        async with session.get(test_url, proxy=proxy_url, timeout=timeout) as response:
            return proxy, response.status == 200
    except Exception:
        return proxy, False


async def main(input_file: str, output_file: str, test_url: str, timeout: int) -> None:
    """Main function to handle proxy checking and reporting."""
    proxies = return_unique(input_file)

    total_proxies = len(proxies)
    working_proxies = []
    invalid_proxies = []

    async with aiohttp.ClientSession() as session:
        tasks = [check_proxy(session, proxy, test_url, timeout) for proxy in proxies]

        start_time = time.time()
        completed_tasks = 0
        working_count = 0
        invalid_count = 0

        for future in asyncio.as_completed(tasks):
            proxy, is_working = await future
            completed_tasks += 1
            if is_working:
                working_proxies.append(proxy)
                working_count += 1
            else:
                invalid_proxies.append(proxy)
                invalid_count += 1

            elapsed_time = time.time() - start_time
            checks_per_second = completed_tasks / elapsed_time if elapsed_time > 0 else 0
            remaining = total_proxies - completed_tasks

            sys.stdout.write(f'\rChecks/s: {checks_per_second:.2f} | '
                             f'Working: {working_count} | '
                             f'Invalid: {invalid_count} | '
                             f'Remaining: {remaining}')
            sys.stdout.flush()

    with open(output_file, 'w') as f:
        for proxy in working_proxies:
            f.write(proxy + '\n')

    sys.stdout.write('\nCompleted!\n')
