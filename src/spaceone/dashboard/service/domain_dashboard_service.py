import logging

from spaceone.core.service import *
from spaceone.dashboard.manager import DomainDashboardManager, DomainDashboardVersionManager
from spaceone.dashboard.model import DomainDashboard, DomainDashboardVersion
from spaceone.dashboard.error import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class DomainDashboardService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain_dashboard_mgr: DomainDashboardManager = self.locator.get_manager('DomainDashboardManager')
        self.version_mgr: DomainDashboardVersionManager = self.locator.get_manager('DomainDashboardVersionManager')

    @transaction(append_meta={'authorization.scope': 'DOMAIN_OR_USER'})
    @check_required(['name', 'domain_id'])
    def create(self, params):
        """Register domain_dashboard

        Args:
            params (dict): {
                'name': 'str',
                'layouts': 'list',
                'dashboard_options': 'dict',
                'settings': 'dict',
                'dashboard_options_schema': 'dict',
                'labels': 'list',
                'tags': 'dict',
                'user_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            domain_dashboard_vo (object)
        """

        if 'user_id' in params:
            user_id = params['user_id']
            tnx_user_id = self.transaction.get_meta('user_id')
            if user_id != tnx_user_id:
                raise ERROR_INVALID_USER_ID(user_id=user_id, tnx_user_id=tnx_user_id)
            else:
                params['scope'] = 'USER'
        else:
            params['scope'] = 'DOMAIN'

        domain_dashboard_vo = self.domain_dashboard_mgr.create_domain_dashboard(params)

        version_keys = ['layouts', 'dashboard_options', 'dashboard_options_schema']
        if set(version_keys) <= params.keys():
            self.version_mgr.create_version_by_domain_dashboard_vo(domain_dashboard_vo)

        return domain_dashboard_vo

    @transaction(append_meta={'authorization.scope': 'DOMAIN_OR_USER'})
    @check_required(['domain_dashboard_id', 'domain_id'])
    def update(self, params):
        """Update domain_dashboard

        Args:
            params (dict): {
                'domain_dashboard_id': 'str',
                'name': 'str',
                'layouts': 'list',
                'dashboard_options': 'dict',
                'settings': 'dict',
                'dashboard_options_schema': 'list',
                'labels': 'list',
                'tags': 'dict',
                'domain_id': 'str'
            }

        Returns:
            domain_dashboard_vo (object)
        """

        domain_dashboard_id = params['domain_dashboard_id']
        domain_id = params['domain_id']

        domain_dashboard_vo: DomainDashboard = self.domain_dashboard_mgr.get_domain_dashboard(domain_dashboard_id,
                                                                                              domain_id)

        version_change_keys = ['layouts', 'dashboard_options', 'dashboard_options_schema']
        if self._check_version_change(domain_dashboard_vo, params, version_change_keys):
            self.domain_dashboard_mgr.increase_version(domain_dashboard_vo)
            self.version_mgr.create_version_by_domain_dashboard_vo(domain_dashboard_vo)

        return self.domain_dashboard_mgr.update_domain_dashboard_by_vo(params, domain_dashboard_vo)

    @transaction(append_meta={'authorization.scope': 'DOMAIN_OR_USER'})
    @check_required(['domain_dashboard_id', 'domain_id'])
    def delete(self, params):
        """Deregister domain_dashboard

        Args:
            params (dict): {
                'domain_dashboard_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            None
        """
        self.domain_dashboard_mgr.delete_domain_dashboard(params['domain_dashboard_id'], params['domain_id'])

    @transaction(append_meta={'authorization.scope': 'DOMAIN_OR_USER'})
    @check_required(['domain_dashboard_id', 'domain_id'])
    def get(self, params):
        """ Get domain_dashboard

        Args:
            params (dict): {
                'domain_dashboard_id': 'str',
                'domain_id': 'str',
                'only': 'list
            }

        Returns:
            domain_dashboard_vo (object)
        """
        domain_dashboard_id = params['domain_dashboard_id']
        domain_id = params['domain_id']

        return self.domain_dashboard_mgr.get_domain_dashboard(domain_dashboard_id, domain_id, params.get('only'))

    @transaction(append_meta={'authorization.scope': 'DOMAIN_OR_USER'})
    @check_required(['domain_dashboard_id', 'version', 'domain_id'])
    def delete_version(self, params):
        """ delete version of domain dashboard

        Args:
            params (dict): {
                'domain_dashboard_id': 'str',
                'version': 'int',
                'domain_id': 'str',
            }

        Returns:
            None
        """

        domain_dashboard_id = params['domain_dashboard_id']
        version = params['version']
        domain_id = params['domain_id']

        domain_dashboard_vo = self.domain_dashboard_mgr.get_domain_dashboard(domain_dashboard_id, domain_id)
        current_version = domain_dashboard_vo.version
        if current_version == version:
            raise ERROR_LATEST_VERSION(version=version)

        return self.version_mgr.delete_version(domain_dashboard_id, version, domain_id)

    @transaction(append_meta={'authorization.scope': 'DOMAIN_OR_USER'})
    @check_required(['domain_dashboard_id', 'version', 'domain_id'])
    def revert_version(self, params):
        """ Revert version of domain dashboard

        Args:
            params (dict): {
                'domain_dashboard_id': 'str',
                'version': 'int',
                'domain_id': 'str',
            }

        Returns:
            domain_dashboard_vo (object)
        """

        domain_dashboard_id = params['domain_dashboard_id']
        version = params['version']
        domain_id = params['domain_id']

        domain_dashboard_vo: DomainDashboard = self.domain_dashboard_mgr.get_domain_dashboard(domain_dashboard_id,
                                                                                              domain_id)
        version_vo: DomainDashboardVersion = self.version_mgr.get_version(domain_dashboard_id, version, domain_id)

        params['layouts'] = version_vo.layouts
        params['dashboard_options'] = version_vo.dashboard_options
        params['dashboard_options_schema'] = version_vo.dashboard_options_schema

        return self.domain_dashboard_mgr.update_domain_dashboard_by_vo(params, domain_dashboard_vo)

    @transaction(append_meta={'authorization.scope': 'DOMAIN_OR_USER'})
    @check_required(['domain_dashboard_id', 'version', 'domain_id'])
    def get_version(self, params):
        """ Get version of domain dashboard

        Args:
            params (dict): {
                'domain_dashboard_id': 'str',
                'version': 'int',
                'domain_id': 'str',
                'only': 'list
            }

        Returns:
            domain_dashboard_version_vo (object)
        """

        domain_dashboard_id = params['domain_dashboard_id']
        version = params['version']
        domain_id = params['domain_id']

        return self.version_mgr.get_version(domain_dashboard_id, version, domain_id, params.get('only'))

    @transaction(append_meta={'authorization.scope': 'DOMAIN_OR_USER'})
    @check_required(['domain_dashboard_id', 'domain_id'])
    @append_query_filter(['domain_dashboard_id', 'version', 'domain_id'])
    @append_keyword_filter(['domain_dashboard_id', 'version'])
    def list_versions(self, params):
        """ List versions of domain dashboard

        Args:
            params (dict): {
                'domain_dashboard_id': 'str',
                'version': 'int',
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.Query)'
            }

        Returns:
            domain_dashboard_version_vos (object)
            total_count
        """
        domain_dashboard_id = params['domain_dashboard_id']
        domain_id = params['domain_id']

        query = params.get('query', {})
        domain_dashboard_version_vos, total_count = self.version_mgr.list_versions(query)
        domain_dashboard_vo = self.domain_dashboard_mgr.get_domain_dashboard(domain_dashboard_id, domain_id)
        return domain_dashboard_version_vos, total_count, domain_dashboard_vo.version

    @transaction(append_meta={'authorization.scope': 'DOMAIN_OR_USER'})
    @check_required(['domain_id'])
    @append_query_filter(['domain_dashboard_id', 'name', 'scope', 'user_id', 'domain_id'])
    @append_keyword_filter(['domain_dashboard_id', 'name'])
    def list(self, params):
        """ List public_dashboards

        Args:
            params (dict): {
                'domain_dashboard_id': 'str',
                'name': 'str',
                'scope': 'str',
                'user_id': 'str'
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.Query)'
            }

        Returns:
            domain_dashboard_vos (object)
            total_count
        """

        query = params.get('query', {})
        return self.domain_dashboard_mgr.list_domain_dashboards(query)

    @transaction(append_meta={'authorization.scope': 'DOMAIN_OR_USER'})
    @check_required(['query', 'domain_id'])
    @append_query_filter(['domain_id'])
    @append_keyword_filter(['domain_dashboard_id', 'name'])
    def stat(self, params):
        """
        Args:
            params (dict): {
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)'
            }

        Returns:
            values (list) : 'list of statistics data'

        """
        query = params.get('query', {})
        return self.domain_dashboard_mgr.stat_domain_dashboards(query)

    @staticmethod
    def _check_version_change(domain_dashboard_vo, params, version_change_keys):
        layouts = domain_dashboard_vo.layouts
        dashboard_options = domain_dashboard_vo.dashboard_options
        dashboard_options_schema = domain_dashboard_vo.dashboard_options_schema

        if any(key for key in params if key in version_change_keys):
            if layouts_from_params := params.get('layouts'):
                if layouts != layouts_from_params:
                    return True
            elif options_from_params := params.get('dashboard_options'):
                if dashboard_options != options_from_params:
                    return True
            elif schema_from_params := params.get('dashboard_options_schema'):
                if schema_from_params != dashboard_options_schema:
                    return True
            else:
                return False
