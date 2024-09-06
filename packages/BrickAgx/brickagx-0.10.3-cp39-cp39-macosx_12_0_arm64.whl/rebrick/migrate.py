#!/usr/bin/env python3
from pathlib import Path
import itertools
import os
import tempfile
import json
import urllib.request
import zipfile
from io import BytesIO
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Action, SUPPRESS
from rebrick import __version__
from rebrick.Core import BrickContext, parseFromFile, analyze, StringVector, DocumentVector
from rebrick.migrations import collect_migrations, ReplaceOp


class VersionAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(__version__)
        exit(0)

def download_package_version(package_name, version):
    """Download a specific version of a package from PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/{version}/json"
    with urllib.request.urlopen(url, timeout=16) as response:
        content = response.read().decode('utf-8')
    data = json.loads(content)
    return data['urls'][0]['url']

def unzip_package(url, extract_to):
    """Download and unzip a package."""
    with urllib.request.urlopen(url, timeout=32) as response:
        file_data = BytesIO(response.read())
    with zipfile.ZipFile(file_data) as zip_file:
        zip_file.extractall(extract_to)

def parse_args():
    parser = ArgumentParser(description="Migrates a .brick file from an older to a newer version", formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("brickfile", metavar="path", help="the .brick file or directory to migrate")
    parser.add_argument("--version", help="Show version", action=VersionAction, nargs=0, default=SUPPRESS)
    parser.add_argument("--from-version", help="Version to convert from", required=True)
    parser.add_argument("--to-version", help="Version to convert to", default=__version__)
    return parser.parse_known_args()

def refactor_brick_file(brickfile, bundle_path_vec, from_version, to_version):
    print(f"Migrating {brickfile} from {from_version} to {to_version}")
    brick_context = BrickContext(bundle_path_vec)
    migrations = collect_migrations(from_version, to_version)

    path = str(Path(brickfile).absolute())
    parse_result = parseFromFile(path, brick_context)

    analyze(brick_context, None)

    documents = DocumentVector()
    documents.push_back(parse_result[0])
    ops = []

    print(f"Found {len(migrations)} migrations ", [m.__name__ for m in migrations])

    for migration in migrations:
        ops.extend(migration(documents))

    for key, op_group in itertools.groupby(ops, lambda op: op.path):
        with open(key, 'r', encoding="utf8") as file:
            lines = file.readlines()
        lines = ReplaceOp.apply_many(op_group, lines)
        with open(key, 'w', encoding="utf8") as file:
            file.writelines(lines)

def run():
    args, _ = parse_args()

    package_name = 'brickbundles'

    # Download the package
    url = download_package_version(package_name, args.from_version)
    if url is None:
        print(f"Could not find the source distribution for {package_name}=={args.from_version}.")
        return

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_path = str(Path(os.path.realpath(tmpdirname)).absolute())
        print(f"Extracting to temporary directory: {tmp_path}")
        unzip_package(url, tmp_path)
        print(f"Package {package_name}=={args.from_version} extracted to {tmp_path}")
        bundle_path = str((Path(tmp_path) / 'brickbundles').absolute())

        print(f'Using bundle path {bundle_path}')
        print(os.listdir(bundle_path))

        bundle_path_vec = StringVector()
        bundle_path_vec.push_back(bundle_path)

        # Apply the refactoring
        if os.path.isdir(args.brickfile):
            for root, _, files in os.walk(args.brickfile):
                for file in files:
                    if file.endswith(".brick") and not file.endswith("config.brick"):
                        brickfile = os.path.join(root, file)
                        refactor_brick_file(brickfile, bundle_path_vec, args.from_version, args.to_version)
        else:
            refactor_brick_file(args.brickfile, bundle_path_vec, args.from_version, args.to_version)

        print(f"Refactor from {args.from_version} to {args.to_version} complete!")

if __name__ == '__main__':
    run()
