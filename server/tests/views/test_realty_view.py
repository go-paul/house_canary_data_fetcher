from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from flask import url_for
from requests import Session

from server import create_app
from server.tests.responses import house_canary_response
from server.utils import http_status


class TestRealtyView(TestCase):
    def setUp(self):
        app = create_app()
        app.config.update({
            'TESTING': True,
        })
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()

    def tearDown(self):
        self.app_context.pop()

    @patch.object(Session, 'get')
    def test_realty_view_success(self, mock_session_get):
        mock_session_get.return_value = Mock(
            json=Mock(return_value=house_canary_response),
            status_code=http_status.HTTP_200_OK,
        )

        with self.app_context:
            url = url_for('realty')
            get_params = {
                'city': 'NYC',
                'details': '[septic,year_built,pool]',
                'state': 'NY',
                'street_address': 'Manhattan 1',
                'zip': 10001,
            }
            get_params_string = '&'.join([f'{k}={v}' for k, v in get_params.items()])
            response = self.client.get(f'{url}?{get_params_string}')
            self.assertEqual(
                response.json,
                {
                    'data': {
                        'septic': True,
                        'pool': False,
                        'year_built': 1957,
                    },
                    'errors': [],
                },
            )

    def test_realty_view_no_get_params(self):
        with self.app_context:
            url = url_for('realty')
            response = self.client.get(url)
            errors = response.json['errors']
            errors.sort()

            self.assertEqual(response.json['data'], {})
            self.assertListEqual(
                errors,
                [
                    'city: Missing data for required field.',
                    'details: Missing data for required field.',
                    'state: Missing data for required field.',
                    'street_address: Missing data for required field.',
                    'zip: Missing data for required field.',
                ]
            )
