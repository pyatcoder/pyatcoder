import sys
from pyatcoder.atcoder_combine import main as combine_main
from pyatcoder.atcoder_binary import main as binary_main
from pyatcoder.tools.envgen import main as envgen_main
from pyatcoder.tools.submit import main as submit_main
from pyatcoder.atcoder_pythran import main as pythran_main


def usage_message():
    print("Usage:")
    print("pyatcoder combine -- numba acl をファイルに追加して提出できるようにする")
    print("pyatcoder aot -- numba acl をファイルに追加して提出できるようにする　AOT用")
    print("pyatcoder binary -- numba aot でコンパイルしてバイナリで提出")
    print("pytcoder sample -- to generate example")
    print("pytcoder submit file -- to submit a code to atcoder")
    print("pyatcoder pythran file -- Create code for submit to Atcoder compiled by pythran")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("combine", "aot", "binary", "sample", "submit", "pythran"):
        usage_message()
        sys.exit(-1)

    prog = " ".join(sys.argv[:2])
    args = sys.argv[2:]

    if sys.argv[1] == "combine" or sys.argv[1] == "aot":
        combine_main(sys.argv[:2], args)

    elif sys.argv[1] == "binary":
        binary_main(prog, args)

    elif sys.argv[1] == "sample":
        envgen_main(prog, args)

    elif sys.argv[1] == "submit":
        submit_main(prog, args)

    elif sys.argv[1] == "pythran":
        pythran_main(prog, args)


if __name__ == '__main__':
    main()