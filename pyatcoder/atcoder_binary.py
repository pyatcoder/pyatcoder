import argparse
import os
import gzip
import base64
from importlib import import_module
import sys


header = """import sys
if sys.argv[-1] == 'ONLINE_JUDGE':
    import os,gzip,base64
    with open(__file__) as f:
        while True:
            line = f.readline()
            if line:
                if line.startswith('###binary'):
                    fname = line.split()[1]
                    gz = f.readline()
                    break
            else:
                exit()
    bin = gzip.decompress(base64.b64decode(gz[2:-1].encode()))
    with open(fname, 'wb') as f:
            f.write(bin)
    os.chmod(fname, 0o775)
"""


def main(prog, args):
    current = os.path.abspath('.')
    sys.path.append(current)

    parser = argparse.ArgumentParser(
        prog=" ".join(prog))
    parser.add_argument('-s', '--src', default='main.py', help='Source code')
    parser.add_argument('-m', '--module', default='nbmodule.py', help='module code')
    parser.add_argument('-o', '--output', default='binary.py', help='Single combined code compiled by Numba')
    args = parser.parse_args(args)

    module_name = os.path.splitext(args.module)[0]
    out = module_name + '.cpython-38-x86_64-linux-gnu.so'
    if os.path.exists(out):
        os.remove(out)
    module = import_module(module_name)
    module.cc.compile()

    src = header
    with open(args.src) as f:
        src += f.read()

    src += '\n"""\n'

    with open(args.module) as f:
        src += f.read()

    src += f'\n###binary {out}\n'

    with open(out, 'rb') as f_bin:
        so = f_bin.read()
    gz = gzip.compress(so)
    asc = str(base64.b64encode(gz))
    src += asc
    src += '\n"""\n'

    with open(args.output, 'w') as f:
        f.write(src)


if __name__ == '__main__':
    main('binary', '')
