# agenticAI-mcp-client
## Overview
This Kong plugin provides integration with any MCP server. It accepts natural language (NL) input, translates it into a neural/structured query language using LLM-based agents, and invokes the MCP server through a client interface. The plugin then processes the server response and makes it available for downstream consumption or delivery to recipients.

Currently, the plugin supports Mongo MCP server and Gmail MCP server, enabling developers to easily handle reporting requirements across databases. It has the intelligence to automatically generate queries from natural language prompts and deliver the results via email, significantly reducing manual effort.## Tested in Kong Release

## Tested in Kong Release
Kong Enterprise 3.11

## Installation
### Setting up Plugin File
```bash
$ git clone https://github.com/satyajitsial/agenticAI-mcp-client
$ cd agenticAI-mcp-client
$ cp agenticAI-mcp-client.py /usr/local/kong/python-plugins
```
### Setting up Kong PDK
```bash
$ git clone https://github.com/Kong/kong-python-pdk.git
$ copy kong-python-pdk /usr/local/src/
```
### Create .env file to add openAPIKey
```bash
$ vi /usr/local/kong/python-plugins/.env
$ OPENAI_API_KEY="place_open_api_key"
```
### Isntall Required Python dependencies
```bash
$ dnf install python3.11
$ alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 10
$ alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 20
$ alternatives --config python3
$ python3 --version
$ python3 -m pip --version
```
### Install plugin dependencies
```bash
$ python3 -m pip install -r /usr/local/kong/python-plugins/requirements.txt
```
### Restart Kong
```bash
$ kong restart
```
