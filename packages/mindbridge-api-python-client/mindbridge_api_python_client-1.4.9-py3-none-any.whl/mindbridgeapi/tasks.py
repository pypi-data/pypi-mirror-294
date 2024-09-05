#
#  Copyright MindBridge Analytics Inc. all rights reserved.
#
#  This material is confidential and may not be copied, distributed,
#  reversed engineered, decompiled or otherwise disseminated without
#  the prior written consent of MindBridge Analytics Inc.
#

from dataclasses import dataclass
from functools import cached_property
import logging
import time
from typing import Any, Dict, Generator, Optional
from pydantic import ValidationError
from mindbridgeapi.base_set import BaseSet
from mindbridgeapi.exceptions import (
    ItemAlreadyExistsError,
    ItemNotFoundError,
    UnexpectedServerError,
)
from mindbridgeapi.generated_pydantic_model.model import (
    ActionableErrorResponse,
    ApiTaskCommentCreateOnly,
    MindBridgeQueryTerm,
)
from mindbridgeapi.task_item import TaskItem

logger = logging.getLogger(__name__)


@dataclass
class Tasks(BaseSet):
    @cached_property
    def base_url(self) -> str:
        return f"{self.server.base_url}/tasks"

    def create(self, item: TaskItem, max_wait_minutes: int = 24 * 60) -> TaskItem:
        """Creates a new task

        Creates a new task on the server retrying if needed

        Args:
            item (TaskItem): The task to be created
            max_wait_minutes (int): Maximum minutes to wait (default: `24 * 60`)

        Returns:
            TaskItem: The successfully created task

        Raises:
            ItemAlreadyExistsError: If the item had an id
            TimeoutError: If waited for more than specified
        """
        if getattr(item, "id", None) is not None and item.id is not None:
            raise ItemAlreadyExistsError(item.id)

        init_interval_sec = 7
        max_interval_sec = 60 * 5

        max_wait_seconds = max_wait_minutes * 60
        start_time = time.monotonic()
        elapsed_time = 0.0
        interval_sec = init_interval_sec
        i = 0

        while (time.monotonic() - start_time) < max_wait_seconds:
            loop_start_time = time.monotonic()
            elapsed_time = loop_start_time - start_time
            logger.info(
                f"Attempting to create task. It has been: {elapsed_time:.1f} seconds"
            )
            resp_dict = super()._create(
                url=self.base_url, json=item.create_json, extra_ok_statuses=[423]
            )
            try:
                return TaskItem.model_validate(resp_dict)
            except ValidationError:
                pass

            try:
                response = ActionableErrorResponse.model_validate(resp_dict)
            except ValidationError as err:
                raise UnexpectedServerError(f"{resp_dict}") from err

            if response.status != 423:
                raise UnexpectedServerError(f"{resp_dict}")

            sleep_seconds = interval_sec - (time.monotonic() - loop_start_time)
            logger.info(
                f"Waiting for about {sleep_seconds} seconds as task creation attempt "
                "resulted in: The data table you are trying to access is currently "
                "unavailable, please wait and try again"
            )
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)

            if interval_sec < max_interval_sec:
                interval_sec = min(init_interval_sec * 2**i, max_interval_sec)

            i = i + 1

        else:
            raise TimeoutError(f"Waited too long: {max_wait_minutes} minutes")

    def add_comment(self, id: str, text: str) -> TaskItem:
        url = f"{self.base_url}/{id}/add-comment"
        create_json = ApiTaskCommentCreateOnly(comment_text=text).model_dump(
            by_alias=True
        )
        resp_dict = super()._create(url=url, json=create_json)
        return TaskItem.model_validate(resp_dict)

    def get_by_id(self, id: str) -> TaskItem:
        url = f"{self.base_url}/{id}"
        resp_dict = super()._get_by_id(url=url)
        return TaskItem.model_validate(resp_dict)

    def update(self, item: TaskItem) -> TaskItem:
        if getattr(item, "id", None) is None:
            raise ItemNotFoundError

        url = f"{self.base_url}/{item.id}"
        resp_dict = super()._update(url=url, json=item.update_json)

        return TaskItem.model_validate(resp_dict)

    def get(
        self, json: Optional[Dict[str, Any]] = None
    ) -> Generator[TaskItem, None, None]:
        if json is None:
            json = {}

        json_str = MindBridgeQueryTerm.model_construct(root=json).model_dump_json()
        logger.info(f"Query (get) is: {json_str}")

        if "analysisId" not in json_str:
            raise ValueError(  # noqa: TRY003
                "At least one valid analysisId term must be provided when querying this"
                " entity."
            )

        url = f"{self.base_url}/query"
        for resp_dict in super()._get(url=url, json=json):
            yield TaskItem.model_validate(resp_dict)

    def delete(self, item: TaskItem) -> None:
        if getattr(item, "id", None) is None:
            raise ItemNotFoundError

        url = f"{self.base_url}/{item.id}"
        super()._delete(url=url)
