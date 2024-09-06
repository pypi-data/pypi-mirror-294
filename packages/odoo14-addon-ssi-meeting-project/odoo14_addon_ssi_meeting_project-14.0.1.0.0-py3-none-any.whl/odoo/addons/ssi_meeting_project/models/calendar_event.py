# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class CalendarEvent(models.Model):
    _name = "calendar.event"
    _inherit = [
        "calendar.event",
        "mixin.responsible_task",
    ]

    _responsible_task_create_page = True
