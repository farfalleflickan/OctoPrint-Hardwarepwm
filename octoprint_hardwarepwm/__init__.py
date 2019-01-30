from __future__ import absolute_import
import octoprint.plugin
import pigpio
import flask

class HardwarepwmPlugin(octoprint.plugin.SettingsPlugin,
                        octoprint.plugin.AssetPlugin,
                        octoprint.plugin.StartupPlugin,
			octoprint.plugin.ShutdownPlugin,
<<<<<<< HEAD
			octoprint.plugin.BlueprintPlugin,
=======
>>>>>>> 8c65d7e05c537c992a8d6d64b468e27b3bc48712
                        octoprint.plugin.TemplatePlugin):

    def __init__(self):
	self.IOpin = 19
	self.Freq = 512
	self.dutyCycle = 50
        self.GPIO = pigpio.pi()

    def startPWM(self, pin, hz, percCycle):
<<<<<<< HEAD
        cycle=float(percCycle*10000)
        if (self.GPIO.connected):
	    if (pin==12 or pin==13 or pin==18 or pin==19):
	        self.GPIO.set_mode(pin, pigpio.ALT5)
        	self.GPIO.hardware_PWM(pin, hz, cycle)
	    else:
	        self._logger.error(str(pin)+" is not a hardware PWM pin.")
	else:
            self._logger.error("Not connected to PIGPIO")
=======
        cycle=float(percCycle/100)*1000000
        if (self.GPIO.connected):
		if (self.IOpin==12 or self.IOpin==13 or self.IOpin==18 or self.IOpin==19):
			self.GPIO.set_mode(self.IOpin, pigpio.ALT5)
        		self.GPIO.hardware_PWM(self.IOpin, hz, cycle)
		else:
			self._logger.error(str(self.IOpin)+" is not a hardware PWM pin.")
	else:
		self._logger.error("Not connected to PIGPIO")
>>>>>>> 8c65d7e05c537c992a8d6d64b468e27b3bc48712

    def stopPWM(self, pin):
        if (self.GPIO.connected):
                self.GPIO.write(pin, 0)
        else:
                self._logger.error("Not connected to PIGPIO")

    def shutOffPWM(self):
        self.GPIO.stop()

    def get_settings_defaults(self):
	return dict(
	    IOpin=self.IOpin,
	    Freq=self.Freq,
	    dutyCycle=self.dutyCycle
	)

    def on_after_startup(self):
<<<<<<< HEAD
        self.getVars()
=======
        self.IOpin = float(self._settings.get(["IOpin"]))
        self.Freq = float(self._settings.get(["Freq"]))
        self.dutyCycle = float(self._settings.get(["dutyCycle"]))
>>>>>>> 8c65d7e05c537c992a8d6d64b468e27b3bc48712
        self.startPWM(self.IOpin, self.Freq, self.dutyCycle)

    def on_shutdown(self):
        self.stopPWM(self.IOpin);
        self.shutOffPWM();

<<<<<<< HEAD
    def getVars(self):
        self.IOpin = float(self._settings.get(["IOpin"]))
        self.Freq = float(self._settings.get(["Freq"]))
        self.dutyCycle = float(self._settings.get(["dutyCycle"]))

    def on_settings_save(self, data):
	octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
	self.stopPWM(self.IOpin)
        self.getVars()
=======
    def on_settings_save(self, data):
	octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
	self.stopPWM(self.IOpin)
	self.IOpin = float(self._settings.get(["IOpin"]))
        self.Freq = float(self._settings.get(["Freq"]))
        self.dutyCycle = float(self._settings.get(["dutyCycle"]))
>>>>>>> 8c65d7e05c537c992a8d6d64b468e27b3bc48712
        self.startPWM(self.IOpin, self.Freq, self.dutyCycle)

    def get_assets(self):
	return dict(
	    js=["js/hardwarepwm.js"],
	    css=["css/hardwarepwm.css"],
	    less=["less/hardwarepwm.less"]
	    )

    def get_template_vars(self):
        return dict(
<<<<<<< HEAD
	    IOpin = float(self._settings.get(["IOpin"])),
	    Freq = float(self._settings.get(["Freq"])),
            dutyCycle = float(self._settings.get(["dutyCycle"]))
	)

    def get_template_configs(self):
        return [
=======
			IOpin = float(self._settings.get(["IOpin"])),
			Freq = float(self._settings.get(["Freq"])),
                        dutyCycle = float(self._settings.get(["dutyCycle"]))
	    )

    def get_template_configs(self):
        return [
	    dict(type="tab", custom_bindings=True),
>>>>>>> 8c65d7e05c537c992a8d6d64b468e27b3bc48712
	    dict(type="settings", custom_bindings=False)
	]


    def get_update_information(self):
	return dict(
	    hardwarepwm=dict(
	        displayName="Hardwarepwm Plugin",
		displayVersion=self._plugin_version,
		type="github_release",
		user="pastapojken",
		repo="OctoPrint-Hardwarepwm",
		current=self._plugin_version,
		pip="https://github.com/you/OctoPrint-Hardwarepwm/archive/{target_version}.zip"
	    )
        )

    @octoprint.plugin.BlueprintPlugin.route("/setPWM", methods=["POST"])
    def set_pwm(self):
        new_cycle = float(flask.request.json['val'])
	self.dutyCycle=new_cycle
        self._settings.set(["dutyCycle"], new_cycle)
	self._settings.save()
        self.getVars()
        self.startPWM(self.IOpin, self.Freq, self.dutyCycle)
        return flask.jsonify(success=True)



__plugin_name__ = "hardwarePWM"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = HardwarepwmPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

