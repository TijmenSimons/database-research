# Database research

Deze research is uitgevoerd als deel van mijn afstudeeropdracht.

## Requirements

Python version 3.12 or higher.

Docker and docker compose.

## How to run

### Launch all docker containers.

```cmd
docker compose up
```

Head to the pottom of the `main.py` file and update the container ids accordingly.

### Install requirements

```cmd
python -m venv venv

.\venv\Scripts\activate

pip install -r .\requirements.txt
```

### Configuring the tests

In the `main.py` in the `compare` function you can configure which databases you wish to test.

By calling `add_test(N)` you can add a new test to the comparisons. The N indicates how many records will be used in the test.

### Run the tests

```cmd
python .\main.py
```
