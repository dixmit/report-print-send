1. Install and configure *base_report_to_printer* as usual.
2. Create a printer record in **Settings > Printing > Printers** with the
   backend set to **WebSocket**.
3. Set the **System Name** to the name of the target printer as known by
   the client-side listener (e.g. ``MFC-L3750CDW``). Leave it empty to
   use the default system printer.
4. Assign the printer as the default globally, per user, or per report
   following the standard *base_report_to_printer* workflow.
5. Install and run the ``odoo-print-client`` agent on the machine
   connected to the printer

       pip install odoo-print-client
       odoo-printer --url "https://odoo.example.com" --db "prod" --user "admin" --password "admin"

   See `odoo-print-client on PyPI <https://pypi.org/project/odoo-print-client/>`_
   for full configuration options.
