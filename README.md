# Load Generator

A tool for generating HTTP traffic against specified targets in infinite loop.

## Configuration
All configuration options, with default values, are defined in Python file located within the project directory under the path:

`./config/config.py` 

Meaning of individual options is following:

* `REQUESTS` - *list of dictionaries* - List of requests to send, consecutively in a loop. Every dictionary contains information about single request. It has to contain following items:
  * `url` - *string* - url to send the request to.
  * `http_method` - *string* - name of the http method to use when sending the request.
  * `headers` - *dict* - contains http headers to use with the request.
  * `data` - *dict* - URL params in case of GET request or JSON body in case of PUT or POST. Not aplicable in case of DELETE, HEAD and OPTIONS
* `FREQUENCY` - *integer* | *decimal* - number of cycles per second when the requests are being sent. To send requests less frequently than one second use a decimal.
* `RANDOMIZE_FREQUENCY` - *boolean* - if True, the delay between requests will be randomly decreased by the value between 0 and up to full delay.
* `CONCURRENT` - *list of integers* - number of requests sent concurrently, consecutively, during the next cycle.
* `LOG_LEVEL` - *string* - python logging framework logging level.

## Use
The tool is designed to be deployed in k8s cluster and run until killed.

However, it can be also run from commandline by issuing a following command:

```bash
make run
```

## Contributing

Clone the repo and cd:
```bash
$ git clone https://github.vodafone.com/VFGroup-NetworkArchitecture-NAAP/load-generator.git
$ cd load-generator
```

Install project's dependencies (and dev-dependencies) using pip:
```bash
$ make init
```

To run the tests:
```bash
$ make test
```

To run the linter:
```bash
$ make check
```

Run `make help` for a full description.

### Suggested dev tools
Code is formatted using `black` and `isort`, and linting is done via `flake8`.
It is recommended to install these applications on your system.

## Copyright
Copyright 2021 Vodafone.
