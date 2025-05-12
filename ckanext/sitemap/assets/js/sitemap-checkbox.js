ckan.module("sitemap-checkbox", function ($, _) {
  "use strict";
  return {
    options: {
      debug: false,
    },

    initialize: function () {
      if (this.options.debug) {
        console.log("sitemap-checkbox module initialized");
      }

      if (this.el.val() == "true") {
        this.el.prop("checked", true);
      } else {
        this.el.prop("checked", false);
      }

      // Bind the change event to the checkbox
      this.el.on("change", function (e) {
        if ($(this).is(":checked")) {
          $(this).val("true");
        } else {
          $(this).val("false");
        }
      });
    },
  };
});
