/** @odoo-module **/

import session from 'web.session';
import { patch } from "@web/core/utils/patch";
import { NavBar } from "@web/webclient/navbar/navbar";


patch(NavBar.prototype, "database_block/static/src/alert/main.Navbar.js", {
    databaseAlert() {
        const message = {};
        if (session.database_block_show_message_in_apps_menu) {
            if (session.database_block_is_warning === true) {
                if (session.database_expiration_message) {
                    const result = {
                        type: "warning",
                        message: session.database_expiration_message,
                    }
                    return result;
                }
                if (session.database_block_message) {
                    const result = {
                        type: "warning",
                        message: session.database_block_message,
                    }
                    return result;
                }
            }
        }
        return message;
    }
 });

