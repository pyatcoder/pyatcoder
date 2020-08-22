#!/usr/bin/python3
import argparse
import sys
import os

from colorama import Fore

from pyatcoder.tools.utils import with_color

from pyatcoder.client.atcoder import AtCoderClient, LoginError
from pyatcoder.common.logging import logger
from pyatcoder.client.models.contest import Contest
from pyatcoder.client.models.problem import Problem
from pyatcoder.common.language import Language

from pyatcoder.tools.models.metadata import Metadata


def main(prog, args, credential_supplier=None, use_local_session_cache=True) -> bool:
    parser = argparse.ArgumentParser(
        prog=prog,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("code_path",
                        help="submit code")

    parser.add_argument("--timeout", '-t',
                        help="Timeout for each test cases (sec) [Default] 1",
                        type=int,
                        default=1)

    parser.add_argument("--save-no-session-cache",
                        action="store_true",
                        help="Save no session cache to avoid security risk",
                        default=False)

    args = parser.parse_args(args)
    basename = os.path.basename(args.code_path)
    dir = os.path.dirname(args.code_path)

    try:
        metadata = Metadata.load_from(os.path.join(dir, "metadata.json"))
    except IOError:
        logger.error(
            '"metadata.json" is not found! You need metadata to use this submission functionality.')
        return False

    try:
        client = AtCoderClient()
        client.login(save_session_cache=args.save_no_session_cache,
                     credential_supplier=credential_supplier,
                     use_local_session_cache=use_local_session_cache,
                     )
    except LoginError:
        logger.error("Login failed. Try again.")
        return False

    contest = Contest(metadata.contest_id)
    p = basename[0]
    problem = Problem(contest=contest, alphabet=p.upper(), problem_id=(metadata.contest_id + '_' + p))
    lang = Language.from_name(metadata.lang)
    with open(args.code_path, 'r') as f:
        source = f.read()
    logger.info(
        "Submitting {} as {}".format(args.code_path, metadata.lang))
    submission = client.submit_source_code(
        contest, problem, lang, source)
    logger.info("{} {}".format(
        with_color("Done!", Fore.LIGHTGREEN_EX),
        contest.get_submissions_url(submission)))


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
