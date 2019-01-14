from odoo import api, fields, models, tools


class PickTicketReport(models.Model):
    _name = "report.pick.ticket"
    _auto = False

    _inherits = {'stock.picking': 'picking_id'}

    carrier_info = fields.Char(string="Sale Order#")
    move_id = fields.Many2one('stock.move', string="Customer Name")
    qty_done = fields.Char(string="Quantity")
    location_id = fields.Many2one('stock.location', string="Location")
    location_dest_id = fields.Many2one('stock.location', string='Destionation', )
    state = fields.Char(string='state', )
    sale_id = fields.Many2one('sale.order', string="Sale Order Id")
    partner_id = fields.Many2one('res.partner', string="Partner Id")
    carrier_id = fields.Many2one('delivery.carrier', string="Carrier Id")
    product_id = fields.Many2one('product.product', string="Carrier Id")

    picking_id = fields.Many2one('stock.picking', string='Pick Number')
    product_uom_id = fields.Many2one('product.uom', 'UOM ')
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse')
    scheduled_date = fields.Date(stirng='Scheduled Date')

    picking_type = fields.Char(string='Type', )

    @api.model_cr
    def init(self):
        self.init_table()

    def init_table(self):
        tools.drop_view_if_exists(self._cr, self._name.replace(".", "_"))

        select_query = """ 
            SELECT
                CASE
                    WHEN res_partner.carrier_info IS NOT NULL
                    THEN res_partner.carrier_info
                    ELSE delivery_carrier.name
                END AS carrier_info,
                public.stock_move_line.move_id,
                public.stock_move_line.qty_done,
                public.stock_move_line.location_id,
                public.stock_move_line.location_dest_id,
                public.stock_move_line.state,
                public.sale_order.id      AS sale_id,
                public.stock_move_line.id AS id,
                public.sale_order.partner_id,
                public.sale_order.carrier_id,
                public.stock_move_line.product_id,
                public.stock_move_line.picking_id,
                public.stock_move_line.product_uom_id,
                public.sale_order.warehouse_id,
                public.stock_picking.scheduled_date,
                public.stock_picking_type.name as picking_type
            FROM
                public.stock_move_line
            INNER JOIN
                public.stock_picking
            ON
                (
                    public.stock_move_line.picking_id = public.stock_picking.id)
            INNER JOIN
                public.sale_order
            ON
                (
                    public.stock_picking.sale_id = public.sale_order.id)
            INNER JOIN
                public.res_partner
            ON
                (
                    public.sale_order.partner_id = public.res_partner.id)
            LEFT OUTER JOIN
                public.delivery_carrier
            ON
                (
                    public.sale_order.carrier_id = public.delivery_carrier.id)
            INNER JOIN
                public.product_product
            ON
                (
                    public.stock_move_line.product_id = public.product_product.id)
            INNER JOIN
                public.stock_picking_type
            ON
                (
                    public.stock_picking.picking_type_id = public.stock_picking_type.id)
                            """

        where_clause = "  WHERE  stock_picking.scheduled_date IS NOT NULL "

        sql_query = "CREATE VIEW " + self._name.replace(".", "_") + " AS ( " + select_query + where_clause + " )"
        self._cr.execute(sql_query)

    @api.model_cr
    def delete_and_create(self):
        self.init_table()
