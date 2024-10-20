import os
import re
import argparse
import subprocess
from collections import defaultdict


pt_pyext = re.compile(r'\.py$')
pt_from = re.compile(r'^\s*from\s+([^\s]+)')
pt_import = re.compile(r'^\s*import\s+([^\s]+\s*)+')
sub_import = re.compile(r'^\s*import\s+')
sub_as = re.compile(r'\s+as\s+[^\s]+')


# パーサーの作成
parser = argparse.ArgumentParser()

# コマンドライン引数の設定
parser.add_argument("-t", "--target", type=str, help="target directry ")
parser.add_argument("-b", "--base", type=str,
                    default='', help="target directry ")
parser.add_argument("-o", "--output_file", type=str,
                    default='requirements.txt', help="target directry ")
args = parser.parse_args()
"""
def reaf():
    return defaultdict(reaf)

canditates = reaf()
"""

canditates = {}
for root, dirs, files in os.walk(args.target):
    for file in files:

        if pt_pyext.search(file) is None:
            continue
        path = os.path.join(root, file)
        with open(path, encoding='utf-8') as f:
            for line in f.readlines():
                match = pt_from.search(line)

                if match != None:

                    modPath = match.group(1)

                    if modPath.find('.') == 0:

                        continue
                    target = canditates
                    key = modPath.split('.')[0]

                    canditates[key] = True
                match = pt_import.search(line)
                if match != None:

                    for canditate in sub_import.sub('', match.group(0)).split(','):

                        modPath = sub_as.sub('', canditate.strip())
                        if modPath.find('.') == 0:
                            continue
                        key = modPath.split('.')[0]

                        canditates[key] = True


output = subprocess.check_output('pip freeze',  text=True)
output_lines = []
for line in output.splitlines():

    name = re.split(r'\W', line.split('==')[0])[0].lower()

    if name in canditates:
        output_lines.append(line)

if args.base != '':
    path = os.path.abspath(os.path.join(os.getcwd(), args.target, args.base))
    with open(path, encoding='utf-8') as fp:
        output_lines.extend(fp.readlines())
output_text = '\n'.join(output_lines)
path = os.path.abspath(os.path.join(
    os.getcwd(), args.target, args.output_file))
with open(path, encoding='utf-8', mode='w') as fp:
    fp.write(output_text)
print(output_text)
