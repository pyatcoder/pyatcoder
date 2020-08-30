import os
from typing import List

from pyatcoder.client.models.sample import Sample


def _make_text_file(file_path, text):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(text)


def create_example(example: Sample, in_example_name: str, out_example_name: str):
    _make_text_file(in_example_name, example.get_input())
    _make_text_file(out_example_name, example.get_output())


def create_examples(examples: List[Sample],
                    target_dir_path: str,
                    in_example_name_format,
                    out_example_name_format):
    def gen_path(file):
        return os.path.join(target_dir_path, file)

    for index, example in enumerate(examples):
        print(f'in_example_name_format: {in_example_name_format}')
        create_example(example,
                       gen_path(in_example_name_format.format(index + 1)),
                       gen_path(out_example_name_format.format(index + 1)))
