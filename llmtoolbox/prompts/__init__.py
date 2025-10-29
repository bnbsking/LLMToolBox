from typing import Tuple, Dict
import yaml


def get_prompt_and_response_format(prompt_path: str, replace_dict: dict = {}) -> Tuple[str, Dict]:
    with open(prompt_path, 'r') as file:
        prompt_template = yaml.safe_load(file)

    prompt = prompt_template['prompt']
    replace_dict = prompt_template['default_replacements'] | replace_dict
    response_format = prompt_template['response_format']

    for key, value in replace_dict.items():
        prompt = prompt.replace(f"{{{{ {key} }}}}", value)

    return prompt, response_format
