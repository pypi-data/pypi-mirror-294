#
#  Copyright MindBridge Analytics Inc. all rights reserved.
#
#  This material is confidential and may not be copied, distributed,
#  reversed engineered, decompiled or otherwise disseminated without
#  the prior written consent of MindBridge Analytics Inc.
#

from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Any, Dict, Generator, Optional
from mindbridgeapi.base_set import BaseSet
from mindbridgeapi.chunked_file_item import ChunkedFileItem
from mindbridgeapi.exceptions import ItemAlreadyExistsError, ItemNotFoundError

if TYPE_CHECKING:
    from mindbridgeapi.chunked_file_part_item import ChunkedFilePartItem


@dataclass
class ChunkedFiles(BaseSet):
    @cached_property
    def base_url(self) -> str:
        return f"{self.server.base_url}/chunked-files"

    def create(self, item: ChunkedFileItem) -> ChunkedFileItem:
        if getattr(item, "id", None) is not None and item.id is not None:
            raise ItemAlreadyExistsError(item.id)

        url = self.base_url
        resp_dict = super()._create(url=url, json=item.create_json)

        return ChunkedFileItem.model_validate(resp_dict)

    def get_by_id(self, id: str) -> ChunkedFileItem:
        url = f"{self.base_url}/{id}"
        resp_dict = super()._get_by_id(url=url)

        return ChunkedFileItem.model_validate(resp_dict)

    def get(
        self, json: Optional[Dict[str, Any]] = None
    ) -> Generator[ChunkedFileItem, None, None]:
        if json is None:
            json = {}

        url = f"{self.base_url}/query"
        for resp_dict in super()._get(url=url, json=json):
            yield ChunkedFileItem.model_validate(resp_dict)

    def send_chunk(
        self,
        chunked_file_item: ChunkedFileItem,
        chunked_file_part_item: "ChunkedFilePartItem",
        data: bytes,
    ) -> None:
        if getattr(chunked_file_item, "id", None) is None:
            raise ItemNotFoundError

        url = f"{self.base_url}/{chunked_file_item.id}/part"
        files = {
            "chunkedFilePart": (
                None,
                chunked_file_part_item.create_body,
                "application/json",
            ),
            "fileChunk": (chunked_file_item.name, data),
        }

        super()._upload(url=url, files=files)
