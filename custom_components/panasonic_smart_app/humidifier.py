from pprint import pprint
import logging
import voluptuous as vol
from typing import Any, Dict, Optional, List
from datetime import timedelta
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_connect, async_dispatcher_send
from homeassistant.helpers import service
from homeassistant.core import callback
from .smartApp import SmartApp

from homeassistant.components.humidifier import PLATFORM_SCHEMA, HumidifierEntity

from homeassistant.const import (
    TEMP_CELSIUS, ATTR_TEMPERATURE,
    CONF_USERNAME, CONF_PASSWORD
)

from homeassistant.components.humidifier.const import (
    ATTR_AVAILABLE_MODES,
    ATTR_HUMIDITY,
    ATTR_MAX_HUMIDITY,
    ATTR_MIN_HUMIDITY,
    ATTR_MODE,
    DEFAULT_MAX_HUMIDITY,
    DEFAULT_MIN_HUMIDITY,
    DEVICE_CLASS_DEHUMIDIFIER,
	SERVICE_SET_HUMIDITY,
    SERVICE_SET_MODE,
    SUPPORT_MODES
)

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'panasonic_smart_app2'
ATTR_ENTITY_ID = "entity_id"





SCAN_INTERVAL = timedelta(seconds=30)
ATTR_MODE = "mode"
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})
#States Attributes
ATTR_ION_SET_SWITCH = "ion"
ATTR_FAN_SPEED_MODE = "fan_speed_mode"
ATTR_CURRRENT_HUMIDITY = "current_humidity"
ATTR_TANK = "tank_show"
ATTR_FAN_SPEED = "fan_speed"

ATTR_FAN_MODE="fan_mode"
ATTR_FAN_MODES="avaiable_fan_modes"

PROP_TO_ATTR = {
#    "ionSetSwitch": ATTR_ION_SET_SWITCH,
	"fan_mode": ATTR_FAN_MODE,
    "fan_modes": ATTR_FAN_MODES,
#    "windSpeedMode": ATTR_FAN_SPEED_MODE,
#    "windSpeed": ATTR_FAN_SPEED,
#	"current_humidity": ATTR_CURRRENT_HUMIDITY,
#        "tank_show": ATTR_TANK,
}
#PRESET_LIST = {
#    # PRESET_NONE: 'Auto',
#    # PRESET_BOOST: 'Powerful',
#    # PRESET_ECO: 'Quiet'
#}
DEHUMI_MODES_LIST =  [
    "0: 連續除濕",
    "1: 自動除濕",
    "2: 防霉抑菌",
    "3: HVAC_MODE_HEAT_COOL",
    "4: 衣物乾燥",
    "5: 保持乾燥",
    "6: 濕度設定",
    "7: 空氣清淨"
]
SUPPORT_FLAGS = SUPPORT_MODES
#SUPPORT_FLAGS = (
#    SUPPORT_MODES
#    # SUPPORT_FAN_MODE |
#    # SUPPORT_PRESET_MODE |
#    # SUPPORT_SWING_MODE
#)

def tryApiStatus(func):
    def wrapper_call(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            args[0]._api.login()
            func(*args, **kwargs)
    return wrapper_call

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the panasonic cloud components."""
    _LOGGER.info('The panasonic_smart_app is setting up Platform.')
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    # _LOGGER.debug(f'The panasonic_smart_app info {username} {password}.')
    api = SmartApp(username, password)
    try:
        api.login()
    except:
        _LOGGER.error('Please Check Your UserName and Password.')
    else:
        devices = []
        for device in api.getDevices().get('GWList'):
            _LOGGER.debug(f'The panasonic_smart_app2 devices {device}.')
            devices.append(PanasonicDevice(device, api))
        add_entities(devices, True)
        _LOGGER.info('The panasonic_smart_app2 setup is done.')

        _LOGGER.info(api.getDevices())

    #service 要執行的內容
    def service_set_fan_speed(call):
    #def async_service_set_fan_speed(call):
        entity_id = call.data[ATTR_ENTITY_ID]
        speed_mode = call.data[ATTR_FAN_SPEED]
        #執行對應信號ENTITY_ID的巨集
        async_dispatcher_send(hass, "set_fan_speed_{}".format(entity_id), speed_mode)

    #註冊一個新的service
    SERVICE_SET_FAN_SPEED_SCHEMA = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.entity_id,
    vol.Required(ATTR_FAN_SPEED): cv.string,
    })
    hass.services.register( "humidifier", "set_fan_speed", service_set_fan_speed, SERVICE_SET_FAN_SPEED_SCHEMA)


class PanasonicDevice(HumidifierEntity):
    def __init__(self, device, api):
        self._api = api
        self._commandList = api._devices['CommandList'][0]['JSON'][0]['list']
        self._device = device
        self._name = device['Devices'][0]['NickName']
        self._auth = device['auth']
        self._supported_features = SUPPORT_FLAGS
        self._available_modes = DEHUMI_MODES_LIST

        self._is_on = False
        self._device_class = DEVICE_CLASS_DEHUMIDIFIER
        self._fan_mode = None
        self._fan_modes = None
        #Default values for device state
 #       self._powerMode = None			# 0:off, 1:on
        self._mode = None			    # device's current mode ['Target_humidity', 'Continuos', 'Smart', 'Dryer']
        #self._ionSetSwitch = None       # 0:off, 1:on
#       self._humidity = None			# current humidity
#       self._humidity_set = None		# target hunidity
#       self._humidity_dot = None		# current humidity (decimal)
#       self._humidity_dot_set = None	# target humidity (decimal)
#       self._windSpeed = None			# fan speed [1..99]
#       self._windSpeedMode = None		# fan speed mode (Silent:40, Medium:60, High:80)
#       self._isDisplay = None
#       self._filterShow = False
#       self._tankShow = False
#       self._dryClothesSetSwitch = None
#       self._upanddownSwing = None
#       self._tankShow = False
        # self._hvac_mode = HVAC_MODE_COOL
        # self._current_fan = 'Auto'
        # self._airswing_hor = 'Auto'
        # self._airswing_vert = 'Auto'
        # self._eco = 'Auto'

        #self._unit = TEMP_CELSIUS
        #self._target_temperature = None
        #self._current_temperature = None
        #self._outside_temperature = None
        # self._mode = None
        # self._eco = 'Auto'
        # self._preset_mode = 'off'



    @tryApiStatus
    def update(self):
        _LOGGER.debug(f"------- UPDATING {self._name} -------")
        """Update the state of this humidifier device."""
        self._status = self._api.getDeviceInfo(self._device['auth'], options=['0x00', '0x01', '0x02', '0x04', '0x09', '0x0D', '0x0E', '0x55', '0x18'])

        _LOGGER.debug(f"Status: {self._status}")
        # _is_on
        self._is_on = bool(int(self._status.get('0x00')))

        _LOGGER.debug(f"_is_on: {self._is_on}")

        _LOGGER.debug(f"[{self._name}] is UPDATED.")

    @property
    def name(self):
        """Return the display name of this humidifier."""
        return self._name
    @property
    def available_modes(self):
        """Return the list of available operation modes."""
        avaiable_modes = list(filter(lambda x: x.get('CommandType') == '0x01', self._commandList))[0].get('Parameters')
        modes_list = []
        for mode in avaiable_modes:
            modes_list.append(self._api.taiSEIA.COMMANDS_OPTIONS.get('0x01').get(str(mode[1])))
        return modes_list

    @property
    def is_on(self):
        """Return true if the device is on."""
        return self._is_on

    @property
    def device_state_attributes(self):
        """Return entity specific state attributes."""
        data = {}

        for prop, attr in PROP_TO_ATTR.items():
            value = getattr(self, prop)
            if value is not None:
                data[attr] = value

        return data

    @property
    def mode(self):
        """Return the current operation."""
        if not self._is_on:
            return "power_off"
        else:
            value = self._status.get('0x01')
            _LOGGER.debug(f"{self._name} mode is {value} - {self._api.taiSEIA.COMMANDS_OPTIONS.get('0x01').get(str(value))}")
            return self._api.taiSEIA.COMMANDS_OPTIONS.get('0x01').get(str(value))

    @property
    def fan_mode(self):
        """Return the device class of the humidifier."""
        if not self._is_on:
            return "power_off"
        else:
            value = self._status.get('0x0E')
            _LOGGER.debug(f"{self._name} fan_mode is {value} - {self._api.taiSEIA.COMMANDS_OPTIONS.get('0x0E').get(str(value))}")
            return self._api.taiSEIA.COMMANDS_OPTIONS.get('0x0E').get(str(value))

    @property
    def fan_modes(self):
        """Return the device class of the humidifier."""
        fan_modes = list(filter(lambda x: x.get('CommandType') == '0x0E', self._commandList))[0].get('Parameters')
        fan_modes_list = []
        for mode in fan_modes:
            fan_modes_list.append(self._api.taiSEIA.COMMANDS_OPTIONS.get('0x0E').get(str(mode[1])))
        return fan_modes_list

    @property
    def device_class(self):
        """Return the device class of the humidifier."""
        return self._device_class

#    @property
#    def temperature_unit(self):
#        """Return the unit of measurement."""
#        return TEMP_CELSIUS
#
#    @property
#    def hvac_mode(self):
#        """Return the current operation."""
#        if not self._is_on:
#            return HVAC_MODE_OFF
#        else:
#            value = self._status.get('0x01')
#            _LOGGER.debug(f"{self._name} hvac_mode is {value} - {self._api.taiSEIA.COMMANDS_OPTIONS.get('0x01').get(str(value))}")
#            return self._api.taiSEIA.COMMANDS_OPTIONS.get('0x01').get(str(value))
#
#    @property
#    def hvac_modes(self):
#        """Return the list of available operation modes."""
#        avaiable_modes = list(filter(lambda x: x.get('CommandType') == '0x01', self._commandList))[0].get('Parameters')
#        modes_list = [HVAC_MODE_OFF]
#        for mode in avaiable_modes:
#            modes_list.append(self._api.taiSEIA.COMMANDS_OPTIONS.get('0x01').get(str(mode[1])))
#        return modes_list
#
    @tryApiStatus
    def turn_on(self):
        self._api.setCommand(self._auth, 0, 1)

    @tryApiStatus
    def turn_off(self):
        self._api.setCommand(self._auth, 0, 0)

    @tryApiStatus
    def set_mode(self,set_mode):
            options = self._api.taiSEIA.COMMANDS_OPTIONS.get('0x01')
            value = list(options.keys())[list(options.values()).index(set_mode)]
            self._api.setCommand(self._auth, 1, value)

#    @tryApiStatus
#    def set_hvac_mode(self, hvac_mode):
#        _LOGGER.debug(f"{self._name} set_hvac_mode: {hvac_mode}")
#        if hvac_mode == HVAC_MODE_OFF:
#            self._api.setCommand(self._auth, 0, 0)
#        else:
#            options = self._api.taiSEIA.COMMANDS_OPTIONS.get('0x01')
#            value = list(options.keys())[list(options.values()).index(hvac_mode)]
#            self._api.setCommand(self._auth, 1, value)
#            if not self._is_on:
#                self._api.setCommand(self._auth, 0, 1)
#
#    @property
#    def preset_mode(self) -> Optional[str]:
#        """Return the current preset mode, e.g., home, away, temp.
#        Requires SUPPORT_PRESET_MODE.
#        """
#        # for key, value in PRESET_LIST.items():
#            # if value == self._eco:
#                # _LOGGER.debug("Preset mode is {0}".format(key))
#                # return key
#
#
#    @property
#    def preset_modes(self) -> Optional[List[str]]:
#        """Return a list of available preset modes.
#        Requires SUPPORT_PRESET_MODE.
#        """
#        # _LOGGER.debug("Preset modes are {0}".format(",".join(PRESET_LIST.keys())))
#        return []
#
#    @property
#    def fan_mode(self):
#        """Return the fan setting."""
#        return 'Auto'
#
#    @property
#    def fan_modes(self):
#        """Return the list of available fan modes."""
#        return []
#
#    # def set_fan_mode(self, fan_mode):
#        # """Set new fan mode."""
#        # _LOGGER.debug("Set %s focus mode %s", self.name, fan_mode)
#
#    @property
#    def swing_mode(self):
#        """Return the fan setting."""
#        return None
#
#    @property
#    def swing_modes(self):
#        """Return the list of available swing modes."""
#        return ['Auto', 'Up', 'UpMid', 'Mid', 'DownMid', 'Down']
#
#    # def set_swing_mode(self, swing_mode):
#    #     """Set swing mode."""
#    #     _LOGGER.debug("Set %s swing mode %s", self.name, swing_mode)
#
    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._supported_features
#
#    @property
#    def target_temperature(self):
#        """Return the target temperature."""
#        return self._target_temperature
#    @property
#    def outside_temperature(self):
#        """Return the current temperature."""
#        return self._outside_temperature
#
#    @property
#    def current_temperature(self):
#        """Return the current temperature."""
#        return self._current_temperature
#
#    @tryApiStatus
#    def set_temperature(self, **kwargs):
#        """Set new target temperature."""
#        target_temp = kwargs.get(ATTR_TEMPERATURE)
#        # if target_temp is None:
#            # return
#        _LOGGER.debug("Set %s temperature %s", self.name, target_temp)
#        self._api.setCommand(self._auth, 3, int(target_temp))
#
#    @property
#    def min_temp(self):
#        """Return the minimum temperature."""
#        return 16
#
#    @property
#    def max_temp(self):
#        """Return the maximum temperature."""
#        return 30
#
#    @property
#    def target_temperature_step(self):
#        """Return the temperature step."""
#        return 1.0

    #將要執行的巨集 連結到服務+entity_id
    async def async_added_to_hass(self):
        """Run when about to be added to hass."""
        async_dispatcher_connect(self.hass, "set_fan_speed_{}".format(self.entity_id), self.service_set_fan_speed_real_action)

    #@callback
    @tryApiStatus
    def service_set_fan_speed_real_action(self, speed_mode):
            options = self._api.taiSEIA.COMMANDS_OPTIONS.get('0x0E')
            value = list(options.keys())[list(options.values()).index(speed_mode)]
            self._api.setCommand(self._auth, 14, value)
