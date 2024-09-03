# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class StockRevaluation(models.Model):
    _name = "stock_revaluation"
    _description = "Stock Revaluation"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.many2one_configurator",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_terminate",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    type_id = fields.Many2one(
        comodel_name="stock_revaluation_type",
        string="Type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    allowed_picking_type_ids = fields.Many2many(
        comodel_name="stock.picking.type",
        string="Allowed Picking Types",
        compute="_compute_allowed_picking_type_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_picking_type_category_ids = fields.Many2many(
        comodel_name="picking_type_category",
        string="Allowed Picking Type Categories",
        compute="_compute_allowed_picking_type_category_ids",
        store=False,
        compute_sudo=True,
    )
    picking_id = fields.Many2one(
        related=False,
        string="# Picking",
        comodel_name="stock.picking",
        required=False,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    stock_move_id = fields.Many2one(
        comodel_name="stock.move",
        string="Stock Move",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    stock_valuation_layer_id = fields.Many2one(
        string="SVL",
        comodel_name="stock.valuation.layer",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    stock_valuation_layer_ids = fields.Many2many(
        string="Stock Valuation Layers",
        comodel_name="stock.valuation.layer",
        relation="rel_stock_revaluation_2_svl",
        column1="stock_revaluation_id",
        column2="stock_valuation_layer_id",
        readonly=True,
    )
    allowed_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Allowed Products",
        compute="_compute_allowed_product_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_product_category_ids = fields.Many2many(
        comodel_name="product.category",
        string="Allowed Product Category",
        compute="_compute_allowed_product_category_ids",
        store=False,
        compute_sudo=True,
    )

    old_price_unit = fields.Float(
        string="Old Price Unit",
        required=True,
        readonly=True,
    )
    quantity = fields.Float(
        string="Old Quantity",
        required=True,
        readonly=True,
    )
    old_value = fields.Float(
        string="Old Value",
        required=True,
        readonly=True,
    )
    new_price_unit = fields.Float(
        string="New Price Unit",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    new_value = fields.Float(
        string="New Value",
        compute="_compute_new_value",
        store=True,
    )

    @api.depends(
        "quantity",
        "new_price_unit",
    )
    def _compute_new_value(self):
        for record in self:
            record.new_value = record.new_price_unit * record.quantity

    @api.depends("type_id")
    def _compute_allowed_product_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.product",
                    method_selection=record.type_id.product_selection_method,
                    manual_recordset=record.type_id.product_ids,
                    domain=record.type_id.product_domain,
                    python_code=record.type_id.product_python_code,
                )
            record.allowed_product_ids = result

    @api.depends("type_id")
    def _compute_allowed_product_category_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.category",
                    method_selection=record.type_id.product_category_selection_method,
                    manual_recordset=record.type_id.product_category_ids,
                    domain=record.type_id.product_category_domain,
                    python_code=record.type_id.product_category_python_code,
                )
            record.allowed_product_category_ids = result

    @api.depends("type_id")
    def _compute_allowed_picking_type_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="stock.picking.type",
                    method_selection=record.type_id.picking_type_selection_method,
                    manual_recordset=record.type_id.picking_type_ids,
                    domain=record.type_id.picking_type_domain,
                    python_code=record.type_id.picking_type_python_code,
                )
            record.allowed_picking_type_ids = result

    @api.depends("type_id")
    def _compute_allowed_picking_type_category_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="picking_type_category",
                    method_selection=record.type_id.picking_type_category_selection_method,
                    manual_recordset=record.type_id.picking_type_category_ids,
                    domain=record.type_id.picking_type_category_domain,
                    python_code=record.type_id.picking_type_category_python_code,
                )
            record.allowed_picking_type_category_ids = result

    @api.onchange(
        "type_id",
    )
    def onchange_product_id(self):
        self.product_id = False

    @api.onchange(
        "product_id",
    )
    def onchange_picking_id(self):
        self.picking_id = False

    @api.onchange(
        "picking_id",
    )
    def onchange_stock_move_id(self):
        self.stock_move_id = False

    @api.onchange(
        "stock_move_id",
    )
    def onchange_stock_valuation_layer_id(self):
        self.stock_valuation_layer_id = False

    @api.onchange(
        "stock_valuation_layer_id",
    )
    def onchange_old_price_unit(self):
        self.old_price_unit = 0.0
        if self.stock_valuation_layer_id:
            self.old_price_unit = self.stock_valuation_layer_id.unit_cost

    @api.onchange(
        "stock_valuation_layer_id",
    )
    def onchange_quantity(self):
        self.quantity = 0.0
        if self.stock_valuation_layer_id:
            self.quantity = self.stock_valuation_layer_id.quantity

    @api.onchange(
        "stock_valuation_layer_id",
    )
    def onchange_old_value(self):
        self.old_value = 0.0
        if self.stock_valuation_layer_id:
            self.old_value = self.stock_valuation_layer_id.value

    @api.constrains(
        "state",
    )
    def constrains_check_journal_entry(self):
        for record in self.sudo():
            record._check_journal_entry()

    def action_reload_svl(self):
        for record in self.sudo():
            record._reload_svl()

    def action_open_svl(self):
        for record in self.sudo():
            result = record._open_svl()
        return result

    def _open_svl(self):
        waction = self.env.ref("stock_account.stock_valuation_layer_action").read()[0]
        waction.update(
            {
                "view_mode": "tree,form",
                "domain": [("id", "in", self.stock_valuation_layer_ids.ids)],
                "context": {},
            }
        )
        return waction

    def _check_journal_entry(self):
        self.ensure_one()
        if self.state in ["confirm", "done", "reject"]:
            if self.stock_valuation_layer_id.debit_move_line_id:
                error_message = _(
                    """
                Context: State change into Waiting for Approval, Reject, Done, or Cancel
                Database ID: %s
                Problem: SVL with ID %s has journal entry
                Solution: Delete SVL's journal entry
                """
                    % (self.id, self.stock_valuation_layer_id.id)
                )
                raise UserError(error_message)
            for incoming_svl in self.stock_valuation_layer_ids:
                if incoming_svl.debit_move_line_id:
                    error_message = _(
                        """
                    Context: State change into Waiting for Approval, Reject, Done, or Cancel
                    Database ID: %s
                    Problem: Incoming SVL with ID %s has journal entry
                    Solution: Delete SVL's journal entry
                    """
                        % (self.id, incoming_svl.id)
                    )
                    raise UserError(error_message)

    def _reload_svl(self):
        self.ensure_one()
        SVLUsage = self.env["stock_valuation_layer_usage"]
        criteria = [("stock_valuation_layer_id", "=", self.stock_valuation_layer_id.id)]
        usages = SVLUsage.search(criteria).mapped("dest_stock_valuation_layer_id")
        self.write({"stock_valuation_layer_ids": [(6, 0, usages.ids)]})

    @ssi_decorator.post_done_action()
    def _01_change_svl_value(self):
        self.ensure_one()
        data = self._prepare_svl_value()
        self.stock_valuation_layer_id.write(data)

    @ssi_decorator.post_done_action()
    def _02_change_incoming_svl_value(self):
        self.ensure_one()
        for incoming_svl_usage in self.stock_valuation_layer_id.usage_ids:
            incoming_svl_usage.write(
                self._prepare_incoming_svl_usage(incoming_svl_usage)
            )
            incoming_svl_usage.dest_stock_valuation_layer_id.write(
                self._prepare_incoming_svl(
                    incoming_svl_usage.dest_stock_valuation_layer_id
                )
            )

    @ssi_decorator.post_cancel_action()
    def _01_change_cancel_svl_value(self):
        self.ensure_one()
        data = self._prepare_cancel_svl_value()
        self.stock_valuation_layer_id.write(data)

    @ssi_decorator.post_cancel_action()
    def _02_change_cancel_incoming_svl_value(self):
        self.ensure_one()
        for incoming_svl_usage in self.stock_valuation_layer_id.usage_ids:
            incoming_svl_usage.write(
                self._prepare_cancel_incoming_svl_usage(incoming_svl_usage)
            )
            incoming_svl_usage.dest_stock_valuation_layer_id.write(
                self._prepare_cancel_incoming_svl(
                    incoming_svl_usage.dest_stock_valuation_layer_id
                )
            )

    def _prepare_cancel_svl_value(self):
        self.ensure_one()
        return {
            "unit_cost": self.old_price_unit,
            "value": self.stock_valuation_layer_id.quantity * self.old_price_unit,
        }

    def _prepare_svl_value(self):
        self.ensure_one()
        return {
            "unit_cost": self.new_price_unit,
            "value": self.stock_valuation_layer_id.quantity * self.new_price_unit,
        }

    def _prepare_incoming_svl_usage(self, incoming_svl_usage):
        self.ensure_one()
        return {
            "value": incoming_svl_usage.quantity * self.new_price_unit,
        }

    def _prepare_incoming_svl(self, incoming_svl):
        self.ensure_one()
        return {
            "unit_cost": incoming_svl.incoming_usage_value / abs(incoming_svl.quantity),
            "value": -1.0 * incoming_svl.incoming_usage_value,
        }

    def _prepare_cancel_incoming_svl_usage(self, incoming_svl_usage):
        self.ensure_one()
        return {
            "value": incoming_svl_usage.quantity * self.old_price_unit,
        }

    def _prepare_cancel_incoming_svl(self, incoming_svl):
        self.ensure_one()
        return {
            "unit_cost": incoming_svl.incoming_usage_value / abs(incoming_svl.quantity),
            "value": -1.0 * incoming_svl.incoming_usage_value,
        }

    @api.model
    def _get_policy_field(self):
        res = super(StockRevaluation, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "cancel_ok",
            "done_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
