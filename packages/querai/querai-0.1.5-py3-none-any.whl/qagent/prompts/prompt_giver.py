class PromptLib:
    text2network = (
        "Extract a network structure from the input text. "
        "The JSON schema contains a list of nodes and a list of edges. "
        "Each node has the `id, type, label` fields. "
        "Each edge has `source, target, label` fields. "
        "\n"
        "Input:"
        "\n"
        "{user_input}"
    )
