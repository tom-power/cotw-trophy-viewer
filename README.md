# Trophy Viewer for theHunter: Call of the Wild

Wanted to be able to search/sort what I do/don't have in my trophy lodge, seems to work, YMMV!

![screenshot](https://github.com/tom-power/cotw-trophy-viewer/blob/main/assets/screenshot.png)

## Installation 

Download .exe from the [release page](https://github.com/tom-power/cotw-trophy-viewer/releases/latest) and run locally.

## Run/build

```
git clone https://github.com/tom-power/cotw-trophy-viewer.git &&
cd cotw-trophy-viewer
```

then

- windows `sh\setup.bat && sh\build.bat`
- unix `sh/setup.sh && sh/build.sh`

check `sh` for other scripts to run locally etc

## Notes/todo/help

the following are mapped, please shout if inaccurate:

- `fur type` from `global_animal_types.blo`
- `animal type` from `global_animal_types.blo`
- `medals` mapped from `ScoreRank` in the `trophy_lodges_adf` 
- `difficulty` mapped from `Difficulty` in the `trophy_lodges_adf`

don't know if [Parque Fernando lodge](https://thehuntercotw.fandom.com/wiki/Missions/Parque_Fernando_Missions#Main_Missions) shows up or not as haven't got to it in the game :)

## Questions

- `include all animals` in filter, idea is to include unmounted animals so you know what's left, is this intuitive? 
- `and or` in the filter, will anyone ever use `or`?

## Thanks

Lots copied from these, thanks!

- [cotw-harvest-tracker](https://github.com/LordHansCapon/cotw-harvest-tracker)
- [animal-population-changer](https://github.com/cpypasta/apc)
- [deca](https://github.com/kk49/deca)

## Disclaimer

_This application is not affiliated, maintained, authorized, endorsed by, or in any way officially
connected with Avalanche Studios Group, or any of its subsidiaries or its affiliates. The official
theHunter™ Call of the Wild website can be found
at [callofthewild.thehunter.com](https://callofthewild.thehunter.com). theHunter™ Call of the Wild
is a registered trademark of [Avalanche Studios Group](https://avalanchestudios.com/)._
