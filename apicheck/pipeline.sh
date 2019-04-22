#!/bin/bash

pipenv run pytest -v
pipenv run pycodestyle apicheck
