import argparse
import ast
import os
import sys
import re

ACL_NAME = 'nbacl'

header = """import sys
if sys.argv[-1] == 'ONLINE_JUDGE':
    import os
    import re
    with open(__file__) as f:
        source = f.read().split('###''nbacl')
    for s in source[1:]:
        s = re.sub("'''.*", '', s)
        sp = s.split(maxsplit=1)
        if os.path.dirname(sp[0]):
            os.makedirs(os.path.dirname(sp[0]), exist_ok=True)
        with open(sp[0], 'w') as f:
            f.write(sp[1])
"""


def get_acl_nodes(node):
    result = []
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.Import):
            for name in child.names:
                if re.match(f'^{ACL_NAME}\\.?', name.name):
                    result.append({'module': '', 'name': name.name})

        elif isinstance(child, ast.ImportFrom):
            if re.match(f'^{ACL_NAME}\\.?', child.module):
                for name in child.names:
                    result.append({'module': child.module, 'name': name.name})
    return result


def search_module(p, sp):
    lib_dir = ""
    lib_dir_list = []
    for n in range(len(p) - 1):
        lib_dir = os.path.join(lib_dir, p[n])
        lib_dir_list.append(p[n])
        lib_file = p[n + 1] + '.py'
        for acl_dir in sp:
            lib_path = os.path.join(acl_dir, lib_dir, lib_file)
            if os.path.isfile(lib_path):
                lib_dir_list.append(lib_file)
                return lib_path, lib_dir_list
    return '', []


def get_modules(imports):
    sp = []
    for p in sys.path:
        acl_dir = os.path.join(p, ACL_NAME)
        if os.path.isdir(acl_dir):
            sp.append(p)
    lib_paths = []
    out_paths = []
    for i in imports:
        if i['module']:
            p = i['module'].split('.') + i['name'].split('.')
        else:
            p = i['name'].split('.')

        lib_path, out_path = search_module(p, sp)
        if lib_path and lib_path not in lib_paths:
            lib_paths.append(lib_path)
            out_paths.append(out_path)
    return lib_paths, out_paths


def execute_output(aot, src, output, my_module, my_module_path, lib_paths, out_paths):
    with open(output, 'w') as f:
        f.write(header)
        if aot:
            f.write(f'    from {my_module_path[:-3]} import cc\n')
            f.write('    cc.compile()\n')
        f.write(src)
        f.write("\n'''")
        if my_module:
            f.write(f'\n###nbacl {my_module_path}\n')
            f.write(my_module)
        for lib_path, out_path in zip(lib_paths, out_paths):
            with open(lib_path) as f_in:
                lib = f_in.read()
            f.write(f'\n###nbacl {"/".join(out_path)}\n')
            f.write(lib)

        f.write("\n'''\n")


def main(prog, args):
    parser = argparse.ArgumentParser(
        prog=" ".join(prog))
    parser.add_argument('-s', '--src', default='main.py', help='Source code')
    if prog[1] == 'combine':
        parser.add_argument('-m', '--module', help='module code')
        parser.add_argument('-o', '--output', default='combined.py', help='Single combined code')
    else:
        parser.add_argument('-m', '--module', default='nbmodule.py', help='module code')
        parser.add_argument('-o', '--output', default='combined_aot.py', help='Single combined code')
    args = parser.parse_args(args)

    with open(args.src) as f:
        src = f.read()
    s = src

    if args.module:
        with open(args.module) as f_in:
            my_module = f_in.read()
        if os.path.dirname(args.module):
            d = os.path.dirname(args.src)
            if args.module.startswith(d):
                my_module_path = args.module[len(d) + 1:]
            else:
                raise ValueError('module は surce と同じか又はその下のディレクトリに置いてください')
        else:
            my_module_path = args.module
        s += '\n' + my_module
    else:
        my_module = None
        my_module_path = None

    imports = get_acl_nodes(ast.parse(s))
    lib_paths, out_paths = get_modules(imports)

    if lib_paths:
        execute_output(prog[1] == 'aot', src, args.output, my_module, my_module_path, lib_paths, out_paths)


if __name__ == '__main__':
    main()
