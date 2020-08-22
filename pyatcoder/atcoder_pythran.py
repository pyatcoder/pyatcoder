import sys
import os
import gzip
import base64
import subprocess


cc_suffix = '_cc'
exe_name = 'a.out'


def write_code(dir_, filename, s):
    with open('{}/{}{}.py'.format(dir_, filename, cc_suffix), 'w') as f:
        f.write('# compiled by pythran\n')
        f.write('"""\n')
        with open('{}/{}.py'.format(dir_, filename), 'r') as f_origin:
            code = f_origin.read()
        f.write(code)
        if code[-1] != '\n':
            f.write('\n')
        f.write('"""\n')
        f.write('import os, sys\n')
        f.write('p = os.path.dirname(__file__)\n')
        f.write(f'pymain = os.path.join(p, "{exe_name}")\n')
        f.write('if len(sys.argv) == 1:\n')
        f.write('    import subprocess\n')
        f.write('    if p == "":\n')
        f.write('        pymain = "./" + pymain\n')
        f.write('    subprocess.call(pymain)\n')
        f.write('else:\n')
        f.write('    import gzip, base64, stat\n')
        f.write(f'    gz = {s}\n')
        f.write('    bin = gzip.decompress(base64.b64decode(gz))\n')
        f.write('    with open(pymain, "wb") as f:\n')
        f.write('        f.write(bin)\n')
        f.write('    os.chmod(pymain, 0o775)\n')


def make_compile(dir_, filename):
    with open("{}/{}.cpp".format(dir_, filename), "w") as f:
        f.write('#include \"{}.hpp\"\nusing namespace __pythran_{};\n'.format(filename, filename))
        f.write('int main() { main2()(); return 0 ; }')

    cmd = "pythran -e {}/{}.py -o {}/{}.hpp".format(dir_, filename, dir_, filename)
    subprocess.call(cmd.split())
    cmd = "pythran-config -- --cflags"
    p = subprocess.run(cmd.split(), capture_output=True)
    cmd = f"{p.stdout.decode()} -std=c++14 -O3 {dir_}/{filename}.cpp -o {dir_}/{filename}"
    subprocess.call(cmd.split())


def main():
    path_ = os.path.abspath(sys.argv[-1])
    dir_ = os.path.dirname(path_)
    filename = os.path.splitext(os.path.basename(path_))[0]
    make_compile(dir_, filename)
    with open('{}/{}'.format(dir_, filename), 'rb') as f_bin:
        so = f_bin.read()
    gz = gzip.compress(so)
    asc = base64.b64encode(gz)
    write_code(dir_, filename, str(asc))
    exit(0)