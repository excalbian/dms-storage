#!/usr/bin/env bash

cd /usr/src/app
flask db upgrade
flask run