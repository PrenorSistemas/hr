# -*- coding: utf-8 -*-
# Copyright 2015 iDT LABS (http://www.@idtlabs.sl)
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta
from dateutil import rrule
from odoo import fields, models
from odoo.tools.float_utils import float_is_zero


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _get_public_holidays_leaves(self, start_dt, end_dt):
        """Get the public holidays for the current employee and given dates in
        the format expected by resource methods.

        :param: start_dt: Initial datetime.
        :param: end_dt: End datetime.
        :return: List of tuples with (start_date, end_date) as elements.
        """
        self.ensure_one()
        leaves = []
        for day in rrule.rrule(rrule.YEARLY, dtstart=start_dt, until=end_dt):
            lines = self.env['hr.holidays.public'].get_holidays_list(
                day.year, employee_id=self.id,
            )
            for line in lines:
                date = fields.Datetime.from_string(line.date)
                leaves.append((
                    date.replace(hour=0, minute=0, second=0, microsecond=0),
                    date.replace(
                        hour=23, minute=59, second=59, microsecond=999999,
                    ),
                ))
        return leaves

