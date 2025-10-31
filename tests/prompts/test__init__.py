from ragentools.prompts import get_prompt_and_response_format


def test_get_prompt_and_response_format():
    prompt, response_format = get_prompt_and_response_format('/app/ragentools/prompts/basic.yaml')
    assert "Hello, I am James" in prompt
    assert response_format == {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "hobbies": {"type": "array", "items": {"type": "string"}}
    }
    print(prompt)
    print(response_format)


if __name__ == "__main__":
    test_get_prompt_and_response_format()
       