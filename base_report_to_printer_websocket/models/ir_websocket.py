# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2026 Dixmit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class IrWebsocket(models.AbstractModel):
    _inherit = "ir.websocket"

    def _build_bus_channel_list(self, channels):
        ws_channels = set(
            self.env["printing.printer"]
            .sudo()
            .search([("backend", "=", "websocket"), ("websocket_channel", "!=", False)])
            .mapped("websocket_channel")
        )
        is_printing_user = self.env.uid and self.env.user.has_group(
            "base_report_to_printer.printing_group_user"
        )
        if not is_printing_user:
            channels = [ch for ch in channels if ch not in ws_channels]
        return super()._build_bus_channel_list(channels)
