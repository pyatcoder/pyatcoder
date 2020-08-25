import sys
from pyatcoder.atcoder_pythran import main as pythran_main
from pyatcoder.tools.envgen import main as envgen_main
from pyatcoder.tools.submit import main as submit_main


def usage_message():
    print("Usage:")
    print("pyatcoder pythran file -- Create code for submit to Atcoder compiled by pythran")
    print("pytcoder gen -- to generate example")
    print("pytcoder submit file -- to submit a code to atcoder")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("pythran", "gen", "submit"):
        usage_message()
        sys.exit(-1)

    prog = " ".join(sys.argv[:2])
    args = sys.argv[2:]

    if sys.argv[1] == "pythran":
        pythran_main(prog, args)

    if sys.argv[1] == "gen":
        envgen_main(prog, args)
        pass

    if sys.argv[1] == "submit":
        submit_main(prog, args)
        pass


if __name__ == '__main__':
    main()