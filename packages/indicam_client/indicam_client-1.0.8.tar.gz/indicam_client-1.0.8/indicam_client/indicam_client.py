""" Client for the Indicam Service API at https://app.hausnet.io/indicam/api.
    See https://docs.hausnet.io/indicam/ for documentation
"""

from __future__ import annotations

import io
from dataclasses import dataclass
import logging

import aiohttp

# Camera config items
CAMCONFIG_MAX_KEY = 'full_perc_from_top'
CAMCONFIG_MIN_KEY = 'empty_perc_from_bottom'
# Connection test results
CONNECT_OK = 0
CONNECT_AUTH_FAIL = 1
CONNECT_FAIL = 2

_LOGGER = logging.getLogger(__name__)


@dataclass
class CamConfig:
    """ Holds the camera configuration. """
    min_perc: float
    max_perc: float


@dataclass
class GaugeMeasurement:
    """ Holds the received measurement for convenient access. """
    body_left: int
    body_right: int
    body_top: int
    body_bottom: int
    float_top: int
    value: float


class IndiCamServiceClient:
    """ API client for the Indicam service. """

    def __init__(self, session: aiohttp.ClientSession, service_url: str, api_key: str) -> None:
        """ Store the service URL and API key for future use. """
        self.req_headers = {
            'Accept': 'application/json',
            'Authorization': f'Token {api_key}',
        }
        self._base_url = service_url
        self._session = session

    async def test_connect(self) -> int:
        """Requests an indicam list from the server, and depending on the success of that, returns one of:
            * CONNECT_OK - Connected and authenticated
            * CONNECT_FAIL - A connection could not be made to the server
            * CONNECT_AUTH_FAIL - Authentication failed
        """
        try:
            async with self._session.get(f'{self._base_url}/indicams/', headers=self.req_headers) as response:
                if response.status == 200:
                    return CONNECT_OK
                elif response.status == 401 or response.status == 403:
                    return CONNECT_AUTH_FAIL
                else:
                    return CONNECT_FAIL
        except aiohttp.ClientError:
            return CONNECT_FAIL

    async def get_indicam_id(self, name: str) -> int | None:
        """ Get a camera's service ID, using the given name """
        async with self._session.get(
            f'{self._base_url}/indicams/?name={name}', headers=self.req_headers
        ) as response:
            if response.status != 200:
                _LOGGER.error(
                    "Failed to find the indicam - handle=%s, status=%d",
                    name,
                    response.status
                )
                return None
            data = await response.json()
            return data['id']

    async def get_camconfig(self, indicam_id: int) -> CamConfig | None:
        """ Get the service's version of the camera configuration. """
        async with self._session.get(
            f'{self._base_url}/indicams/{indicam_id}/camconfig_current/', headers=self.req_headers
        ) as response:
            if response.status != 200:
                _LOGGER.error(
                    'Unable to fetch camera config - status=%d, indicam_id=%d',
                    response.status,
                    indicam_id
                )
                return None
            data = await response.json()
            if CAMCONFIG_MAX_KEY not in data or CAMCONFIG_MIN_KEY not in data:
                _LOGGER.error('Invalid cam_config - json=%s', response.content)
                return None
            return CamConfig(
                min_perc=data[CAMCONFIG_MIN_KEY],
                max_perc=data[CAMCONFIG_MAX_KEY]
            )

    async def create_camconfig(self, indicam_id: int, camconfig: CamConfig) -> bool:
        """ Set the camera configuration at the service. """
        data = {
            'indicam': indicam_id,
            CAMCONFIG_MAX_KEY: camconfig.max_perc,
            CAMCONFIG_MIN_KEY: camconfig.min_perc
        }
        async with self._session.post(
            f'{self._base_url}/camconfigs/', data=data, headers=self.req_headers
        ) as response:
            if response.status != 201:
                _LOGGER.error(
                    'Error creating camera config - status=%d, indicam_id=%d',
                    response.status,
                    indicam_id
                )
                return False
            return True

    async def upload_image(self, device_name, image) -> int | None:
        """ Post the image to the service, for processing, and return the
            image ID returned by the API, None if an error occurred.
        """
        endpoint = f'{self._base_url}/images/{device_name}/upload/'
        data = io.BytesIO(bytearray(image))
        upload_headers = self.req_headers
        upload_headers['Content-Type']  = 'image/jpeg'
        async with self._session.post(endpoint, data=data, headers=upload_headers) as response:
            if response.status != 201:
                _LOGGER.error(
                    'Error uploading image - status=%d',
                    response.status
                )
                return None
            data = await response.json()
            return data['image_id']

    async def measurement_ready(self, image_id: int) -> bool:
        """ Has a measurement been made for the given image? """
        async with self._session.get(f'{self._base_url}/measurements/?src_image={image_id}', headers=self.req_headers) as response:
            if not response or response.status != 200 or not response.content:
                return False
            return True

    async def get_measurement(self, image_id: int) -> GaugeMeasurement | None:
        """ Get the measurement for the submitted image. """
        async with self._session.get(
            f'{self._base_url}/measurements/?src_image={image_id}', headers=self.req_headers
        ) as response:
            if not response or response.status != 200:
                _LOGGER.error(
                    "Error retrieving measurement for image %d', status=%d",
                    image_id,
                    None if not response else response.status
                )
                return None
            data = await response.json()
            result_json = data[0]
            if result_json['error'] == 1:
                _LOGGER.error("Unknown error processing image %d, measurement %d", image_id, result_json['id'])
                return None
            if result_json['error'] == 2:
                _LOGGER.error(
                    "Could not extract measurement from image %d, measurement %d", image_id, result_json['id']
                )
                return None
            measurement = GaugeMeasurement(
                body_left=int(result_json['gauge_left_col']),
                body_right=int(result_json['gauge_right_col']),
                body_top=int(result_json['gauge_top_row']),
                body_bottom=int(result_json['gauge_bottom_row']),
                float_top=int(result_json['float_top_col']),
                value=float(result_json['value'])
            )
            _LOGGER.debug(
                "Measurement received left=%d, right=%d, top=%d, bottom=%d, "
                "float=%d, value=%f",
                measurement.body_left,
                measurement.body_right,
                measurement.body_top,
                measurement.body_bottom,
                measurement.float_top,
                measurement.value
            )
            return measurement
