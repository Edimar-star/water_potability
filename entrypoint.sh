#!/bin/bash

ROUTE="$(pwd)/data/keyfile.json"
if [ -f "$ROUTE" ]; then
    python ./data/load_data.py
    python ./data/train_model.py
fi

gunicorn -w 4 -b 0.0.0.0:3000 'server.main:app' & streamlit run ./client/main.py
