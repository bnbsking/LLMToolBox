apt update && apt install -y curl

curl -sSL https://install.python-poetry.org | python3 -

export PATH="$HOME/.local/bin:$PATH"

poetry init

poetry install

poetry shell
