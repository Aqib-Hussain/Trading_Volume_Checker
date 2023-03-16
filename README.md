# CpxQueryTool

This is a command line tool that will query our cloud provider x. 

Written in Python, it aims to fulfill all challenge targets given.

## Assumptions

A few assumptions were made in the creation of this tool:
- As it was not mentioned, a server will be deemed unhealthy if it reaches 95% usage in either CPU or Memory utilisation
- If there is only one instance of a service running it will be flagged even if healthy due to there being less than the 2 required healthy instances
- The application will run on port 4445
- The test server will be used when running tests
- Python3.10 will be installed to the following path: C:\Python310\python.exe 

## Installation and Setup

When running the server please use port 4445

Python3.10 was used in development, whilst the application will work on earlier versions it is highly recommended that Python3.10 is used 

Use the package manager pip to install the following:

```bash
pip install typer[all]
```
```bash
pip install responses
```

## Usage

To run the server do the following:

```bash
./cpx_server.py 4445
```

To run the tool do the following:

```bash
./cpxQueryTool.py [OPTIONS]
```

CpxQueryTool offers 4 different options.

- flag: Flags all services with fewer than 2 healthy instances running 
- pservice: Print all running services
- pstats: Print the average CPU/Memory Usage
- track: Track the CPU/Memory usage of all instances of a given service over time until stopped (specify which service by using --givenservice [yourservice])

To review options you can use --help as an argument when running the tool 

## Testing Usage

The test application to be run is cpxTests.py
It can be run by the following:

```bash
./cpxTests.py
```

Mocking of the server was in use for these tests. 

## Choices made, Reasoning and other notes

For this project I decided to use typer as my library of choice for building out the CLI application. 
It allows for a clean interface in the terminal and makes creating CLI applications easy.
Typer also comes with rich which was used to create more beautiful tables.

Whilst I would normally use Argparse for creating CLI applications I felt as though I should take this time as a learning opportunity to use a new technology that I had not tried before.
In the end I was able to fulfill the objectives required using this new technology in the short amount of time I had to learn it. 

In terms of testing unit testing was used in most places however since objective 4 (tracking) involves an external stopping signal (ctrl + c) this was functionally tested instead of unit tested.
Due to the way that Windows outputs ansi characters compared to Linux machines, I needed to change some of the variables based on the operating system used in the automated tests.

If I had more time there are a few things I would improve upon:
- I would take more time to reduce the amount of repeated code
- I would take the time to create more robust test cases, although edge cases were accounted for it would be good to find any that were missed
- The tracking function could have been created neater



