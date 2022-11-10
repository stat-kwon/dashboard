import unittest

from mongoengine import connect, disconnect
from spaceone.core import config, utils
from spaceone.core.transaction import Transaction
from spaceone.core.unittest.result import print_data
from parameterized import parameterized

from spaceone.dashboard.info import DomainDashboardInfo, DomainDashboardsInfo
from spaceone.dashboard.model import DomainDashboard
from spaceone.dashboard.service.domain_dashboard_service import DomainDashboardService
from spaceone.dashboard.error import *
from test.factory import DomainDashboardFactory
from test.factory.domain_dashboard_version_factory import DomainDashboardVersionFactory
from test.lib import *


class TestDomainDashboardService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.dashboard')
        config.set_service_config()
        config.set_global(MOCK_MODE=True)
        connect('test', host='mongomock://localhost')

        cls.domain_id = utils.generate_id('domain')
        cls.transaction = Transaction({
            'service': 'dashboard',
            'api_class': 'DomainDashboard'
        })
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        disconnect()

    def tearDown(self, *args) -> None:
        print()
        print('(tearDown) ==> Delete all data_sources')
        domain_dashboard_vos = DomainDashboard.objects.filter()
        domain_dashboard_vos.delete()

    @parameterized.expand([['user_id', None], ['user_id', 'cloudforet@gmail.com']], name_func=key_value_name_func)
    def test_create_domain_dashboard(self, key, value):
        params = {
            'name': 'test',
            'domain_id': 'domain-12345',
            'dashboard_options': {
                'project_id': 'project-1234'
            },
            'settings': {
                'date_range': {'enabled': False},
                'currency': {'enabled': False}
            }
        }

        if key and value:
            params.update({key: value})

        self.transaction.method = 'create'
        self.transaction.set_meta('user_id', 'cloudforet@gmail.com')
        domain_dashboard_svc = DomainDashboardService(transaction=self.transaction)
        domain_dashboard_vo = domain_dashboard_svc.create(params.copy())

        print_data(domain_dashboard_vo.to_dict(), 'test_create_domain_dashboard')
        DomainDashboardInfo(domain_dashboard_vo)

        self.assertIsInstance(domain_dashboard_vo, DomainDashboard)
        self.assertEqual(params['name'], domain_dashboard_vo.name)
        self.assertEqual(params['dashboard_options']['project_id'],
                         domain_dashboard_vo.dashboard_options.get('project_id'))

    def test_create_domain_dashboard_invalid_user_id(self):
        params = {
            'name': 'test',
            'domain_id': 'domain-12345',
            'dashboard_options': {
                'project_id': 'project-1234'
            },
            'settings': {
                'date_range': {'enabled': False},
                'currency': {'enabled': False}
            },
            'user_id': 'cloudforet2@gmail.com'
        }

        self.transaction.method = 'create'
        self.transaction.set_meta('user_id', 'cloudforet@gmail.com')
        domain_dashboard_svc = DomainDashboardService(transaction=self.transaction)
        with self.assertRaises(ERROR_INVALID_USER_ID):
            domain_dashboard_svc.create(params.copy())

    def test_update_domain_dashboard(self):
        domain_dashboard_vo = DomainDashboardFactory(domain_id=self.domain_id)

        params = {
            'domain_dashboard_id': domain_dashboard_vo.domain_dashboard_id,
            'name': 'update domain dashboard test',
            'settings': {
                'date_range': {'enabled': False},
                'currency': {'enabled': False}
            },
            'tags': {'a': 'b'},
            'domain_id': self.domain_id
        }

        self.transaction.method = 'update'
        domain_dashboard_svc = DomainDashboardService(transaction=self.transaction)
        domain_dashboard_vo = domain_dashboard_svc.update(params.copy())
        print_data(domain_dashboard_vo.to_dict(), 'test_update_project_dashboard')

        self.assertIsInstance(domain_dashboard_vo, DomainDashboard)
        self.assertEqual(params['name'], domain_dashboard_vo.name)

    def test_delete_version(self):
        domain_dashboard_vo = DomainDashboardFactory(domain_id=self.domain_id)
        params = {
            'domain_dashboard_id': domain_dashboard_vo.domain_dashboard_id,
            'name': 'update domain dashboard test',
            'layouts': [{'name': 'widget4'}],
            'settings': {
                'date_range': {'enabled': False},
                'currency': {'enabled': False}
            },
            'tags': {'a': 'b'},
            'domain_id': self.domain_id
        }
        self.transaction.method = 'update'
        domain_dashboard_svc = DomainDashboardService(transaction=self.transaction)
        domain_dashboard_vo = domain_dashboard_svc.update(params.copy())
        print_data(domain_dashboard_vo.to_dict(), 'test_update_project_dashboard')

        params = {
            'domain_dashboard_id': domain_dashboard_vo.domain_dashboard_id,
            'version': 1,
            'domain_id': domain_dashboard_vo.domain_id
        }

        domain_dashboard_svc.delete_version(params.copy())

    def test_delete_latest_version(self):
        domain_dashboard_vo = DomainDashboardFactory(domain_id=self.domain_id)
        params = {
            'domain_dashboard_id': domain_dashboard_vo.domain_dashboard_id,
            'version': 1,
            'domain_id': domain_dashboard_vo.domain_id
        }
        print(params)

        self.transaction.method = 'delete_version'
        domain_dashboard_svc = DomainDashboardService(transaction=self.transaction)
        with self.assertRaises(ERROR_LATEST_VERSION):
            domain_dashboard_svc.delete_version(params.copy())

    def test_revert_version(self):
        pass

    def test_get_version(self):
        pass

    def test_list_versions(self):
        pass

    def test_get_domain_dashboard(self):
        domain_dashboard_vo = DomainDashboardFactory(domain_id=self.domain_id)

        params = {
            'domain_dashboard_id': domain_dashboard_vo.domain_dashboard_id,
            'domain_id': self.domain_id
        }

        self.transaction.method = 'get'
        domain_dashboard_svc = DomainDashboardService(transaction=self.transaction)
        get_domain_dashboard_vo = domain_dashboard_svc.get(params)

        print_data(get_domain_dashboard_vo.to_dict(), 'test_get_domain_dashboard')
        DomainDashboardInfo(get_domain_dashboard_vo)

        self.assertIsInstance(get_domain_dashboard_vo, DomainDashboard)
        self.assertEqual(domain_dashboard_vo.name, get_domain_dashboard_vo.name)
        self.assertEqual(domain_dashboard_vo.domain_dashboard_id, get_domain_dashboard_vo.domain_dashboard_id)

    def test_list_domain_dashboards(self):
        domain_dashboard_vos = DomainDashboardFactory.build_batch(10, domain_id=self.domain_id)
        list(map(lambda vo: vo.save(), domain_dashboard_vos))

        print_data(domain_dashboard_vos[4].to_dict(), "5th domain_dashboard_vo")

        params = {
            'domain_dashboard_id': domain_dashboard_vos[4].domain_dashboard_id,
            'domain_id': self.domain_id
        }

        self.transaction.method = 'list'
        domain_dashboard_svc = DomainDashboardService(transaction=self.transaction)
        list_domain_dashboard_vos, total_count = domain_dashboard_svc.list(params)

        DomainDashboardsInfo(list_domain_dashboard_vos, total_count)

        self.assertEqual(len(list_domain_dashboard_vos), 1)
        self.assertEqual(list_domain_dashboard_vos[0].domain_dashboard_id, params.get('domain_dashboard_id'))
        self.assertIsInstance(list_domain_dashboard_vos[0], DomainDashboard)
        self.assertEqual(total_count, 1)


if __name__ == '__main__':
    unittest.main()
