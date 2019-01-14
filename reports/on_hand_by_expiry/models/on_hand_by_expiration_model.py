# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools
import logging
from datetime import datetime,timedelta

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, pycompat, misc

_logger = logging.getLogger(__name__)


class OnHandByExpiry(models.Model):
    _name = "on_hand_by_expiry"
    _auto = False

    qty = fields.Float("Product Qty")
    product_id = fields.Many2one('product.product', string='Product Name')
    location_id = fields.Many2one('stock.location', string='Location')
    status = fields.Char('Status')
    expiration_date = fields.Datetime("Expiration Date")
    alert_date = fields.Datetime("Alert Date")
    color_value =  fields.Integer("Scrab Location", compute="_set_date_fg_color")
    scrap_location = fields.Boolean("Scrap Location")
    product_sku = fields.Char("Product SKU")


    @api.model_cr
    def init(self):
        self.init_table()

    def init_table(self):
        tools.drop_view_if_exists(self._cr, 'on_hand_by_expiry')
        start_date = self.env.context.get('s_date')
        end_date = self.env.context.get('e_date')
        current_date = fields.Date.to_string(datetime.now())

        sql_query = """  CREATE VIEW on_hand_by_expiry AS (             
            SELECT l.product_id as product_id, l.id as id,                 
                sq.quantity as qty,
                l.use_date as expiration_date,
                l.alert_date as alert_date,
                sq.location_id as location_id,
                sl.scrap_location,
                t.sku_code as product_sku,
                CASE 
                    WHEN l.use_date < '""" + str(current_date) + """' THEN 'Expired'
                    WHEN l.alert_date <= '""" + str(current_date) + """' THEN 'Expiring'
                    WHEN l.alert_date >= '""" + str(current_date) + """' THEN 'Valid'
                END AS status
            FROM 
                stock_production_lot l LEFT JOIN stock_quant sq ON sq.lot_id = l.id 
                LEFT JOIN product_product p ON p.id = sq.product_id LEFT JOIN product_template t 
                ON t.id = p.product_tmpl_id LEFT JOIN stock_location sl On sl.id = sq.location_id 
                
            WHERE 
                sq.quantity > 0 AND sq.lot_id IS NOT NULL AND sq.location_id IS NOT NULL """

        location_id = self.env.context.get('location_id')
        product_sku_code = self.env.context.get('product_sku')

        AND = " AND "

        if not location_id is None:
            sql_query = sql_query + AND + " sq.location_id = " + str(location_id)

        if not product_sku_code is None:
            sql_query = sql_query + AND + " t.sku_code = '" + str(product_sku_code) + "'"

        if start_date and end_date:
            sql_query = sql_query + AND + " l.use_date >='" + str(start_date) + "'" + AND + " l.use_date <='" + str(end_date)+"'"

        sql_query = sql_query + " )"

        self._cr.execute(sql_query)

    @api.model_cr
    def delete_and_create(self):
        self.init_table()

    cart_qty = fields.Integer(compute='_compute_cart_qty')

    @api.multi
    @api.depends('status')
    def _set_date_fg_color(self):
        for product_lot in self:
            if product_lot.status == "Expired":
                product_lot.color_value = 1
            elif product_lot.status == "Expiring":
                product_lot.color_value = 2
            elif product_lot.status == "Valid":
                product_lot.color_value = 3

