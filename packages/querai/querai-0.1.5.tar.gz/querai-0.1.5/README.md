# `qagent` - Query Agent

An abstract layer between applications and genAI.

## Installation and Run

### Setup credentials

* In `.env` file add your own `OPENAI_API_KEY` key

### Run

You need to have `poetry` installed first.

1. `poetry install`

2. `poetry shell`

3. Try one example command below.

## Add your own flow

See the first example

## Example

- Example usage of it in a customized usecase:

```bash
python tests/realstuff/01_dummy_question.py
```

- Example configuration of a prompt flow:

```
cat qagent/prompts/dialogflow/example-plan/text-to-table.json
```

- Run tests to see how it works: See Section `Test` below

## Development

### Test

Unitests

```bash
python -m unittest discover tests -v
```
