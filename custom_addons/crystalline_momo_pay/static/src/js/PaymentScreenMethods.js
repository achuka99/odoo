/**@odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { MomoPopup } from "@crystalline_momo_pay/js/PopUp/momo_pop_up";
import { patch } from "@web/core/utils/patch";

// Define the sendRequest method
async function sendRequest(amountToPay) {
    // Prepare the request payload
    const payload = {
        "amount": "12000",
        "currency": "EUR",
        "reference": "ER-POS-0005",
        "phone_number": "46733123450",
        "payer_message": "Payment for invoice ER-POS-0005"
       };

    // Send the request to your backend
    const response = await fetch('/payment/momo/initiate', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json; charset=UTF-8"
        },
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        const data = await response.json();
        console.log(data);
        console.log('message also goes')
        // Handle the response, e.g., show a success message or redirect to a payment confirmation page
    } else {
        console.error('Payment initiation failed');
        // Handle errors, e.g., show an error message
    }
}


// Patch the PaymentScreen component to add a custom alert popup
patch(PaymentScreen.prototype, {
    async onClick() {
        // Access the current order's total amount
        const order = this.pos.get_order();
        const totalAmount = order.get_total_with_tax();
        console.log(order)

        // Show the custom alert popup instead of the default behavior
        this.popup.add(MomoPopup, {
            title: _t('Please enter MTN details'),
            amountToPay: totalAmount.toFixed(2), // Pass the total amount to the popup
            sendRequest: sendRequest.bind(this), // Pass the sendRequest method
        });
    }
});


