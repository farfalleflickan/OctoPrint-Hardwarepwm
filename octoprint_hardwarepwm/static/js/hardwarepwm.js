/*
 * View model for OctoPrint-Hardwarepwm
 *
 * Author: Daria Rostirolla
 * License: AGPLv3
 */
$(function() {
    function HardwarepwmViewModel(parameters) {
        this.settings = parameters[0];
        this.perc0 = ko.observable();
        this.perc1 = ko.observable();
        this.perc2 = ko.observable();
        this.perc3 = ko.observable();

        this.onBeforeBinding = function() {
            this.perc0(this.settings.settings.plugins.hardwarepwm.duties()[0]);
            this.perc1(this.settings.settings.plugins.hardwarepwm.duties()[1]);
            this.perc2(this.settings.settings.plugins.hardwarepwm.duties()[2]);
            this.perc3(this.settings.settings.plugins.hardwarepwm.duties()[3]);
        }

        this.handlePWM = function (item) {
            var pwmVal0 = parseInt(item.perc0());
            var pwmVal1 = parseInt(item.perc1());
            var pwmVal2 = parseInt(item.perc2());
            var pwmVal3 = parseInt(item.perc3());
            if (pwmVal0 < 0 || pwmVal0 > 100 || isNaN(pwmVal0) || pwmVal1 < 0 || pwmVal1 > 100 || isNaN(pwmVal1) || pwmVal2 < 0 || pwmVal2 > 100 || isNaN(pwmVal2) || pwmVal3 < 0 || pwmVal3 > 100 || isNaN(pwmVal3)) {
                new PNotify({
                    title: "hardwarePWM",
                    text: "Duty cycle value needs to be between 0 and 100!",
                    type: "error"
                });
            } else {
                $.ajax({
                    type: "POST",
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    data: JSON.stringify({"val0":pwmVal0, "val1":pwmVal1, "val2":pwmVal2, "val3":pwmVal3}),
                    url: window.PLUGIN_BASEURL + "hardwarepwm/setPWM"
                });
            }
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: HardwarepwmViewModel,
        dependencies: [ "settingsViewModel" ],
        elements: [ "#tab_plugin_hardwarepwm" ]
    });
});
