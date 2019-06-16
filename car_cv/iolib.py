import tarfile
from sys import stdout

import requests


def stream_download(url: str, output_path: str):
    """
    Downloads a file in a streaming fashion (writing data to disk as it is received and then discarding it from
    memory).

    Args:
        url: The URL at which to find the file to be downloaded.
        output_path: The path where the downloaded file will be placed.
    """
    with requests.get(url, stream=True) as req:
        if req.status_code == 200:
            total_size = int(req.headers.get('content-length', None))
            downloaded_size = 0
            with open(output_path, 'wb') as f:
                last_output_length = 0
                for chunk in req.iter_content(chunk_size=4096):
                    downloaded_size += len(chunk)
                    if total_size:
                        output_string = (f'\rAmount downloaded: {downloaded_size:,}/{total_size:,} '
                                         f'({downloaded_size / total_size:.1%})').ljust(last_output_length)

                    else:
                        output_string = f'\rAmount downloaded: {downloaded_size:,}'.ljust(last_output_length)

                    last_output_length = len(output_string)
                    stdout.write(output_string)
                    stdout.flush()
                    f.write(chunk)

                stdout.write('\n')

        else:
            raise RuntimeError(f'Download failed; got HTTP code {req.status}')


def extract_tgz(archive_path: str, output_path: str):
    """
    Extracts files from a gzip-compressed tarball.

    Args:
        archive_path: The path to the archive.
        output_path: The path where the extracted files will be placed.
    """
    with tarfile.open(archive_path, 'r:gz') as f:
        f.extractall(output_path)
