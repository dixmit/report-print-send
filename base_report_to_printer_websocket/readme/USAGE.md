Once configured, printing works transparently. When a user prints a
report that is set to *Send to Printer* and the assigned printer uses the
**WebSocket** backend, the module will:

1. Render the report as PDF.
2. Encode the PDF content in Base64.
3. Send a ``print_job`` message on the ``printer`` bus channel with the
   following payload

       {
           "printer_name": "<system_name of the printer>",
           "file_data": "<base64-encoded PDF>"
       }

The recommended client-side agent is
`odoo-print-client <https://pypi.org/project/odoo-print-client/>`_,
which listens to the bus channel and forwards jobs to the local printer.
