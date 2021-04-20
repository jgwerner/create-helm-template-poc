# create-helm-template-poc

## Overview

Microservice used to create helm custom configs to deploy IllumiDesk services.

## Dev Install

Install in editable mode:

    pip install -e .

## Run Application

Run application locally with debug mode enabled:

```bash
export FLASK_APP=src/templategenerator/templategenerator
export FLASK_ENV=development
flask run
```

## Update Dependencies

    pip-compile dev-requirements.in

## License

MIT
