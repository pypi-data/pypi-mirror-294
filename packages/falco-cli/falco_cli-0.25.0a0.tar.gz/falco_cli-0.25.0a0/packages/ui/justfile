set dotenv-load := true

# List all available commands
_default:
    @just --list --unsorted

@fmt:
    hatch fmt --formatter

@dj *ARGS:
    cd demo && hatch run python manage.py {{ ARGS }}

@run-demo:
    cd demo && hatch run python manage.py tailwind runserver