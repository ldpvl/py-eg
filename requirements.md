### Install python packages

    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt

### Generate requirements.txt

    pip list --format=freeze > requirements.txt