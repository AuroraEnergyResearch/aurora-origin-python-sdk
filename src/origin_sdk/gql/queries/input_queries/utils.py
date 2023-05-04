from typing import Dict, Iterable, Union


RecursiveTree = Dict[str, Union[None, Iterable["RecursiveTree"]]]


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
