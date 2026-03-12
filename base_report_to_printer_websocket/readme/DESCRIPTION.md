This module extends *base_report_to_printer* to send print jobs through
the Odoo Bus (WebSocket) instead of a traditional print server like CUPS.

When a report is printed, the module encodes the rendered PDF in Base64
and broadcasts it on the ``printer`` bus channel as a ``print_job``
message. A client-side listener (browser extension, desktop agent, etc.)
can then pick up the payload and forward it to the local printer.

Main features:

- No external print server required — works over the existing Odoo Bus.
- Sends print jobs as Base64-encoded PDFs via WebSocket.
- Compatible with the standard *base_report_to_printer* configuration
  (global, per user, per report, per user + report).
- Works with `odoo-print-client <https://pypi.org/project/odoo-print-client/>`_
  as the client-side agent to receive and print jobs.
