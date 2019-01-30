/*
 * View model for OctoPrint-Hardwarepwm
 *
 * Author: Dario Rostirolla
 * License: AGPLv3
 */
$(function() {
    function HardwarepwmViewModel(parameters) {
        var self = this;
	self.settings = parameters[0];
        self.perc = ko.observable();

	self.onBeforeBinding = function() {
            self.perc(self.settings.settings.plugins.hardwarepwm.dutyCycle());
        }

	self.handlePWM = function (item) {
		var pwmVal = item.perc();
		if (pwmVal < 0 || pwmVal > 100 || isNaN(pwmVal)) {
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
				data: JSON.stringify({"val":pwmVal}),
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
