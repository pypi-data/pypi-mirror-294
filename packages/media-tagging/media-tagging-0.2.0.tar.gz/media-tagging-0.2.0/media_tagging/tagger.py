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
"""Module for performing media tagging.

Media tagging sends API requests to tagging engine (i.e. Google Vision API)
and returns tagging results that can be easily written.
"""

from media_tagging.taggers import api, base, llm

_TAGGERS = {
  'vision-api': api.GoogleVisionAPITagger,
  'video-api': api.GoogleVideoIntelligenceAPITagger,
  'gemini-image': llm.GeminiImageTagger,
  'gemini-structured-image': llm.GeminiImageTagger,
  'gemini-description-image': llm.GeminiImageTagger,
}

_LLM_TAGGERS_TYPES = {
  'gemini-image': llm.LLMTaggerTypeEnum.UNSTRUCTURED,
  'gemini-structured-image': llm.LLMTaggerTypeEnum.STRUCTURED,
  'gemini-description-image': llm.LLMTaggerTypeEnum.DESCRIPTION,
}


def create_tagger(
  tagger_type: str, tagger_parameters: dict[str, str] | None = None
) -> base.BaseTagger:
  """Factory for creating taggers based on provided type.

  Args:
    tagger_type: Type of tagger.
    tagger_parameters: Various parameters to instantiate tagger.

  Returns:
    Concrete tagger class.
  """
  if not tagger_parameters:
    tagger_parameters = {}
  if tagger := _TAGGERS.get(tagger_type):
    if issubclass(tagger, llm.LLMTagger):
      return tagger(
        tagger_type=_LLM_TAGGERS_TYPES.get(tagger_type), **tagger_parameters
      )
    return tagger(**tagger_parameters)
  raise ValueError(
    f'Incorrect tagger {type} is provided, '
    f'valid options: {list(_TAGGERS.keys())}'
  )
