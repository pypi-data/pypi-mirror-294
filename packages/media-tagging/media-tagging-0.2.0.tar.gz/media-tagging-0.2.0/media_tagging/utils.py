# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Various utils."""

import os

import smart_open


def convert_path_to_media_name(media_path: str) -> str:
  """Extracts file name without extension."""
  base_name = media_path.split('/')[-1]
  return base_name.split('.')[0]


def read_media_as_bytes(media_path: str | str | os.PathLike) -> bytes:
  """Reads media content from local or remote storage."""
  with smart_open.open(media_path, 'rb') as f:
    return f.read()
