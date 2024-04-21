/**@odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class CustomButton extends Component {
    static template = "point_of_sale.CustomButton";

    setup() {
        this.pos = usePos();
    }

    async onClick() {
        // Implement your custom button logic here
        console.log(_t('Custom Button clicked'));
    }
}

ProductScreen.addControlButton({
    component: CustomButton,
});
