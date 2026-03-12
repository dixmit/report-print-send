# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2026 Dixmit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from base64 import b64encode

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PrintingPrinter(models.Model):
    _inherit = "printing.printer"

    backend = fields.Selection(
        selection_add=[("websocket", "WebSocket")],
        ondelete={"websocket": "cascade"},
    )
    websocket_channel = fields.Char(
        string="WebSocket Channel",
        default="printer",
        help="Channel name used to route print jobs to the correct WebSocket client.",
    )

    def print_document(
        self, report, content, action=None, doc_format="qweb-pdf", **kwargs
    ):
        if self.backend != "websocket":
            return super().print_document(
                report, content, action=action, doc_format=doc_format, **kwargs
            )
        self.ensure_one()
        if isinstance(content, str):
            content = content.encode("utf-8")
        pdf_b64 = b64encode(content).decode("utf-8")
        payload = {
            "printer_name": self.system_name or "",
            "file_data": pdf_b64,
            "file_type": doc_format,
        }
        channel = self.websocket_channel or "printer"
        self.env["bus.bus"]._sendone(channel, "print_job", payload)
        _logger.info("Print job sent via WebSocket to printer '%s'", self.name)
        return True
