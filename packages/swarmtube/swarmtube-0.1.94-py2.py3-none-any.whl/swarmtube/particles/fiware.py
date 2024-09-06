"""
 `FIWARE` support classes
"""

import asyncio
import json
import re
import sys
import traceback
from datetime import datetime

import aiohttp


from agptools.logs import logger
from agptools.helpers import DATE, camel_case_split

from syncmodels.definitions import (
    ORG_KEY,
    REG_PRIVATE_KEY,
    MONOTONIC_KEY,
    ID_KEY,
)
from syncmodels.crud import parse_duri
from syncmodels.helpers.orion import OrionInjector

from swarmtube import __version__
from ..logic.swarmtube import (
    Particle,
    SkipWave,
    RetryWave,
)


log = logger(__file__)


class OrionParticleSync(Particle):
    """Generic Particle to synchronize data with Orion"""

    # TODO: set by config / yaml
    TARGET_URL = "https://orion.ccoc.spec-cibernos.com"
    # TARGET_URL = "https://orion.ccoc.spec-cibernos.com/v2/entities"
    # Note: for batch update use the following url (doesn't apply right now as is one to one)
    # url = "https://orion.ccoc.spec-cibernos.com/v2/op/update?options=flowControl"

    def __init__(
        self,
        uid,
        sources,
        broker,
        storage,
        target_url=None,
        service=None,
        service_path=None,
    ):
        super().__init__(uid, sources, broker, storage)
        self.target_url = target_url or self.TARGET_URL

        self.service = service
        self.service_path = service_path
        self.orion = OrionInjector(
            self.target_url, self.service, self.service_path
        )

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

        # returning None so no data is really needed to sync
        # just advance the TubeSync wave mark

        for tube_name in ekeys:
            data = edge[tube_name]

            _fquid = parse_duri(tube_name)
            for key, (where, translate) in {
                "path": (
                    'fiware-servicepath',
                    lambda x: x.replace('_', '/'),
                ),
                "thing": ('type', lambda x: x.replace('_', '.')),
            }.items():

                value = _fquid[key]
                value = translate(value)
                data.setdefault(where, value)

            result = await self.orion.push(data)

        return None
