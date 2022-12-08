from typing import List


def _convert_raw_house_canary_reponse_to_data(response_data: dict, details: List[str]) -> dict:
    property_data = response_data.get('property/details', {}).get('result', {}).get('property')
    data = {}

    if not property_data:
        return data

    for field in details:

        if field == 'septic':
            value = property_data.get('sewer', '').lower() == field
        else:
            value = property_data[field]

        data[field] = value

    return data


def convert_raw_response_to_data(
    response_data: dict, details: List[str], data_source: str = 'house_canary',
) -> dict:
    if data_source == 'house_canary':
        return _convert_raw_house_canary_reponse_to_data(response_data, details)
    return {}
