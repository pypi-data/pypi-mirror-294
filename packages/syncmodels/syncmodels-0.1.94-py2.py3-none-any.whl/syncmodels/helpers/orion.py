import asyncio
from datetime import datetime
import re
import sys
import traceback

import aiohttp

from agptools.helpers import DATE, camel_case_split
from agptools.logs import logger

from syncmodels.crud import parse_duri
from syncmodels.definitions import (
    ORG_KEY,
    REG_PRIVATE_KEY,
    ID_KEY,
    MONOTONIC_KEY,
    extract_wave,
)

from syncmodels import __version__


# from swarmtube.logic.swarmtube import (
#     SkipWave,
#     RetryWave,
# )


log = logger(__file__)


class OrionInjector:
    """
    Inject data into Orion using async http.
    """

    MAPPER = None
    EXCLUDE = set(["id", "type"])
    HEADER_KEYS = set(["fiware-service", "fiware-servicepath"])
    FULL_EXCLUDE = EXCLUDE.union(HEADER_KEYS)
    TYPES = {
        "ts": "timestamp",
        "date": "timestamp",
        "location": "geo:point",
        str: "string",
        float: "float",
        int: "integer",
    }
    TIMEOUT_INFO = aiohttp.ClientTimeout(
        total=None,
        # total timeout (time consists connection establishment for a new connection
        # or waiting for a free connection from a pool if pool connection limits are exceeded)
        # default value is 5 minutes, set to `None` or `0` for unlimited timeout
        sock_connect=15,
        # Maximal number of seconds for connecting to a peer for a new connection,
        # not given from a pool. See also connect.
        sock_read=15,
        # Maximal number of seconds for reading a portion of data from a peer
    )
    RETRY = 15

    HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": f"OrionInjector/{__version__}",
        # "Accept": "*/*",
        # "Accept-Encoding": "gzip, deflate, br",
        # additional headers for the FIWARE item
        # "fiware-service": "fs_ccoc",
        # "fiware-servicepath": "/beacons/traces",
    }

    # TARGET_URL = "https://orion.ccoc.spec-cibernos.com/v2/entities"
    SERVICE_PATH = ""  # Need to be overridden by the user or use default pattern generation

    ORION_WAVES = {}

    async def get_orion_wave(self, headers, snap):
        key = f"{headers['fiware-service']}:{headers['fiware-servicepath']}/{snap['id']}"
        orion_wave = self.ORION_WAVES.get(key)
        if not orion_wave:
            try:
                async with aiohttp.ClientSession() as session:
                    url = self.target_url + "/v2/entities/{id}".format_map(
                        snap
                    )
                    response = await session.get(url, headers=headers)
                    if response.status < 300:
                        orion_item = await response.json()
                        if "ts" in orion_item:
                            orion_wave = orion_item["ts"].get('value')
                            if orion_wave:
                                orion_wave = DATE(orion_wave)
                                self.ORION_WAVES[key] = orion_wave
            except aiohttp.ClientError as why:
                log.error(why)
                log.error(
                    "".join(traceback.format_exception(*sys.exc_info()))
                )
        return orion_wave

    def update_orion_wave(self, headers, snap, orion_wave):
        key = f"{headers['fiware-service']}:{headers['fiware-servicepath']}/{snap['id']}"
        self.ORION_WAVES[key] = orion_wave

    def __init__(self, target_url, service, service_path):
        self.target_url = target_url
        self.service = service
        self.service_path = service_path
        self.methods = [
            (
                "put",
                self.target_url
                # + "/v2/entities/{id}/attrs?options=append,keyValues",
                + "/v2/entities/{id}/attrs",
                self.FULL_EXCLUDE,
            ),
            (
                "post",
                # self.target_url + "/v2/entities?options=keyValues",
                self.target_url + "/v2/entities",
                [],
            ),
        ]

    def get_service_path(self):
        "Generate service path from class name, removing common prefixes"
        name = self.service_path or self.__class__.__name__

        for ban in "Orion", "Particle", "Sync", "Tube":
            name = name.replace(ban, "")

        tokens = [""] + camel_case_split(name)
        name = "/".join(tokens).lower()
        return name

    def _guess_type(self, key, value):
        "Guess type of a key-value pair based on its value"
        type_ = self.TYPES.get(key)
        if type_ is None:
            if isinstance(value, str):
                x = DATE(value)
                if isinstance(x, datetime):
                    return "timestamp"
            # return default value of 'string'
            type_ = self.TYPES.get(value.__class__, "string")
        return type_

    def _to_snap(self, data):
        "check is data is in 'tube' mode and transform into snapshot"
        meta = {}
        snap = {}
        for key, value in data.items():
            if re.match(REG_PRIVATE_KEY, key):
                meta[key] = value
            else:
                snap[key] = value
        if meta:
            fquid = meta.get(ORG_KEY)
            if fquid:
                _fquid = parse_duri(fquid)
                snap[ID_KEY] = _fquid[ID_KEY]

            wave = meta.get(MONOTONIC_KEY) or extract_wave(data)
            if wave:
                snap["ts"] = DATE(wave)

        return meta, snap

    def _to_fiware(self, data):
        """Create a json for Orion based on given data"""

        # "type" --> entity_type: i.e. beacons.traces
        _id = data.get(ID_KEY)
        if not _id:
            fquid = data.get(ORG_KEY) or data["_path"]

            _uri = parse_duri(fquid)
            entity_id = _uri[ID_KEY]

            # entity_id = tf(entity_id)
            # entity_id = esc(entity_id)
            data["id"] = entity_id
        # data["id"] = str(data[MONOTONIC_KEY])  # --> entity_id

        _ts = data.get("ts")
        if isinstance(_ts, (int, datetime)):
            # "ts": {
            #     "value": "2024-03-06 09:43:11",
            #     "type": "timestamp"
            # },
            date = DATE(_ts)
            # date = datetime.fromtimestamp(_ts / 1000000000)
            # data['ts'] = date.strfmt("%Y-%m-%d %H:%M:%S.%f %z")
            # data['ts'] = date.strftime("%Y-%m-%dT%H:%M:%S.%f")
            # data['ts'] = date.strftime("%Y-%m-%dT%H:%M:%S")  # --> entity_ts
            data["ts"] = {
                "type": "timestamp",
                "value": date.strftime("%Y-%m-%d %H:%M:%S"),  # --> entity_ts
            }
        try:
            data["location"] = "{lat},{lng}".format_map(data)
        except KeyError:
            pass

        data.setdefault(
            "type", self.get_service_path().replace("/", ".")[1:]
        )

        # check if a validation MAPPER is defined
        if self.MAPPER:
            item = self.MAPPER.pydantic(data)
            if item:
                data = item.model_dump(mode="json")
        else:
            # filter any private key when pydantic models are
            # not helping us, so if we need to publish a private
            # key, create a pydantic model that contains the key
            # and this purge will not be executed
            for key in list(data):
                if re.match(REG_PRIVATE_KEY, key):
                    data.pop(key)

        # get headers
        headers = {
            **self.HEADERS,
            "fiware-service": data.pop("fiware-service", self.service),
            "fiware-servicepath": data.pop(
                "fiware-servicepath", self.service_path
            ),
        }
        # try to translate all regular existing fields
        for key in set(data.keys()).difference(self.FULL_EXCLUDE):
            value = data[key]

            if isinstance(value, dict) and not set(value.keys()).difference(
                ["value", "type"]
            ):
                pass
            else:
                data[key] = {
                    "value": value,
                    "type": self._guess_type(key, value),
                }
        return headers, data

    async def _push(self, session, data, headers):
        """
        # Update an entity
        # https://fiware-orion.readthedocs.io/en/1.10.0/user/update_action_types/index.html#update

        201: POST
        204: POST

        400: POST
        # 'type': 'beacons/trace'
        {'error': 'BadRequest', 'description': 'Invalid characters in entity type'}


        400: PATCH
        {'error': 'BadRequest', 'description': 'entity id specified in payload'}
        {'error': 'BadRequest', 'description': 'entity type specified in payload'}
        {'error': 'BadRequest', 'description': 'attribute must be a JSON object, unless keyValues option is used'}
        {'error': 'BadRequest', 'description': 'empty payload'}

        400: DELETE
        {'error': 'BadRequest', 'description': 'Orion accepts no payload for GET/DELETE requests. HTTP header Content-Type is thus forbidden'}


        404: PATCH
        {'error': 'NotFound',  'description': 'The requested entity has not been found. Check type and id'}
        {'error': 'BadRequest','description': 'Service not found. Check your URL as probably it is wrong.'}

        {'orionError': {'code': '400',
                'reasonPhrase': 'Bad Request',
                'details': 'Service not found. Check your URL as probably it '
                           'is wrong.'}}

        422: POST
        {'error': 'Unprocessable', 'description': 'Already Exists'}
        {'error': 'Unprocessable', 'description': 'one or more of the attributes in the request do not exist: ['plate ]'}

        Example of headers

        headers = {
            "Content-Type": "application/json",
            "fiware-service": "fs_ccoc",
            "fiware-servicepath": "/test",
        }
        """
        for method, url, exclude in self.methods:
            method = getattr(session, method)
            url = url.format_map(data)
            _data = {k: v for k, v in data.items() if k not in exclude}
            async with method(
                url,
                json=_data,
                headers=headers,
            ) as response:
                if response.status < 300:
                    break
                if response.headers.get('Content-Length'):
                    reason = await response.json()
                    log.info("Orion [%s]: %s", response.status, reason)
        return response

    async def _compute(self, edge, ekeys):
        """
        # TODO: looks like is a batch insertion! <-----

        Example
        {
        "actionType": "APPEND",
        "entities": [
            {
                "id": "TL1",
                "type": "totem.views",
                "ts": {
                    "value": "2024-03-06 09:43:11",
                    "type": "timestamp"
                },
                "conteo": {
                    "value": 9,
                    "type": "integer"
                },
                "component": {
                    "value": "C11 - TOTEMS",
                    "type": "string"
                },
                "place": {
                    "value": "LUCENTUM",
                    "type": "string"
                },
                "location": {
                    "type": "geo:point",
                    "value": "38.365156979723906,-0.438225677848391"
                }
            }
        ]
        }
        """
        assert len(ekeys) == 1, "Stream must have just 1 input tube"

        # returning None means that no data is really needed for synchronization
        # just advance the TubeSync wave mark
        for tube_name in ekeys:
            data = edge[tube_name]
            return await self.push(data)

    async def push(self, data, **context):
        """try to push data to Orion"""
        response = None
        meta, snap = self._to_snap(data)
        headers, snap = self._to_fiware(snap)

        orion_wave = await self.get_orion_wave(headers, snap)
        swarm_wave = DATE(extract_wave(data))

        if orion_wave and orion_wave > swarm_wave:
            log.warning(
                """Orion has newer wave than the data that we're trying to push, SKIPPING!
                orion_wave: [%s]
                swarm_wave: [%s]
                (other process are updating the same entities?)
                """,
                orion_wave,
                swarm_wave,
            )
            return

        # check 1st time if there is sync problem with orion
        # due SwarmTube's external causes (3rd party situations)
        # update with context
        for key in self.HEADER_KEYS.intersection(context).difference(
            headers
        ):
            headers[key] = context[key]
        if snap:
            for tries in range(0, self.RETRY):
                try:
                    async with aiohttp.ClientSession() as session:
                        response = await self._push(session, snap, headers)
                        self.update_orion_wave(headers, snap, swarm_wave)
                        return response

                except aiohttp.ClientError as why:
                    log.error(why)
                    log.error(
                        "".join(traceback.format_exception(*sys.exc_info()))
                    )
                log.warning("retry: %s: %s", tries, data)
                await asyncio.sleep(0.5)
            return response
