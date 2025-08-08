# API Tester Tool

A simple and powerful tool for testing APIs with JSON files.

## Features

- Batch testing of API endpoints with JSON files
- Web interface for interactive API testing
- Automatic response saving
- Support for custom headers and authentication

## Installation

```bash
pip install -e . -i https://mirrors.aliyun.com/pypi/simple/
```

## Command Line Usage

```bash
# Test all JSON files in a directory
api-tester --test-dir /path/to/json/files --output-dir results --url https://your-api.com/endpoint --token your-token
```

## Web Interface

```bash
# Start web interface
api-tester --web
```

## Development

```bash
git clone https://github.com/f112o/API-test-for-fastGPT.git
cd api-tester-tool
pip install -e .
```