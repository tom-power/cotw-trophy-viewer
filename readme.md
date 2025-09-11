# COTW trophy viewer

Tool to view your COTW trophies.

Uses `trophy_lodges_adf` and mapping to work out names.

Lots copied from:

- [cotw-harvest-tracker](https://github.com/LordHansCapon/cotw-harvest-tracker)
- [animal-population-changer](https://github.com/cpypasta/apc)

### Installation

...

### Usage

...


### Build

...

### Animal type mapping

Mapping `TrophyAnimal` -> `Type` in `trophy_lodges_adf` manually at the moment, and any help with that would be much appreciated.

Please do via PR against [this](https://github.com/tom-power/cotw-trophy-viewer/blob/main/cotw-trophy-viewer/lib/model/animalType.py) file, or issue etc.

```
{
  ...
  "TrophyAnimal": {
      ...
      "Type": 1511159411 // this is a fallow deer
      ...
  }
}
```

You can check your `trophy_lodges_adf` using the [adf tool](https://mathartbang.com/deca/tool/adf.html).

Alternatively, if anyone has insight as to how the `Type` is generated and could share that would be fantastic.
