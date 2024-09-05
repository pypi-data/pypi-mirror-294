#
#  Copyright MindBridge Analytics Inc. all rights reserved.
#
#  This material is confidential and may not be copied, distributed,
#  reversed engineered, decompiled or otherwise disseminated without
#  the prior written consent of MindBridge Analytics Inc.
#

from dataclasses import dataclass
from functools import cached_property
from typing import Any, Dict, Generator, Optional
from mindbridgeapi.analyses import Analyses
from mindbridgeapi.base_set import BaseSet
from mindbridgeapi.engagement_item import EngagementItem
from mindbridgeapi.exceptions import ItemAlreadyExistsError, ItemNotFoundError
from mindbridgeapi.file_manager import FileManager


@dataclass
class Engagements(BaseSet):
    @cached_property
    def base_url(self) -> str:
        return f"{self.server.base_url}/engagements"

    def create(self, item: EngagementItem) -> EngagementItem:
        if getattr(item, "id", None) is not None and item.id is not None:
            raise ItemAlreadyExistsError(item.id)

        url = self.base_url
        resp_dict = super()._create(url=url, json=item.create_json)
        engagement = EngagementItem.model_validate(resp_dict)
        self.restart_file_manager_items(engagement)
        self.restart_analyses(engagement)

        return engagement

    def get_by_id(self, id: str) -> EngagementItem:
        url = f"{self.base_url}/{id}"
        resp_dict = super()._get_by_id(url=url)
        engagement = EngagementItem.model_validate(resp_dict)
        self.restart_file_manager_items(engagement)
        self.restart_analyses(engagement)

        return engagement

    def update(self, item: EngagementItem) -> EngagementItem:
        if getattr(item, "id", None) is None:
            raise ItemNotFoundError

        url = f"{self.base_url}/{item.id}"
        resp_dict = super()._update(url=url, json=item.update_json)

        engagement = EngagementItem.model_validate(resp_dict)
        self.restart_file_manager_items(engagement)
        self.restart_analyses(engagement)

        return engagement

    def get(
        self, json: Optional[Dict[str, Any]] = None
    ) -> Generator[EngagementItem, None, None]:
        if json is None:
            json = {}

        url = f"{self.base_url}/query"
        for resp_dict in super()._get(url=url, json=json):
            engagement = EngagementItem.model_validate(resp_dict)
            self.restart_file_manager_items(engagement)
            self.restart_analyses(engagement)
            yield engagement

    def restart_file_manager_items(self, engagement_item: EngagementItem) -> None:
        if getattr(engagement_item, "id", None) is None:
            raise ItemNotFoundError

        engagement_item.file_manager_items = FileManager(server=self.server).get(
            json={"engagementId": {"$eq": engagement_item.id}}
        )

    def restart_analyses(self, engagement_item: EngagementItem) -> None:
        if getattr(engagement_item, "id", None) is None:
            raise ItemNotFoundError

        engagement_item.analyses = Analyses(server=self.server).get(
            json={"engagementId": {"$eq": engagement_item.id}}
        )

    def delete(self, item: EngagementItem) -> None:
        if getattr(item, "id", None) is None:
            raise ItemNotFoundError

        url = f"{self.base_url}/{item.id}"
        super()._delete(url=url)
