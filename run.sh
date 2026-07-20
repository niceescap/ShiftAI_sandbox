#!/bin/bash
# Lancement du banc d'essai sur Linux (port 8000, accessible mobile)
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
