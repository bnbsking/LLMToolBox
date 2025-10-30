from llmtoolbox.common.formatting import get_response_model


def test_get_response_model():
    response_format = {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "hobbies": {"type": "array", "items": {"type": "string"}}
    }

    ResponseModel = get_response_model(response_format)
    person = ResponseModel(name="Alice", age=30, hobbies=["reading", "coding"])

    assert person.name == "Alice"
    assert person.age == 30
    assert person.hobbies == ["reading", "coding"]
    print(person)


if __name__ == "__main__":
    test_get_response_model()
