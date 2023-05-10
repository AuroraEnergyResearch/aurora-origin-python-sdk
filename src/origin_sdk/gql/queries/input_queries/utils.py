from typing import Dict, Union

RecursiveTree = Dict[str, Union["RecursiveTree", None, str, bool, list]]


def get_new_line(level: int):
    return "\n" + "\t" * level


def tree_to_string(tree: RecursiveTree, level=1):
    return (
        (get_new_line(level)).join(
            [
                "{",
                *[
                    key
                    if type(value) != dict
                    else f"""{key} {
                tree_to_string(value, level=level+1)
            }"""
                    for key, value in tree.items()
                ],
            ]
        )
        + f"{get_new_line(level-1)}}}"
    )


transform_fields: RecursiveTree = {"type": None, "value": None}

transform_fields_with_cause: RecursiveTree = {
    **transform_fields,
    "cause": {"reason": None},
}

variable_values: RecursiveTree = {
    "original": None,
    "validationWarnings": None,
    "validationErrors": None,
}

yearly_values_fragment: RecursiveTree = {"year": None, **variable_values}

variable_values_with_transform: RecursiveTree = {
    **variable_values,
    "transform": transform_fields,
}

yearly_values_with_transform: RecursiveTree = {
    "year": None,
    **variable_values_with_transform,
}
