# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
import datetime
from odoo.tools import float_repr

_logger = logging.getLogger(__name__)


class inventory_adjustment_report(models.Model):
    _inherit = 'stock.inventory'
    # start_date = fields.Date('Start Date', required=True)
    # end_date = fields.Date(string="End Date", required=True)


    p_sku = fields.Char("Product SKU", store=False, compute="_calculateSKU")
    type= fields.Char("Type", store=False)
    date_cal=fields.Date('Inventory Date',store=False)
    date_posted=fields.Date('Date Posted',store=False)
    amount= fields.Monetary("Amount", store=False)
    total_amt=fields.Monetary("Total Amount", store=False)
    p_qty = fields.Integer('Qty', store=False)
    currency_id = fields.Many2one('res.currency', 'Currency', store=False)



    @api.multi
    def _calculateSKU(self):

        for order in self:
            ACTIONS = {
                "product": "Stockable Product",
                "consu": "Consumable",
                "service": "Service",

            }
            order.p_sku = order.product_id.product_tmpl_id.sku_code
            order.type =order.product_id.product_tmpl_id.type
            order.date_cal=order.date
            order.date_posted=order.date
            order.p_qty=order.line_ids.product_qty
            order.amount = (float_repr(order.product_id.product_tmpl_id.list_price, precision_digits=2))
            # order.total_amt =(float_repr(order.product_qty * order.product_id.product_tmpl_id.list_price, precision_digits=2))
            for order in order.line_ids.product_qty:
                order.p_qty = order

    # @api.model
    # def check(self, data):
    #     if data:
    #         return upper(data)
    #     else:
    #         return " "
    #
    # @api.multi
    # def get_report_values(self):
    #     temp = []
    #     ACTIONS = {
    #         "product": "Stockable Product",
    #         "consu": "Consumable",
    #         "service": "Service",
    #     }
    #     scraps = self.env['stock.scrap'].search([])
    #     for user in scraps:
    #         temp_2 = []
    #         temp_2.append(user.product_id.product_tmpl_id.sku_code)
    #         temp_2.append(
    #             datetime.datetime.strptime(str(user.create_date), '%Y-%m-%d %H:%M:%S').date().strftime('%m/%d/%Y'))
    #         temp_2.append(ACTIONS[user.product_id.product_tmpl_id.type])
    #         temp_2.append(user.scrap_qty)
    #         temp_2.append(user.product_id.product_tmpl_id.list_price)
    #         temp_2.append(user.scrap_qty * user.product_id.product_tmpl_id.list_price)
    #         temp.append(temp_2)
    #
    #     adjustment = self.env['stock.inventory.line'].search([])
    #     groupby_dict = {}
    #     filtered_by_date = list(
    #         filter(lambda x: x.inventory_id.date >= self.start_date and x.inventory_id.date <= self.end_date,
    #                adjustment))
    #     _logger.info('AKASH %r', filtered_by_date)
    #     groupby_dict['data'] = filtered_by_date
    #
    #     final_dict = {}
    #     for user in groupby_dict.keys():
    #
    #         for order in groupby_dict[user]:
    #             temp_2 = []
    #             temp_2.append(order.product_id.product_tmpl_id.sku_code)
    #             temp_2.append(
    #                 datetime.datetime.strptime(str(order.create_date), '%Y-%m-%d %H:%M:%S').date().strftime('%m/%d/%Y'))
    #             temp_2.append(ACTIONS[order.product_id.product_tmpl_id.type])
    #             temp_2.append(order.product_qty)
    #             temp_2.append(float_repr(order.product_id.product_tmpl_id.list_price, precision_digits=2))
    #             temp_2.append(
    #                 float_repr(order.product_qty * order.product_id.product_tmpl_id.list_price, precision_digits=2))
    #
    #             temp.append(temp_2)
    #
    #         final_dict['data'] = temp
    #     final_dict['data'].sort(key=lambda x: self.check(x[0]))
    #     datas = {
    #         'ids': self,
    #         'model': 'inventory.adjustment.report',
    #         'form': final_dict,
    #         'start_date': fields.Datetime.from_string(str(self.start_date)).date().strftime('%m/%d/%Y'),
    #         'end_date': fields.Datetime.from_string(str(self.end_date)).date().strftime('%m/%d/%Y'),
    #
    #     }
    #     return self.env.ref('inventory_adjustment_report.action_todo_model_report').report_action([],
    #                                                                                               data=datas)
