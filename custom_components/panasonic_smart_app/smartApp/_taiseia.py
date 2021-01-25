""" TaiSEIA 101 """
from homeassistant.components.humidifier.const import (
    MODE_NORMAL, MODE_ECO, MODE_AWAY, MODE_BOOST, MODE_COMFORT, MODE_HOME, MODE_SLEEP, MODE_AUTO, MODE_BABY,
    SUPPORT_MODES
)

COMMANDS_NAME = {
    "0x00": "電源",
    "0x01": "功能選擇",
    "0x02": "時間到關",
    "0x03": "target_temperature",
    "0x04": "濕度設定",
    "0x09": "風向設定",
    "0x0D": "nanoe(清淨、脫臭)",
    "0x0E": "風量設定",
    "0x55": "時間到開",
    "0x18": "操作提示音"
   
}

COMMANDS_OPTIONS = {
    "0x00": {
        "0": "Off",
        "1": "On"
    },
    "0x01": {
        "0": "連續除濕",
        "1": "自動除濕",
        "2": "防霉抑菌",
        "3": "HVAC_MODE_HEAT_COOL",
        "4": "衣物乾燥",
        "5": "保持乾燥",
        "6": "濕度設定",
        "7": "空氣清淨"
        #: [['連續除濕', 0], ['自動除濕', 1], ['防霉抑菌', 2], ['空氣清淨', 7], ['衣物乾燥', 4], ['保持乾燥', 5], ['濕度設定', 6]]},
    },
    "0x0E": {
        "0": "自動",
        "1": "急速",
        "2": "標準",
        "3": "靜音",

        #[['自動', 0], ['急速', 1], ['標準', 2], ['靜音', 3]]}
    }
}