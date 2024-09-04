from __future__ import annotations

import io
import os
import pathlib
import asyncio
from typing import overload
import aiohttp
from urllib.parse import urlparse, parse_qs

import anyio
from typing_extensions import TypeGuard

from ._types import (
    FileTypes,
    FileContent,
    RequestFiles,
    HttpxFileTypes,
    Base64FileInput,
    HttpxFileContent,
    HttpxRequestFiles,
)
from ._utils import is_tuple_t, is_mapping_t, is_sequence_t


def is_base64_file_input(obj: object) -> TypeGuard[Base64FileInput]:
    return isinstance(obj, io.IOBase) or isinstance(obj, os.PathLike)


def is_file_content(obj: object) -> TypeGuard[FileContent]:
    return (
        isinstance(obj, bytes)
        or isinstance(obj, tuple)
        or isinstance(obj, io.IOBase)
        or isinstance(obj, os.PathLike)
        or (isinstance(obj, str) and os.path.exists(obj))
    )


def assert_is_file_content(obj: object, *, key: str | None = None) -> None:  # nosec
    if not is_file_content(obj):
        prefix = (
            f"Expected entry at `{key}`"
            if key is not None
            else f"Expected file input `{obj!r}`"
        )
        raise RuntimeError(
            f"{prefix} to be bytes, an io.IOBase instance, PathLike or a tuple but received {type(obj)} instead. See https://github.com/almanak/almanak-python/tree/main#file-uploads"
        ) from None


@overload
def to_httpx_files(files: None) -> None: ...


@overload
def to_httpx_files(files: RequestFiles) -> HttpxRequestFiles: ...


def to_httpx_files(files: RequestFiles | None) -> HttpxRequestFiles | None:
    if files is None:
        return None

    if is_mapping_t(files):
        files = {key: _transform_file(file) for key, file in files.items()}
    elif is_sequence_t(files):
        files = [(key, _transform_file(file)) for key, file in files]
    else:
        raise TypeError(
            f"Unexpected file type input {type(files)}, expected mapping or sequence"
        )

    return files


def _transform_file(file: FileTypes) -> HttpxFileTypes:
    if is_file_content(file):
        if isinstance(file, os.PathLike):
            path = pathlib.Path(file)
            return (path.name, path.read_bytes())

        return file

    if is_tuple_t(file):
        return (file[0], _read_file_content(file[1]), *file[2:])

    raise TypeError(
        f"Expected file types input to be a FileContent type or to be a tuple"
    )


def _read_file_content(file: FileContent) -> HttpxFileContent:
    if isinstance(file, os.PathLike):
        return pathlib.Path(file).read_bytes()
    return file


@overload
async def async_to_httpx_files(files: None) -> None: ...


@overload
async def async_to_httpx_files(files: RequestFiles) -> HttpxRequestFiles: ...


async def async_to_httpx_files(files: RequestFiles | None) -> HttpxRequestFiles | None:
    if files is None:
        return None

    if is_mapping_t(files):
        files = {key: await _async_transform_file(file) for key, file in files.items()}
    elif is_sequence_t(files):
        files = [(key, await _async_transform_file(file)) for key, file in files]
    else:
        raise TypeError(
            "Unexpected file type input {type(files)}, expected mapping or sequence"
        )

    return files


async def _async_transform_file(file: FileTypes) -> HttpxFileTypes:
    if is_file_content(file):
        if isinstance(file, os.PathLike):
            path = anyio.Path(file)
            return (path.name, await path.read_bytes())

        return file

    if is_tuple_t(file):
        return (file[0], await _async_read_file_content(file[1]), *file[2:])

    raise TypeError(
        f"Expected file types input to be a FileContent type or to be a tuple"
    )


async def _async_read_file_content(file: FileContent) -> HttpxFileContent:
    if isinstance(file, os.PathLike):
        return await anyio.Path(file).read_bytes()

    return file


async def upload_file(session, url, file_path):
    if is_file_content(file_path):
        data = await _async_read_file_content(file_path)  # Await the async function
    else:
        raise ValueError(f"File path {file_path} is not a valid file content")

    async with session.put(url, data=data) as response:
        return response.status


async def upload_files(presigned_urls, files):
    async with aiohttp.ClientSession() as session:
        tasks = []
        file_url_mapping = {}

        for url in presigned_urls:
            file_path = match_url_to_file(url, files)
            if file_path:
                if file_path in file_url_mapping:
                    raise Exception(f"Duplicate match found for file: {file_path}")
                file_url_mapping[file_path] = url
            else:
                raise Exception(f"No matching file found for URL: {url}")

        unmatched_files = set(files) - set(file_url_mapping.keys())
        if unmatched_files:
            raise Exception(f"Files not matched to presigned URLs: {unmatched_files}")

        for file_path, url in file_url_mapping.items():
            task = asyncio.create_task(upload_file(session, url, file_path))
            tasks.append(task)

        return await asyncio.gather(*tasks)


def match_url_to_file(url, files):
    # Split by '?' and take the first part
    url_path = url.split("?")[0]

    # Split the remaining path by '/'
    path_parts = url_path.split("/")

    # The file path is everything after the artifact name
    file_path = "/".join(
        path_parts[4:]
    )  # Assuming artifact name is always the 4th part

    # Check for an exact match
    if file_path in files:
        return file_path

    # If no exact match, try matching by basename
    basename = os.path.basename(file_path)
    matches = [f for f in files if os.path.basename(f) == basename]

    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        # If multiple matches, find the one with the most matching characters
        best_match = None
        max_match_length = 0

        for match in matches:
            match_length = len(set(match).intersection(set(file_path)))
            if match_length > max_match_length:
                max_match_length = match_length
                best_match = match

        return best_match

    # If no match found, return None
    return None
