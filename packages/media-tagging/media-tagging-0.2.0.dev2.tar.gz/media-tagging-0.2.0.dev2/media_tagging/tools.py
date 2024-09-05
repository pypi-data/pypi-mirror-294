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
"""Exposes media tagger as a tool for Langchain agents."""

import langchain_core
import smart_open

from media_tagging import tagger, utils
from media_tagging.taggers import base as base_tagger


class MediaTaggingInput(langchain_core.pydantic_v1.BaseModel):
  """Input for text categorization."""

  tagger_type: str = langchain_core.pydantic_v1.Field(
    description='Type of media tagger'
  )
  media_url: str = langchain_core.pydantic_v1.Field(
    description='URL to get media from'
  )


class MediaTaggingResults(langchain_core.tools.BaseTool):
  """Tools that performs text categorization.

  Attributes:
    llm_parameters: Parameter for LLM initialization.
    name: Name of the tool.
    description: Description the tool.
    args_schema: Input model for the tool.
  """

  llm_parameters: dict[str, str] = {'model': 'gemini-1.5-flash'}
  name: str = 'media_tagging_results_json'
  description: str = 'tag media (image or videos)'
  args_schema: type[langchain_core.pydantic_v1.BaseModel] = MediaTaggingInput

  def _run(
    self,
    tagger_type: str,
    media_url: str,
  ) -> list[dict[str, str]]:
    """Performs media tagging based on LLM and vectorstore.

    Args:
      tagger_type: Type of tagger to use for media tagging.
      media_url: URLs of media to be tagged.

    Returns:
      Mappings between medium and its tags.
    """
    media_tagger = tagger.create_tagger(tagger_type)
    media_name = utils.convert_path_to_media_name(media_url)
    with smart_open.open(media_url, 'rb') as f:
      media_bytes = f.read()
    tagging_options = base_tagger.TaggingOptions()
    return media_tagger.tag(
      name=media_name, content=media_bytes, tagging_options=tagging_options
    ).dict()
