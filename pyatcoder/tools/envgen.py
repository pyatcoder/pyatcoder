#!/usr/bin/python3
import argparse
import os
import sys
import traceback
from os.path import expanduser
import time

from colorama import Fore

from pyatcoder.client.atcoder import AtCoderClient, Contest, LoginError, PageNotFoundError
from pyatcoder.client.models.problem import Problem
from pyatcoder.client.models.problem_content import InputFormatDetectionError, SampleDetectionError
from pyatcoder.common.logging import logger
from pyatcoder.config.config import Config
from pyatcoder.fileutils.create_contest_file import create_examples
from pyatcoder.tools import get_default_config_path
from pyatcoder.tools.utils import with_color


class BannedFileDetectedError(Exception):
    pass


class EnvironmentInitializationError(Exception):
    pass


def output_splitter():
    # for readability
    print("=================================================", file=sys.stderr)


def _message_on_execution(cwd: str, cmd: str):
    return "Executing the following command in `{}`: {}".format(cwd, cmd)


def prepare_procedure(atcoder_client: AtCoderClient,
                      problem: Problem,
                      config: Config,
                      contest_dir_path: str):

    pid = problem.get_alphabet().lower()

    def emit_error(text):
        logger.error(with_color("Problem {}: {}".format(pid, text), Fore.RED))

    def emit_info(text):
        logger.info("Problem {}: {}".format(pid, text))

    # Fetch problem data from the statement
    try:
        content = atcoder_client.download_problem_content(problem)
    except InputFormatDetectionError as e:
        emit_error("Failed to download input format.")
        raise e
    except SampleDetectionError as e:
        emit_error("Failed to download samples.")
        raise e

    # Store examples to the directory path
    if len(content.get_samples()) == 0:
        emit_info("No samples.")
    else:
        create_examples(content.get_samples(), contest_dir_path,
                        config.etc_config.in_example_format + pid + '{}.txt',
                        config.etc_config.out_example_format + pid + '{}.txt')
        emit_info("Created examples.")

    output_splitter()


def prepare_contest(atcoder_client: AtCoderClient,
                    contest_id: str,
                    contest_dir_path: str,
                    config: Config,
                    retry_delay_secs: float = 1.5,
                    retry_max_delay_secs: float = 60,
                    retry_max_tries: int = 10):
    attempt_count = 1
    while True:
        try:
            problem_list = atcoder_client.download_problem_list(
                Contest(contest_id=contest_id))
            break
        except PageNotFoundError:
            if 0 < retry_max_tries < attempt_count:
                raise EnvironmentInitializationError
            logger.warning(
                "Failed to fetch. Will retry in {} seconds. (Attempt {})".format(retry_delay_secs, attempt_count))
            time.sleep(retry_delay_secs)
            retry_delay_secs = min(retry_delay_secs * 2, retry_max_delay_secs)
            attempt_count += 1

    tasks = [(atcoder_client,
              problem,
              config) for
             problem in problem_list]

    output_splitter()

    problems = []
    for argv in tasks:
        problem = argv[1]
        problems.append(problem.get_alphabet())
        try:
            prepare_procedure(argv[0], problem, argv[2], contest_dir_path)
        except Exception:
            # Prevent the script from stopping
            print(traceback.format_exc(), file=sys.stderr)
            pass


USER_CONFIG_PATH = os.path.join(
    expanduser("~"), ".atcodertools.toml")


def get_config(args: argparse.Namespace) -> Config:
    def _load(path: str) -> Config:
        logger.info("Going to load {} as config".format(path))
        with open(path, 'r') as f:
            return Config.load(f, args)

    if args.config:
        return _load(args.config)

    if os.path.exists(USER_CONFIG_PATH):
        return _load(USER_CONFIG_PATH)

    return _load(get_default_config_path())


class DeletedFunctionalityError(Exception):
    pass


def main(prog, args):
    parser = argparse.ArgumentParser(
        prog=prog,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-c", "--contest",
                        help="Contest ID (e.g. arc001)"
                        "[Default] Current directory name")

    parser.add_argument("--without-login",
                        action="store_true",
                        help="Download data without login")

    parser.add_argument("--path",
                        help="Path to example data directory. This script will create examples"
                             " in path/\n"
                             "[Default] Current directory")

    parser.add_argument("--save-no-session-cache",
                        action="store_true",
                        help="Save no session cache to avoid security risk",
                        default=None)

    parser.add_argument("--config",
                        help="File path to your config file\n{0}{1}".format("[Default (Primary)] {}\n".format(
                            USER_CONFIG_PATH),
                            "[Default (Secondary)] {}\n".format(
                                get_default_config_path()))
                        )

    args = parser.parse_args(args)
    config = get_config(args)

    contest_dir_path = os.getcwd()

    if args.contest:
        contest_id = args.contest
    else:
        contest_id = os.path.basename(os.path.normpath(contest_dir_path))

    if args.path:
        contest_dir_path = args.path


    client = AtCoderClient()
    if not config.etc_config.download_without_login:
        try:
            client.login(
                save_session_cache=not config.etc_config.save_no_session_cache)
            logger.info("Login successful.")
        except LoginError:
            logger.error(
                "Failed to login (maybe due to wrong username/password combination?)")
            sys.exit(-1)
    else:
        logger.info("Downloading data without login.")

    prepare_contest(client,
                    contest_id,
                    contest_dir_path,
                    config)


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
