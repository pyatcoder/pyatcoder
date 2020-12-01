import argparse
import os
import gzip
import base64
from importlib import import_module


header = """import sys
if sys.argv[-1] == 'ONLINE_JUDGE':
    import os
    import re
    with open(__file__) as f:
        binary = f.read().split('###binary')[1].split()
    fname = binary[0]
    gz = binary[1]
    bin = gzip.decompress(base64.b64decode(gz))    
    with open(fname, 'w') as f:
            f.write(bin)
    os.chmod(fname, 0o775)
"""


def main(prog, args):
    parser = argparse.ArgumentParser(
        prog=" ".join(prog))
    parser.add_argument('-s', '--src', default='main.py', help='Source code')
    parser.add_argument('-m', '--module', default='nbmodule.py', help='module code')
    parser.add_argument('-o', '--output', default='binary.py', help='Single combined code compiled by Numba')
    args = parser.parse_args(args)

    module_name = os.path.splitext(args.module)[0]
    module = import_module(module_name)
    module.cc.compile()
    out = module_name + '.cpython-38-x86_64-linux-gnu.so'

    src = header
    with open(args.src) as f:
        src += f.read()

    src += '\n"""\n'

    with open(args.module) as f:
        src += f.read()

    src += '\n###binary'

    with open(out, 'rb') as f_bin:
        so = f_bin.read()
    gz = gzip.compress(so)
    asc = base64.b64encode(gz)
    src += asc
    src += '\n"""\n'

