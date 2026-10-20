/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {FormLabel} from "@web/views/form/form_label";
import {fieldVisualFeedback} from "@web/views/fields/field";

patch(FormLabel.prototype, {
    get className() {
        const {
            readonly,
            required,
            invalid,
            empty,
        } = fieldVisualFeedback(
            this.props.fieldInfo.field,
            this.props.record,
            this.props.fieldName,
            this.props.fieldInfo
        );
        const classes = this.props.className ? [this.props.className] : [];
        if (invalid) {
            classes.push("o_field_invalid");
        }
        if (empty) {
            classes.push("o_form_label_empty");
        }
        if (readonly && !this.props.notMuttedLabel) {
            classes.push("o_form_label_readonly");
        }

        if (required) {
            classes.push("o_field_invalid");
        }
        return classes.join(" ");
    }
})
