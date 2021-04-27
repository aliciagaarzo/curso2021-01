# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Module name",
    "summary": "Module summary",
    "version": "11.0.1.0.0",
    # see https://odoo-community.org/page/development-status
    "development_status": "Alpha|Beta|Production/Stable|Mature",
    "category": "Uncategorized",
    "author": "<AUTHOR(S)>, Odoo Community Association (OCA)",
    # see https://odoo-community.org/page/maintainer-role for a description of the maintainer role and responsibilities
    "license": "AGPL-3",
    "depends": [
        "base",
    ],
    # this feature is only present for 11.0+
    "data": [
       'security/helpdesk_security.xml',
       'security/ir.model.access.csv',
       "views/helpdesk_menu.xml",
       "views/helpdesk_view.xml",
       "views/helpdesk_tag_view.xml",
    ],
}
