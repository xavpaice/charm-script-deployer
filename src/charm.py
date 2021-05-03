#!/usr/bin/env python3
#
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Deploy an aribtrary script to a specified location."""

import logging
import os

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class ScriptDeployer(CharmBase):
    """Deployer charm."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self._stored.set_default(things=[])

    def _on_config_changed(self, _):
        """Deploy a custom script supplied by config."""
        script = self.config["script"]
        location = self.config["location"]
        logger.debug("Deploying script to %s", location)
        with open(location, 'w') as f:
            f.write(script)
        os.chmod(location, 0o755)
        self.unit.status = ActiveStatus()


if __name__ == "__main__":
    main(ScriptDeployer)
