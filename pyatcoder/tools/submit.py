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

ALL_LANGUAGES = {'python', 'pypy3', 'cython'}


def main(prog, args, credential_supplier=None, use_local_session_cache=True) -> bool:
    parser = argparse.ArgumentParser(
        prog=prog,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("file",
                        help="提出するソースコードの PATH")

    parser.add_argument("-c", "--contest",
                        help="コンテスト ID (e.g. abc270)"
                        "[Default] カレントディレクトリ名")

    parser.add_argument("-p", "--problem",
                        help="問題番号 (e.g. a)、大文字でも小文字でも可"
                        "[Default] ファイル名の先頭文字")

    parser.add_argument("--language", "-l",
                        help="提出するプログラム言語\n"
                             "python, pypy2, pypy3, cython の４つから選択"
                        "[Default] file の拡張子が .py の場合は python、.pyx の場合は cython。")

    parser.add_argument("--timeout", '-t',
                        help="Timeout for each test cases (sec) [Default] 1",
                        type=int,
                        default=1)

    parser.add_argument("--save-no-session-cache",
                        action="store_true",
                        help="Save no session cache to avoid security risk",
                        default=False)

    args = parser.parse_args(args)

    try:
        client = AtCoderClient()
        client.login(save_session_cache=args.save_no_session_cache,
                     credential_supplier=credential_supplier,
                     use_local_session_cache=use_local_session_cache,
                     )
    except LoginError:
        logger.error("Login failed. Try again.")
        return False

    if args.contest:
        contest_id = args.contest
    else:
        contest_id = os.path.basename(os.path.normpath(os.getcwd()))
    if args.problem:
        p = args.problem.lower()
    else:
        p = os.path.basename(args.file)[0]
    problem = Problem(contest=contest_id, alphabet=p.upper(), problem_id=(contest_id + '_' + p))
    if args.language:
        lang = args.language
        if lang not in ALL_LANGUAGES:
            logger.error("プログラム言語は、'python', 'pypy3', 'cython'にしか対応していません。")
            return False
    else:
        ext = os.path.splitext('ab/abc.py')[1]
        if ext == ".py":
            lang = 'python'
        elif ext == ".pyx":
            lang = 'cython'
        else:
            logger.error("対応している拡張子は .py 及び .pyx です。")
            return False

    with open(args.file, 'r') as f:
        source = f.read()
    logger.info(
        "Submitting {} as {}".format(args.file, lang))
    contest = Contest(contest_id)
    submission = client.submit_source_code(
        contest, problem, lang, source)
    logger.info("{} {}".format(
        with_color("Done!", Fore.LIGHTGREEN_EX),
        contest.get_submissions_url(submission)))


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
