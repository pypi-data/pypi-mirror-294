# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class CalendarEvent(models.Model):
    _name = "calendar.event"
    _inherit = [
        "calendar.event",
        "mixin.outsource_work_object",
    ]
    _outsource_work_create_page = True
