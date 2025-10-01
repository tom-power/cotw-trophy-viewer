# COTW trophy viewer

Wanted a quick overview of what I had/didn't have in my trophy lodges.

Lots copied from these (thank you!):

- [cotw-harvest-tracker](https://github.com/LordHansCapon/cotw-harvest-tracker)
- [animal-population-changer](https://github.com/cpypasta/apc)
- [deca](https://github.com/kk49/deca)

## Disclaimer

_This application is not affiliated, maintained, authorized, endorsed by, or in any way officially
connected with Avalanche Studios Group, or any of its subsidiaries or its affiliates. The official
theHunter™ Call of the Wild website can be found
at [callofthewild.thehunter.com](https://callofthewild.thehunter.com). theHunter™ Call of the Wild
is a registered trademark of [Avalanche Studios Group](https://avalanchestudios.com/)._

## Installation 

Download binaries from the [release page](https://github.com/tom-power/cotw-trophy-viewer/releases/latest) and run locally.

## Run/build

```
git clone https://github.com/tom-power/cotw-trophy-viewer.git &&
cd cotw-trophy-viewer
```

then:

- windows `sh\setup.bat && sh\build.bat`
- unix `sh/setup.sh && sh/build.sh`

check `sh` for other scripts to run locally etc

## Notes

Tested on steam on pc with the animals I have currently.

## Help

Don't know how to get names for `fur type` currently, any help welcome!

Very likely missing animal names, their name won't appear in the `Animal` column, let me know in an issue. 

Have been guessing names and checking in `test_hash.py`, probably easier to mot hash in the first place but I haven't explored.