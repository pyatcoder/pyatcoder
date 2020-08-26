import os
import numba
from numba.pycc import CC


def compile(file_name):
    """
    :param file_name:
    :return:
    """
    func = []
    signatures = []
    if os.path.exists(config['example']):
        f = os.open(config['example'], os.O_RDONLY)
        stdin_bk = os.dup(0)
        os.dup2(f, 0)
        try:
            module = runpy.run_module(file_name, run_name="__main__")
            for k in module:
                e = module[k]
                if type(e) == numba.targets.registry.CPUDispatcher \
                        and e.nopython_signatures:
                    cc.export(k, e.nopython_signatures[0])(e)
                    func.append(k)
                    signatures.append(str(e.nopython_signatures[0]))
            auto_jit = True
        finally:
            os.dup2(stdin_bk, 0)
            os.close(f)



def main(prog, args):
    path_ = os.path.abspath(args[-1])
    dir_ = os.path.dirname(path_)
    filename = os.path.splitext(os.path.basename(path_))[0]
    make_compile(dir_, filename)
    with open('{}/{}'.format(dir_, filename), 'rb') as f_bin:
        so = f_bin.read()
    gz = gzip.compress(so)
    asc = base64.b64encode(gz)
    write_code(dir_, filename, str(asc))
    exit(0)