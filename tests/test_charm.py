import unittest
from unittest.mock import mock_open, patch

from charm import ScriptDeployer
from ops.model import ActiveStatus
from ops.testing import Harness


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.location = "/tmp/foo-test"
        self.harness = Harness(ScriptDeployer)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    @patch('os.chmod')
    @patch('__main__.__builtins__.open', new_callable=mock_open)
    def test_config_changed(self, m_open, mock_chmod):
        self.harness.update_config({"location": self.location,
                                    "script": "#mock data"})

        mock_chmod.assert_called_with(self.location, 0o755)
        m_open.assert_called_with('/tmp/foo-test', 'w')
        handle = m_open()
        handle.write.assert_any_call("#mock data")
        self.assertEqual(self.harness.model.unit.status, ActiveStatus())
