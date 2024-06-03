import logging
from typing import Union

from spaceone.core.service import *
from spaceone.core.error import *
from spaceone.dashboard.manager.private_data_table_manager import (
    PrivateDataTableManager,
)
from spaceone.dashboard.manager.private_widget_manager import PrivateWidgetManager
from spaceone.dashboard.model.private_data_table.request import *
from spaceone.dashboard.model.private_data_table.response import *
from spaceone.dashboard.model.private_data_table.database import PrivateDataTable

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class PrivateDataTableService(BaseService):
    resource = "PrivateDataTable"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pri_data_table_mgr = PrivateDataTableManager()

    @transaction(
        permission="dashboard:PrivateDataTable.write",
        role_types=["USER"],
    )
    @convert_model
    def add(
        self, params: PrivateDataTableAddRequest
    ) -> Union[PrivateDataTableResponse, dict]:
        """Add private data table

        Args:
            params (dict): {
                'widget_id': 'str',             # required
                'name': 'str',
                'source_type': 'str',           # required
                'options': 'dict',              # required
                'tags': 'dict',
                'user_id': 'str',               # injected from auth (required)
                'domain_id': 'str',             # injected from auth (required)
            }

        Returns:
            PrivateDataTableResponse:
        """

        pri_widget_mgr = PrivateWidgetManager()
        pri_widget_mgr.get_private_widget(
            params.widget_id,
            params.domain_id,
            params.user_id,
        )

        params_dict = params.dict()
        params_dict["data_type"] = "ADDED"

        pri_data_table_vo = self.pri_data_table_mgr.create_private_data_table(
            params_dict
        )

        return PrivateDataTableResponse(**pri_data_table_vo.to_dict())

    @transaction(
        permission="dashboard:PrivateDataTable.write",
        role_types=["USER"],
    )
    @convert_model
    def transform(
        self, params: PrivateDataTableTransformRequest
    ) -> Union[PrivateDataTableResponse, dict]:
        """Add private data table

        Args:
            params (dict): {
                'widget_id': 'str',             # required
                'name': 'str',
                'operator': 'str',              # required
                'options': 'dict',              # required
                'tags': 'dict',
                'user_id': 'str',               # injected from auth (required)
                'domain_id': 'str',             # injected from auth (required)
            }

        Returns:
            PrivateDataTableResponse:
        """

        pri_widget_mgr = PrivateWidgetManager()
        pri_widget_mgr.get_private_widget(
            params.widget_id,
            params.domain_id,
            params.user_id,
        )

        params_dict = params.dict()
        params_dict["data_type"] = "TRANSFORMED"

        pri_data_table_vo = self.pri_data_table_mgr.create_private_data_table(
            params_dict
        )

        return PrivateDataTableResponse(**pri_data_table_vo.to_dict())

    @transaction(
        permission="dashboard:PrivateDataTable.write",
        role_types=["USER"],
    )
    @convert_model
    def update(
        self, params: PrivateDataTableUpdateRequest
    ) -> Union[PrivateDataTableResponse, dict]:
        """Update private data table

        Args:
            params (dict): {
                'data_table_id': 'str',         # required
                'name': 'str',
                'options': 'dict',
                'tags': 'dict',
                'user_id': 'str',               # injected from auth (required)
                'domain_id': 'str'              # injected from auth (required)
            }

        Returns:
            PrivateDataTableResponse:
        """

        pri_data_table_vo: PrivateDataTable = (
            self.pri_data_table_mgr.get_private_data_table(
                params.data_table_id, params.domain_id, params.user_id
            )
        )

        pri_data_table_vo = self.pri_data_table_mgr.update_private_data_table_by_vo(
            params.dict(exclude_unset=True), pri_data_table_vo
        )

        return PrivateDataTableResponse(**pri_data_table_vo.to_dict())

    @transaction(
        permission="dashboard:PrivateDataTable.write",
        role_types=["USER"],
    )
    @convert_model
    def delete(self, params: PrivateDataTableDeleteRequest) -> None:
        """Delete private data table

        Args:
            params (dict): {
                'data_table_id': 'str',         # required
                'user_id': 'str',               # injected from auth (required)
                'domain_id': 'str'              # injected from auth (required)
            }

        Returns:
            None
        """

        pri_data_table_vo: PrivateDataTable = (
            self.pri_data_table_mgr.get_private_data_table(
                params.data_table_id,
                params.domain_id,
                params.user_id,
            )
        )

        self.pri_data_table_mgr.delete_private_data_table_by_vo(pri_data_table_vo)

    @transaction(
        permission="dashboard:PrivateDataTable.write",
        role_types=["USER"],
    )
    @convert_model
    def load(self, params: PrivateDataTableLoadRequest) -> dict:
        """Load private data table

        Args:
            params (dict): {
                'data_table_id': 'str',         # required
                'granularity': 'str',           # required
                'start': 'str',
                'end': 'str',
                'sort': 'list',
                'page': 'dict',
                'user_id': 'str',               # injected from auth (required)
                'domain_id': 'str'              # injected from auth (required)
            }

        Returns:
            None
        """

        pri_data_table_vo: PrivateDataTable = (
            self.pri_data_table_mgr.get_private_data_table(
                params.data_table_id,
                params.domain_id,
                params.user_id,
            )
        )

        # TODO: Implement load private data table

        return {
            "results": [],
            "total_count": 0,
        }

    @transaction(
        permission="dashboard:PrivateDataTable.read",
        role_types=["USER"],
    )
    @convert_model
    def get(
        self, params: PrivateDataTableGetRequest
    ) -> Union[PrivateDataTableResponse, dict]:
        """Get private data table

        Args:
            params (dict): {
                'data_table_id': 'str',         # required
                'user_id': 'str',               # injected from auth (required)
                'domain_id': 'str'              # injected from auth (required)
            }

        Returns:
            PrivateDataTableResponse:
        """

        pri_data_table_vo: PrivateDataTable = (
            self.pri_data_table_mgr.get_private_data_table(
                params.data_table_id,
                params.domain_id,
                params.user_id,
            )
        )

        return PrivateDataTableResponse(**pri_data_table_vo.to_dict())

    @transaction(
        permission="dashboard:PrivateDataTable.read",
        role_types=["USER"],
    )
    @append_query_filter(
        [
            "widget_id",
            "data_table_id",
            "name",
            "data_type",
            "source_type",
            "operator",
            "domain_id",
            "user_id",
        ]
    )
    @append_keyword_filter(["data_table_id", "name"])
    @convert_model
    def list(
        self, params: PrivateDataTableSearchQueryRequest
    ) -> Union[PrivateDataTablesResponse, dict]:
        """List private data tables

        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v1.Query)'
                'widget_id': 'str',                             # required
                'data_table_id': 'str',
                'name': 'str',
                'data_type': 'str',
                'source_type': 'str',
                'operator': 'str',
                'user_id': 'str',                               # injected from auth (required)
                'domain_id': 'str',                             # injected from auth (required)
            }

        Returns:
            PrivateDataTablesResponse:
        """

        query = params.query or {}
        (
            pri_data_table_vos,
            total_count,
        ) = self.pri_data_table_mgr.list_private_data_tables(query)
        pri_data_tables_info = [
            pri_data_table_vo.to_dict() for pri_data_table_vo in pri_data_table_vos
        ]
        return PrivateDataTablesResponse(
            results=pri_data_tables_info, total_count=total_count
        )