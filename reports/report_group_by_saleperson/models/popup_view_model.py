from odoo import api, fields, models ,_
import datetime

class DiscountSummaryPopUp(models.TransientModel):
    _name = 'saleperson.popup'
    _description = 'Gross Sale By Salesperson'

    compute_at_date = fields.Selection([
        (0, 'Show All '),
        (1, 'Date Range ')
    ], string="Compute", help="Choose to analyze the Show Summary or from a specific date in the past.")

    start_date = fields.Datetime('Start Date', default = (fields.date.today() - datetime.timedelta(days = 31)))
    end_date = fields.Datetime('End Date', default = fields.Datetime.now)

    def open_table(self):

        if self.compute_at_date:
            action = {
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'name': _('Sales Orders'),
                'res_model': 'sale.order',
                'context': {'group_by':'user_id' , 'start_date' : self.start_date , 'end_date' : self.end_date} ,
                'domain':[('state', 'not in', ('draft', 'sent', 'cancel')),('confirmation_date', '>=', self.start_date),('confirmation_date','<=', self.end_date)] ,
            }
            return action
        else:
            action = {
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'name': _('Sales Orders'),
                'res_model': 'sale.order',
                'context': {'group_by':'user_id'},
                'domain': [('state', 'not in', ('draft', 'sent', 'cancel'))],
            }
            return action
