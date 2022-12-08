from copy import deepcopy
from unittest import TestCase

from server.converters import convert_raw_response_to_data
from server.tests.responses import house_canary_response


class TesConverters(TestCase):
    def test_converter_all_fields(self):
        response_data = deepcopy(house_canary_response)
        details = ['septic', 'year_built', 'pool']
        data = convert_raw_response_to_data(response_data, details)
        self.assertEqual(
            data,
            {
                'septic': True,
                'pool': False,
                'year_built': 1957,
            }
        )

    def test_converter_no_septic(self):
        response_data = deepcopy(house_canary_response)
        response_data['property/details']['result']['property']['sewer'] = 'municipal'
        details = ['septic', 'year_built', 'pool']
        data = convert_raw_response_to_data(response_data, details)
        self.assertEqual(
            data,
            {
                'septic': False,
                'pool': False,
                'year_built': 1957,
            }
        )

    def test_converter_only_pool(self):
        response_data = deepcopy(house_canary_response)
        details = ['pool']
        data = convert_raw_response_to_data(response_data, details)
        self.assertEqual(
            data,
            {
                'pool': False,
            }
        )
