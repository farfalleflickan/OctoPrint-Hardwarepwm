# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import pigpio

class HardwarepwmPlugin(octoprint.plugin.SettingsPlugin,
                        octoprint.plugin.AssetPlugin,
                        octoprint.plugin.StartupPlugin,
                        octoprint.plugin.TemplatePlugin):

    def __init__(self):
	self.IOpin = 19
	self.Freq = 512
	self.dutyCycle = 50
        self.GPIO = pigpio.pi()

    def startPWM(self, pin, hz, percCycle):
        cycle=float(percCycle/100)*1000000
        if (self.GPIO.connected):
		self.GPIO.set_mode(pin, pigpio.ALT5)
        	self.GPIO.hardware_PWM(pin, hz, cycle)
	else:
		self._logger.info("Not connected to PIGPIO")

    def stopPWM(self, pin):
        if (self.GPIO.connected):
                self.GPIO.write(pin, 0)
        else:
                self._logger.info("Not connected to PIGPIO")

    def shutOffPWM(self):
        self.GPIO.stop()

    ##~~ SettingsPlugin mixin
    def get_settings_defaults(self):
	return dict(
		IOpin=self.IOpin,
		Freq=self.Freq,
		dutyCycle=self.dutyCycle
		)

    def on_after_startup(self):
        self.IOpin = float(self._settings.get(["IOpin"]))
        self.Freq = float(self._settings.get(["Freq"]))
        self.dutyCycle = float(self._settings.get(["dutyCycle"]))
        self.startPWM(self.IOpin, self.Freq, self.dutyCycle)

    def on_settings_save(self, data):
	octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
	self.stopPWM(self.IOpin)
	self.IOpin = float(self._settings.get(["IOpin"]))
        self.Freq = float(self._settings.get(["Freq"]))
        self.dutyCycle = float(self._settings.get(["dutyCycle"]))
        self.startPWM(self.IOpin, self.Freq, self.dutyCycle)

    ##~~ AssetPlugin mixin
    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
	# core UI here.
	return dict(
	    js=["js/hardwarepwm.js"],
	    css=["css/hardwarepwm.css"],
	    less=["less/hardwarepwm.less"]
	    )

    def get_template_vars(self):
        return dict(
			IOpin = float(self._settings.get(["IOpin"])),
			Freq = float(self._settings.get(["Freq"])),
                        dutyCycle = float(self._settings.get(["dutyCycle"]))
	    )

    def get_template_configs(self):
        return [
	    dict(type="tab", custom_bindings=False),
	    dict(type="settings", custom_bindings=False)
	    ]


    ##~~ Softwareupdate hook
    def get_update_information(self):
	# Define the configuration for your plugin to use with the Software Update
	# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
	# for details.
	return dict(
	    hardwarepwm=dict(
	        displayName="Hardwarepwm Plugin",
		displayVersion=self._plugin_version,
                # version check: github repository
		type="github_release",
		user="pastapojken",
		repo="OctoPrint-Hardwarepwm",
		current=self._plugin_version,
                # update method: pip
		pip="https://github.com/you/OctoPrint-Hardwarepwm/archive/{target_version}.zip"
		)
            )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "hardwarePWM"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = HardwarepwmPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

