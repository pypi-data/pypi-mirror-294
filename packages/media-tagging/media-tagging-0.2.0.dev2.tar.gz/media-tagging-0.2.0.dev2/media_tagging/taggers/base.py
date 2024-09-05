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
"""Module for defining common interface for taggers."""

import abc
import dataclasses
from collections.abc import MutableSequence, Sequence
from typing import Literal

import pydantic


@dataclasses.dataclass
class TaggingOptions:
  """Specifies options to refine media tagging.

  Attributes:
    n_tags: Max number of tags to return.
    tags: Particular tags to find in the media.
  """

  n_tags: int | None = None
  tags: Sequence[str] | None = None

  def __post_init__(self):  # noqa: D105
    if self.tags and not isinstance(self.tags, MutableSequence):
      self.tags = [tag.strip() for tag in self.tags.split(',')]


class Tag(pydantic.BaseModel):
  """Represents a single tag.

  Attributes:
    name: Descriptive name of the tag.
    score: Score assigned to the tag.
  """

  name: str = pydantic.Field(description='tag_name')
  score: float = pydantic.Field(description='tag_score from 0 to 1')


class Description(pydantic.BaseModel):
  """Represents brief description of the media.

  Attributes:
    text: Textual description of the media.
  """

  text: str = pydantic.Field(description='brief description of the media')


class TaggingResult(pydantic.BaseModel):
  """Contains tagging information for a given identifier.

  Attributes:
    identifier: Unique identifier of a media being tagged.
    type: Type of media.
    tags: Tags associated with a given media.
  """

  identifier: str = pydantic.Field(description='media identifier')
  type: Literal['image', 'video'] = pydantic.Field(description='type of media')
  content: list[Tag] | Description = pydantic.Field(
    description='tags or description in the result'
  )


class BaseTagger(abc.ABC):
  """Interface to inherit all taggers from."""

  @abc.abstractmethod
  def tag(
    self,
    name: str,
    content: bytes,
    tagging_options: TaggingOptions = TaggingOptions(),
    **kwargs: str,
  ) -> TaggingResult:
    """Sends media bytes to tagging engine.

    Args:
      name: Identifier of the media content being tagged.
      content: Raw types of the media.
      tagging_options: Parameters to refine the tagging results.
      kwargs: Optional keywords arguments to be sent for tagging.

    Returns:
      Results of tagging.
    """

  def _limit_number_of_tags(
    self, tags: Sequence[Tag], n_tags: int
  ) -> list[Tag]:
    """Returns limited number of tags from the pool.

    Args:
      tags: All tags produced by tagging algorithm.
      n_tags: Max number of tags to return.

    Returns:
      Limited number of tags sorted by the score.
    """
    sorted_tags = sorted(tags, key=lambda x: x.score, reverse=True)
    return sorted_tags[:n_tags]
