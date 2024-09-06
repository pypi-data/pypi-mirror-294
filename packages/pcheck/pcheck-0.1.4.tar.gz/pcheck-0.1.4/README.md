# Proxy Checker and Saver

## Overview

This Python script tests a list of proxies to determine which ones are working and saves the working proxies to an output file. It uses `aiohttp` for asynchronous HTTP requests, allowing it to efficiently check multiple proxies in parallel.

## Features

- Asynchronously checks a list of proxies.
- Tests proxies against a user-defined URL.
- Supports authentication in proxy URLs.
- Saves working proxies to a specified output file.
- Provides real-time progress updates on the command line.


## Requirements

- Python 3.7 or higher
- `pip` library

You can install the required library using pip:

```sh
pip install pcheck
```

## Usage
```sh
pcheck -i INPUT_FILE -o OUTPUT_FILE [-u TEST_URL] [-t TIMEOUT]
```


## Command-Line Arguments
```
    -i, --input: Path to the input file containing proxies. Each proxy should be on a new line.
    -o, --output: Path to the output file where working proxies will be saved.
    -u, --url: URL to test proxies against (default is http://httpbin.org/ip).
    -t, --timeout: Timeout for proxy requests in seconds (default is 5).
```

## Example

To test proxies listed in proxies.txt, save working proxies to working_proxies.txt, and test against http://example.com with a timeout of 10 seconds:

```sh
pcheck -i proxies.txt -o working_proxies.txt -u http://example.com -t 10
```

## Proxy Format

The script supports proxies in the following formats:

```
    username:password@host:port
    host:port:username:password
```

Make sure to provide proxies in one of these formats to ensure proper parsing.

## Output

The script writes the working proxies to the specified output file, with each proxy on a new line. It also displays real-time progress on the console, including the number of working and invalid proxies, checks per second, and the number of remaining proxies.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
## Contact

For any questions or issues, please contact rootcode@duck.com or open an issue here.
