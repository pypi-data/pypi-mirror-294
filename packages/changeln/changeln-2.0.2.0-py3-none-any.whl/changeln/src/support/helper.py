"""
Copyright 2021-2024 Vitaliy Zarubin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import glob
import os
from pathlib import Path


# Find file in directory
def find_path_file(extension: str, path: Path) -> Path | None:
    files = glob.glob(f'{path}/*.{extension}')
    if files:
        return Path(files[0])
    return None


# Get full path file
def get_path_file(path: str, none: bool = True, starting: str = None) -> Path | None:
    if not path:
        return None

    if not starting:
        starting = os.getcwd()

    # Format path
    if path.startswith('~/'):
        path = os.path.expanduser(path)
    if path.startswith('./'):
        path = '{}{}'.format(starting, path[1:])
    if path.startswith('../'):
        path = '{}/{}'.format(starting, path)

    # Read path
    path = Path(path)

    if none and not path.is_file():
        return None

    return Path(path)
