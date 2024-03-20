# idoven-challenge

## Main dependencies

Pipenv is used to install and track package dependencies. Both in the Docker file and in the manual approach, the dependencies are installed from the `Pipenv.lock` file (using `sync`) in order to get the exact same environment I've been using during the development of the challenge.

The main packages used are:

* FastAPI
* uvicorn
* SQLAlchemy
* aiosqlite
* Alembic
* Pydantic
* PyLint
* Black
* PyTest

## Setup

In order to run the challenge, a Pipenv environment has to be created. To do so, run the following command at the root of the project:

```shell
pipenv sync --dev
```

Once the virtual environment has been created, activate it:

```shell
pipenv shell
```

Run the Alembic migrations in order to create the local SQLite database which gives support to the challenge:

```shell
alembic upgrade head
```

At this point, you'll be able to start the FastAPI server and run the tests by using the provided scripts:

```shell
./scripts/dev_server # Will start the FastAPI server listening in port 3000
```

```shell
./scripts/run_tests
```

If you don't want to use Pipenv, I tried to make your life easier and provided Docker configurations for both launching the FastAPI server and running the tests without much fuss.

To do so open a terminal and run the appropriate Make targets:

```shell
make run  # Will start the FastAPI server listening in port 3000
```

```shell
make tests 
```

## API documentation

As usual with FastAPI projects, the documentation is available at [`http://localhost:3000/docs`](http://localhost:3000/docs)

The endpoints for the API are:

---

`/api/login` (POST)

Login endpoint.

The authentication is implemented by using JWT tokens.

The default admin user (created by an Alembic data migration) is:

* **User:** [idoven@example.com](idoven@example.com)
* **Password:** admin1234

The payload for this endpoint must be sent as form data with two keys: `username` and `password`, following the conventions of JWT libraries used in the challenge.

The response of this call, if succesful, will be a JSON including two keys:

* `access_token`: The main JWT access token to be used in subsequent requests
* `refresh_token`: The refresh JWT token to be used when the main one expires

Is the responsibility of the client to store this tokens to be used in the following requests, in which an authorization header will have to be included:

```Authorization: Bearer <access_token>```

---

`/api/user` (GET)

Get all registered users.

Only admin users are able to use this endpoint.

---

`/api/user` (POST)

Create new user.

Payload must be a JSON with the following structure:

```json
{
    "email": "<new user email>",
    "password": "<new user password>",
    "is_admin": true|false
}
```

Only admin users are able to use this endpoint.

---

`/api/user/{user_id}` (GET)

Get existing user info.

Only admin users are able to use this endpoint.

---

`/api/user/{user_id}` (DELETE)

Delete existing user.

Only admin users are able to use this endpoint.

---

`/api/ecg` (POST)

Create new ECG.

Payload must be a JSON with the following structure:

```json
{
    "id": "<new ECG id>",
    "date": "<new ECG date>",
    "leads": [
        { "name": "<lead name 1>", "signal": [1, 2, -3], "sample_count": 3 },
        { "name": "<lead name 2>", "signal": [1, 2, -3, 4, -5] },
    ]
}
```

Only regular users are able to use this endpoint.

---

`/api/ecg/{ecg_id}` (GET)

Get existing ECG.

Current authenticated user will only have access to their ECGs.

Only regular users are able to use this endpoint.

---

`/api/ecg/{ecg_id}` (DELETE)

Delete existing ECG.

Current authenticated user will only have access to their ECGs.

Only regular users are able to use this endpoint.

---

`/api/insights/{ecg_id}` (GET)

Get the insights for existing ECG.

Current authenticated user will only have access to the insights of their ECGs.

Only regular users are able to use this endpoint.

## VSCode settings file

Just in case you're a VSCode user and wan't to reuse my project configuration. I decided against including this in the repository as a proper file cause it's a local and personal settings file and has nothing to do with an official repo.

```json
{
    "files.exclude": {
        "**/.git": true,
        "**/.DS_Store": true,
        "**/Thumbs.db": true,
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/.venv": true,
        "**/.vscode": true,
    },
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.analysis.extraPaths": [
        "${workspaceFolder}/app"
    ],
    "python.envFile": "${workspaceFolder}/.env",
    "python.analysis.autoFormatStrings": true,
    "pylint.args": [
        "--init-hook",
        "import sys; sys.path.insert(0, 'app')"
    ],
    "editor.formatOnType": false,
    "editor.formatOnPaste": false,
    "editor.formatOnSave": true,
    "editor.formatOnSaveMode": "file",
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit",
        },
        "editor.defaultFormatter": "ms-python.black-formatter",
    },
    "black-formatter.importStrategy": "fromEnvironment",
    "black-formatter.interpreter": [
        "${workspaceFolder}/.venv/bin/python"
    ],
    "python.testing.pytestArgs": [
        "app"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true
}
```
