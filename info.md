
# Panasonic Smart App
This is a home assistant's integration for panasonic smart app.

For complete info, please go to [Repository]'s README.

[Repository]: https://github.com/PhantasWeng/panasonic_smart_app

## Why do I Need this?
Due to Panasonic climates' api in Taiwan are separate to global.
We can't use [python-panasonic-comfort-cloud] and [panasonic_ac] in `Home Assistant`.

So I create [python-panasonic-smart-app] and [panasonic_smart_app] integration.

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

## And..
### You can also...

<a href="https://www.buymeacoffee.com/phantas"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=phantas&button_colour=FFDD00&font_colour=000000&font_family=Poppins&outline_colour=000000&coffee_colour=ffffff"></a>
