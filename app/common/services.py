from config.settings import root

from pathlib import Path


def version():
    commit_hash = None
    head_file_path = '.git/HEAD'

    while head_file_path is not None:
        head_file = Path(root(head_file_path))

        if not (head_file.exists() and head_file.is_file()):
            break

        with head_file.open() as f:
            commit_hash = f.readline().replace('\n', '')

        if not commit_hash.startswith('ref: '):
            head_file_path = None
            continue

        head_file_path = f'.git/{commit_hash[5:]}'

    return commit_hash
