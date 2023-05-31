#!/bin/bash

cd flask_app

gunicorn app:app
