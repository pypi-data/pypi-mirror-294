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

import json
import pathlib

from entrypoints import cli
from media_tagging import writer
from media_tagging.taggers import api

_SCRIPT_DIR = pathlib.Path(__file__).parent


def test_image_tagging(fake_tagger, mocker):
  mocker.patch(
    'media_tagging.taggers.api.GoogleVisionAPITagger.tag',
    return_value=fake_tagger.tag(),
  )

  concrete_tagger = api.GoogleVisionAPITagger()
  concrete_writer = writer.JsonWriter()
  image_path = f'{_SCRIPT_DIR}/../unit/data/test_image.jpg'
  image_name = 'test'
  cli.tag_media(
    media_path=image_path,
    tagger_type=concrete_tagger,
    writer_type=concrete_writer,
  )
  with open('test.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

  assert data.get('identifier') == image_name
  assert data.get('type') == 'image'
  assert isinstance(data.get('content'), list)
  assert isinstance(data.get('content')[0], dict)
  assert 'name' in data.get('content')[0]
  assert 'score' in data.get('content')[0]
