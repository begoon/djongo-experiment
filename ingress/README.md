# Ingress CMS

## Installation

    python -m venv .venv
    . ./.venv/bin/activate

    pip install flake8 black

    pip install djongo

    pip install pytz

    pip uninstall pymongo 
    pip install pymongo==3.12.3

## Issues

> "Not Implemented Error: Database objects do not implement truth value testing or bool()." while running makemigration

<https://stackoverflow.com/questions/70185942/why-i-am-getting-not-implemented-error-database-objects-do-not-implement-truth>
