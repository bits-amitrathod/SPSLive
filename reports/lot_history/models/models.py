# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import datetime

_logger = logging.getLogger(__name__)
class lot_history(models.Model):
    _inherit = 'stock.production.lot'

    pr_sku = fields.Char("SKU/Catalog No", store=False, compute="_calculateSKU")
    pr_name= fields.Char("Product Name", store=False)
    pr_type = fields.Char("Product Type", store=False)
    cr_date = fields.Date("Creation date", store=False)
    vend=fields.Char("Vendor", store=False)
    ph=fields.Char("Phone", store=False)
    email=fields.Char("Email", store=False)
    p_qty = fields.Integer('Qty', store=False)
    @api.multi
    def _calculateSKU(self):
        ACTIONS = {
            "product": "Stockable Product",
            "consu": "Consumable",
            "service": "Service",
        }
        for order in self:
            order.pr_sku = order.product_id.product_tmpl_id.sku_code
            order.pr_name=order.product_id.product_tmpl_id.name
            order.pr_type=(ACTIONS[order.product_id.product_tmpl_id.type])
            order.cr_date=order.create_date
            order.vend=order.product_id.product_tmpl_id.product_brand_id.partner_id.name
            order.ph=order.product_id.product_tmpl_id.product_brand_id.partner_id.phone
            order.email = order.product_id.product_tmpl_id.product_brand_id.partner_id.email
            for p in order.quant_ids:
                order.p_qty = p.quantity
    # @api.multi
    # def get_report_values(self):
    #     lots = self.env['stock.production.lot'].search([])
    #     groupby_dict = {}
    #
    #     for user in self.product_id:
    #         filtered_order = list(filter(lambda x: x.product_id == user, lots))
    #         filtered_by_date = list( filter(lambda x: x.create_date >= self.start_date and x.create_date <= self.end_date, filtered_order))
    #         groupby_dict[user.name] = filtered_by_date
    #
    #
    #         ACTIONS = {
    #             "product": "Stockable Product",
    #             "consu": "Consumable",
    #             "service": "Service",
    #         }
    #
    #
    #
    #         final_dict = {}
    #         for user in groupby_dict.keys():
    #             temp = []
    #             for order in groupby_dict[user]:
    #                 temp_2 = []
    #                 temp_2.append(order.product_id.product_tmpl_id.sku_code)
    #                 temp_2.append(order.name)
    #                 temp_2.append(order.product_id.product_tmpl_id.name)
    #                 temp_2.append(ACTIONS[order.product_id.product_tmpl_id.type])
    #                 temp_2.append(datetime.datetime.strptime(str(order.create_date), '%Y-%m-%d %H:%M:%S').date().strftime('%m-%d-%Y'))
    #                 temp_2.append(order.product_id.product_tmpl_id.product_brand_id.partner_id.name)
    #                 temp_2.append(order.product_id.product_tmpl_id.product_brand_id.partner_id.phone)
    #                 temp_2.append(order.product_id.product_tmpl_id.product_brand_id.partner_id.email)
    #
    #                 temp.append(temp_2)
    #             final_dict[user] = temp
    #
    #     datas = {
    #         'ids': self,
    #         'model': 'product.list.report',
    #         'form': final_dict,
    #         'start_date': fields.Datetime.from_string(str(self.start_date)).date().strftime('%m/%d/%Y'),
    #         'end_date': fields.Datetime.from_string(str(self.end_date)).date().strftime('%m/%d/%Y'),
    #
    #     }
    #     return self.env.ref('lot_history.action_todo_model_report').report_action([], data=datas)
