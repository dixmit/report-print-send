# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2026 Dixmit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo.tests.common import TransactionCase


class TestIrWebsocket(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.printer = cls.env["printing.printer"].create(
            {
                "name": "WS Printer",
                "system_name": "ws_printer",
                "backend": "websocket",
                "websocket_channel": "warehouse_1",
            }
        )
        cls.group_user = cls.env.ref("base_report_to_printer.printing_group_user")
        cls.public_user = cls.env.ref("base.public_user")

    def _build_string_channel_list(self, user, channels):
        """Call _build_bus_channel_list with the given client channels and
        return only string channels, filtering out record-based channels
        (res.groups, res.partner) to avoid comparison warnings."""
        mock_request = mock.MagicMock()
        mock_request.session.uid = user.id
        with mock.patch("odoo.addons.bus.models.ir_websocket.request", mock_request):
            IrWs = self.env["ir.websocket"].with_user(user)
            result = IrWs._build_bus_channel_list(list(channels))
        return [ch for ch in result if isinstance(ch, str)]

    def test_printing_user_keeps_printer_channel(self):
        """Users with printing group should keep requested printer channels."""
        user = self.env.user
        user.group_ids |= self.group_user
        result = self._build_string_channel_list(user, ["warehouse_1"])
        self.assertIn("warehouse_1", result)

    def test_non_printing_user_gets_printer_channel_filtered(self):
        """Users without printing group should have printer channels removed."""
        self.assertFalse(
            self.public_user.has_group("base_report_to_printer.printing_group_user")
        )
        result = self._build_string_channel_list(self.public_user, ["warehouse_1"])
        self.assertNotIn("warehouse_1", result)

    def test_non_printing_user_keeps_other_channels(self):
        """Non-printer channels should not be filtered for any user."""
        result = self._build_string_channel_list(
            self.public_user, ["warehouse_1", "other_channel"]
        )
        self.assertNotIn("warehouse_1", result)
        self.assertIn("other_channel", result)

    def test_channel_not_in_printers_is_not_filtered(self):
        """Channels that don't match any printer are always kept."""
        result = self._build_string_channel_list(
            self.public_user, ["unrelated_channel"]
        )
        self.assertIn("unrelated_channel", result)
