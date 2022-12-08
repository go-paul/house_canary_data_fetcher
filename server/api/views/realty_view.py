import logging
from json import JSONDecodeError
import os
from typing import Optional
from typing import Tuple

import requests
from flask import current_app as app
from flask import request
from flask.views import MethodView
from requests import RequestException
from requests.adapters import HTTPAdapter

from server.api.schemas.get_parameters import RealtyParametersSchema
from server.converters import convert_raw_response_to_data
from server.utils import http_status
from server.utils.exceptions import BadRequest
from server.utils.exceptions import ServerError

logger = logging.getLogger(__name__)


class RealtyView(MethodView):
    def _validate_get_params(self, parameters: dict) -> dict:
        details = parameters.get('details', '').lower()
        if details.startswith('[') and details.endswith(']'):
            parameters['details'] = [str(i) for i in details[1:-1].split(',')]

        validation_results = RealtyParametersSchema().validate(parameters)
        if validation_results:
            logger.debug(f'GET parameters: {parameters}. Validation: {validation_results}')
            raise BadRequest([
                f'{f}: {" ".join(errors)}'
                for f, errors in validation_results.items()
            ])

        return parameters

    def _make_realty_details_request(
        self,
        url: str,
        get_params: Optional[dict] = None,
        auth: Optional[Tuple[str, str]] = None,
    ) -> dict:
        """ Pull data from external provider
        """
        session = requests.Session()
        session.mount(url, HTTPAdapter(max_retries=5))

        logger.debug(f'Request to: {url}. Params: {get_params}')

        try:
            api_response = session.get(url, params=get_params, auth=auth)
        except RequestException:
            logger.exception('API is not available.')
            raise BadRequest(['Could not get realty data'])

        if api_response.status_code != http_status.HTTP_200_OK:
            logger.error(f'Error: {api_response.text}')
            raise BadRequest(['Could not get realty data'])

        try:
            api_response_dict = api_response.json()
        except (KeyError, JSONDecodeError):
            logger.exception('Recieved data from API could not be serialized.')
            raise BadRequest(['Could not serialize realty data'])

        return api_response_dict

    def get(self) -> Tuple[dict, int]:
        """ `data` field in the response will contain all fields specified in `details` URL param
        """
        get_params = self._validate_get_params(request.args.to_dict())

        data_provider = app.config.get('DATA_PROVIDER')

        # get API credentials by provider
        if data_provider == 'house_canary':
            property_url = app.config.get('HOUSE_CANARY_API_PROPERTY_URL')
            auth_user = app.config.get('HOUSE_CANARY_API_USER')
            auth_password = app.config.get('HOUSE_CANARY_API_PASSWORD')
        else:
            raise ServerError([f'Unsupported data provider `{data_provider}`'])

        # validate API credentials
        if not property_url:
            logger.error('Data provider URL was not set')
            raise BadRequest(['Could not get realty data'])

        # retrieve data
        response_data = self._make_realty_details_request(
            property_url,
            get_params=get_params,
            auth=(auth_user, auth_password),
        )
        data = convert_raw_response_to_data(
            response_data,
            details=get_params['details'],
            data_source=data_provider,
        )

        return {
            'data': data,
            'errors': [],
        }, http_status.HTTP_200_OK
