> [!WARNING]
> 當初開啟這個 Project 的時候，是因為找不到任何可以使用的 intergration，因此寫了這個 project 希望能夠拋磚引玉
> Home Assistant 經過多次改版後，部分功能已經 Migrate 到新的參數，目前這個專案還沒有重新寫過
> 我雖然有想重新改版這個 Project 的念頭，畢竟還是有一些程式的結構我認為可以更好
> 但目前的我重心在其他商業專案上，Python 也不是我的主力程式語言，所以一直沒有改版
>
> 另外，**osk2** 在我的拋磚引玉之下，Forked 了這個專案讓他支援的產品線更豐富、有更好的使用體驗
> 我推薦大家在 home assistant v2025.1 之後，這個 project 失效時，可以考慮轉用[他維護的 project](https://github.com/osk2/panasonic_smart_app)
>
> 感謝這個專案讓我交到了一些不同領域的專家
> 我還是會嘗試翻新這個 Project，但目標將會是穩定、效能、還有提供對應的 UI，提供整合 UI 跟 API 的 intergration
> 設備支援度會一樣專注在**冷氣**

> [!WARNING]
> When I first started this project, it was because there were no usable integrations available, so I created this project in hopes of inspiring others to contribute.
> After several major updates to Home Assistant, some functionalities have now migrated to new parameters.
> 
> However, this project has not been rewritten yet.
> Although I have considered revamping this project especially since I believe the structure could be improved. my current focus is on other commercial projects, and Python is not my primary programming language, so I haven't gotten around to it yet.
> 
> In the meantime, thanks to my initial effort, **osk2** forked this project and extended it to support more product lines and provide a better user experience.
> I highly recommend switching to [his maintained project](https://github.com/osk2/panasonic_smart_app) once this project becomes incompatible with Home Assistant v2025.1 or later.
>
> 
> I'm grateful that this project has helped me connect with experts from different fields.
> I still plan to eventually refresh this project, aiming for better stability, performance, and providing a UI that integrates both the frontend and API for a smoother integration experience.
> Device support will continue to primarily focus on **air conditioners**.


[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
# Panasonic Smart App
This is a home assistant's integration for panasonic smart app.

## Why do I Need this?
Due to Panasonic climates' api in Taiwan are separate to global.
We can't use [python-panasonic-comfort-cloud] and [panasonic_ac] in `Home Assistant`.

So I create [python-panasonic-smart-app] and [panasonic_smart_app] integration.

# How to Install?

### via HACS
You can install the component via the `Home Assistant Community Store (HACS)` directly.

### Manually
Copy `__init__.py`, `climate.py`, and `manifest.json` to the `custom_components/panasonic_smart_app/` folder.


## Configuration
Add the following configuration in configuration.yaml:

```
climate:
  - platform: panasonic_smart_app
    username: !secret smart_app_account
    password: !secret smart_app_password
```

## Entities Available
- **climate**: Air Condition with `CZ-T007` wifi model.

# Attention
This project only test with `Panasonic air conditioner - PX series` which use `CZ-T007` wifi adapater. `CZ-T005`, `CZ-T006` or `PXGD` series might occurs some error.

## Tested
|  Series   | Model      | Adapater |
| :-------: | ---------- | -------- |
| PX Series | CS-RX28GA2 | CZ-T007  |
| RX Series | CS-RX28GA2 |          |
|     -     | CS-RX36GA2 |          |
|     -     | CS-RX50GA2 |          |
|     -     | CS-RX71GA2 |          |


## Appreciate
[@clspeter] for RX series testing.

[@clspeter]: https://github.com/PhantasWeng/panasonic_smart_app/issues/5
---
## And..
### You can also...

<a href="https://www.buymeacoffee.com/phantas"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=phantas&button_colour=FFDD00&font_colour=000000&font_family=Poppins&outline_colour=000000&coffee_colour=ffffff"></a>


--

# Logs
How to open the logs record?

Set config in `configuration.yaml` like below:

```yaml
logger:
  default: warning
  logs:
    custom_components.panasonic_smart_app: debug
```
