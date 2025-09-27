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
### Setting up Kong Conf File
```bash
$ plugins = bundled,agenticAI-mcp-client
$ custom_plugins_enabled = on
$ pluginserver_names = agenticAI-mcp-client
$ pluginserver_my_plugin_socket = /usr/local/kong/python_pluginserver.sock
$ pluginserver_my_plugin_start_cmd = python3 /usr/local/src/kong-python-pdk/kong-pluginserver.py -d /usr/local/kong/python-plugins
$ pluginserver_my_plugin_query_cmd = python3 /usr/local/src/kong-python-pdk/kong-pluginserver.py -d /usr/local/kong/python-plugins --dump-all-plugins
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
### Install mongo database and Ensure MCP Server is Running

```bash
$ docker run --name mongodb -p 27017:27017 -d mongo:latest
$ npx -y mongodb-mcp-server@latest --transport http
$ git clone https://github.com/mongodb-js/mongodb-mcp-server
$ npm install --save-dev rimraf
```

# Configuration Reference

## Enable the plugin on a Consumer

### Admin-API
For example, configure this plugin on a consumer by making the following request:
```	bash	
  curl -i -X POST http://localhost:8001/plugins --data "name=agenticAI-mcp-client" --data "config.instructions=Translate natural language into MongoDB queries.Use the MongoDB MCP tools to run the queries.Explain results clearly and in human-readable form The DB name is testdb.Return the full query result as JSON without truncating. The connection string for mongodb is <MONGO_CONNECTION_STRING>" --data "config.message=Give the name of users in the users collection whose age>= 30" --data "config.mcp_servers=MongoDB MCP Server" --data "config.urls=<MCP_SERVER_HOST>"
```

## Parameters

| FORM PARAMETER	     														| DESCRIPTION										  													|
| ----------- 																		| -----------																								|
| name<br>Type:string  														|  The name of the plugin to use, in this case agenticAI-mcp-client
 |										  |
| config.instructions<br>Type:string              |  System Prompt for Agents|
| config.message<br>Type:string              |  Reporting queries for Mongo|
| config.mcp_servers<br>Type:string              |  Name MCP Server|
| config.urls<br>Type:string              |  URL of MCP Server|

## Contributors
Developed By : AshalP@verifone.com , AkashA@verifone.com<br>
Designed By  : SatyajitS3@verifone.com, Prema.Namasivayam@verifone.com , RitikB1@verifone.com
