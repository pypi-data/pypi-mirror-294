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
"""Provides CLI for media tagging."""

import argparse
import logging
import os

import smart_open
from gaarf.cli import utils as gaarf_utils

from media_tagging import tagger, utils, writer
from media_tagging.taggers import base as base_tagger


def tag_media(
  media_path: str | os.PathLike,
  tagger_type: base_tagger.BaseTagger,
  writer_type: writer.BaseWriter = writer.JsonWriter(),
  single_output_name: str | None = None,
  tagging_parameters: dict[str, str] | None = None,
) -> None:
  """Runs media tagging algorithm.

  Args:
    media_path: Local or remote path to media file.
    tagger_type: Initialized tagger.
    writer_type: Initialized writer for saving tagging results.
    single_output_name: Parameter for saving results to a single file.
    tagging_parameters: Optional keywords arguments to be sent for tagging.
  """
  media_paths = media_path.split(',')
  if not tagging_parameters:
    tagging_parameters = {}
  results = []
  for path in media_paths:
    media_name = utils.convert_path_to_media_name(path)
    logging.info('Processing media: %s', path)
    with smart_open.open(path, 'rb') as f:
      media_bytes = f.read()
    results.append(
      tagger_type.tag(
        media_name,
        media_bytes,
        tagging_options=base_tagger.TaggingOptions(**tagging_parameters),
      )
    )
  writer_type.write(results, single_output_name)


def main():
  """Main entrypoint."""
  parser = argparse.ArgumentParser()
  parser.add_argument('--media-path', dest='media_path')
  parser.add_argument('--tagger', dest='tagger', default='vision-api')
  parser.add_argument('--writer', dest='writer', default='json')
  parser.add_argument('--output-to-file', dest='output', default=None)
  parser.add_argument('--loglevel', dest='loglevel', default='INFO')
  args, kwargs = parser.parse_known_args()

  concrete_tagger = tagger.create_tagger(args.tagger)
  concrete_writer = writer.create_writer(args.writer)
  tagging_parameters = gaarf_utils.ParamsParser(['tagger']).parse(kwargs)

  logging.basicConfig(
    format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s',
    level=args.loglevel,
    datefmt='%Y-%m-%d %H:%M:%S',
  )
  logging.getLogger(__file__)

  tag_media(
    media_path=args.media_path,
    tagger_type=concrete_tagger,
    writer_type=concrete_writer,
    single_output_name=args.output,
    tagging_parameters=tagging_parameters.get('tagger'),
  )


if __name__ == '__main__':
  main()
