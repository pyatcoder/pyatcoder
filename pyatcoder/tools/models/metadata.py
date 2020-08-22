import json

from pyatcoder.common.language import Language


class Metadata:

    def __init__(self, contest_id: str, problems: list, sample_in_pattern: str, sample_out_pattern: str,
                 lang: str):
        self.contest_id = contest_id
        self.problems = problems
        self.sample_in_pattern = sample_in_pattern
        self.sample_out_pattern = sample_out_pattern
        self.lang = lang

    def to_dict(self):
        return {
            "contest_id": self.contest_id,
            "problems": self.problems,
            "sample_in_pattern": self.sample_in_pattern,
            "sample_out_pattern": self.sample_out_pattern,
            "lang": self.lang,
        }

    @classmethod
    def from_dict(cls, dic):
        return Metadata(
            contest_id=dic["contest_id"],
            problems=dic["problems"],
            sample_in_pattern=dic["sample_in_pattern"],
            sample_out_pattern=dic["sample_out_pattern"],
            lang=dic["lang"],
        )

    @classmethod
    def load_from(cls, filename):
        with open(filename) as f:
            return cls.from_dict(json.load(f))

    def save_to(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=1, sort_keys=True)
            f.write('\n')
