#!/bin/bash

if [ -f "$FILE_PATH" ]; then
    python /app/data/load_data.py
    python /app/data/train_model.py
fi

python /app/server/main.py & streamlit run /app/client/main.py
