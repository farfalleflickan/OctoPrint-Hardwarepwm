from __future__ import absolute_import
import octoprint.plugin
import pigpio
import flask

class HardwarepwmPlugin(octoprint.plugin.SettingsPlugin,
                        octoprint.plugin.AssetPlugin,
                        octoprint.plugin.StartupPlugin,
                        octoprint.plugin.ShutdownPlugin,
                        octoprint.plugin.BlueprintPlugin,
                        octoprint.plugin.TemplatePlugin):

    def __init__(self):
        self.pins=[12, 13, 18, 19]
        self.freqs=[0, 0, 0, 0]
        self.duties=[0, 0, 0, 0]
        self.GPIO = pigpio.pi()

    def startALL(self):
        for i in range(len(self.pins)):
            self.startPWM(self.pins[i], self.freqs[i], self.duties[i])

    def stopALL(self):
        for i in range(len(self.pins)):
            self.stopPWM(self.pins[i])

    def startPWM(self, pin, hz, percCycle):
        cycle=int(percCycle*10000)
        self._logger.info("startPWM: "+str(pin)+" "+str(hz)+" "+str(percCycle))
        if (self.GPIO.connected):
            if (pin==18 or pin==19):
                self.GPIO.set_mode(pin, pigpio.ALT5)
                self.GPIO.hardware_PWM(pin, hz, cycle)
            elif (pin==12 or pin==13):
                self.GPIO.set_mode(pin, pigpio.ALT0)
                self.GPIO.hardware_PWM(pin, hz, cycle)
            else:
                self._logger.error(str(pin)+" is not a hardware PWM pin.")
        else:
            self._logger.error("Not connected to PIGPIO")

    def stopPWM(self, pin):
        if (self.GPIO.connected):
            self.GPIO.write(pin, 0)
        else:
            self._logger.error("Not connected to PIGPIO")

    def shutOffPWM(self):
        self.GPIO.stop()

    def get_settings_defaults(self):
        return dict(pins=[12, 13, 18, 19],freqs=[0, 0, 0, 0],duties=[0, 0, 0, 0])

    def on_after_startup(self):
        self.getVars()
        self._logger.info("Loading config pins, freqs & duties: "+str(self.pins)+" "+str(self.freqs)+" "+str(self.duties))
        self.startALL()

    def on_shutdown(self):
        self.stopALL()
        self.shutOffPWM()

    def getVars(self):
        self.pins[0] = int(self._settings.get(["pins"])[0])
        self.pins[1] = int(self._settings.get(["pins"])[1])
        self.pins[2] = int(self._settings.get(["pins"])[2])
        self.pins[3] = int(self._settings.get(["pins"])[3])
        self.freqs[0] = int(self._settings.get(["freqs"])[0])
        self.freqs[1] = int(self._settings.get(["freqs"])[1])
        self.freqs[2] = int(self._settings.get(["freqs"])[2])
        self.freqs[3] = int(self._settings.get(["freqs"])[3])
        self.duties[0] = int(self._settings.get(["duties"])[0])
        self.duties[1] = int(self._settings.get(["duties"])[1])
        self.duties[2] = int(self._settings.get(["duties"])[2])
        self.duties[3] = int(self._settings.get(["duties"])[3])
        self._logger.info("getVars: "+str(self.pins)+" "+str(self.freqs)+" "+str(self.duties))

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.stopALL()
        self._logger.info("Saving config")
        self.getVars()
        self.startALL()

    def get_assets(self):
        return dict(js=["js/hardwarepwm.js"])

    def get_template_vars(self):
        return dict(pins=self._settings.get(["pins"]), freqs=self._settings.get(["freqs"]), duties=self._settings.get(["duties"]))

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    def get_update_information(self):
        return dict(
            hardwarepwm=dict(
                displayName="Hardwarepwm Plugin",
                displayVersion=self._plugin_version,
                type="github_release",
                user="farfalleflickan",
                repo="OctoPrint-Hardwarepwm",
                current=self._plugin_version,
                pip="https://github.com/farfalleflickan/OctoPrint-Hardwarepwm/archive/{target_version}.zip"
            )
        )

    @octoprint.plugin.BlueprintPlugin.route("/setPWM", methods=["POST"])
    def set_pwm(self):
        duty0=int(flask.request.json['val0'])
        duty1=int(flask.request.json['val1'])
        duty2=int(flask.request.json['val2'])
        duty3=int(flask.request.json['val3'])
        self.duties[0]=duty0
        self.duties[1]=duty1
        self.duties[2]=duty2
        self.duties[3]=duty3
        self._logger.info("/setPWM args: "+str(duty0)+" "+str(duty1)+" "+str(duty2)+" "+str(duty3))
        self._settings.set(["duties"], self.duties)
        self._settings.save(True, True)
        self.stopALL()
        self.getVars()
        self.startALL()
        return flask.jsonify(success=True)

__plugin_name__ = "hardwarePWM"
__plugin_pythoncompat__ = ">=3,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = HardwarepwmPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
            "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
