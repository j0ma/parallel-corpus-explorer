#!/bin/bash

export SOURCE_LANGUAGE=${SOURCE_LANGUAGE:-English}
export TARGET_LANGUAGE=${TARGET_LANGUAGE:-English}

export SOURCE_SENTENCES_FILE=$(find . | fzf | xargs realpath)
export TARGET_SENTENCES_FILE=$(find . | fzf | xargs realpath)

cd flask_app

gunicorn app:app
