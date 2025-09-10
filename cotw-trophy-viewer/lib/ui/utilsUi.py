from nicegui import ui


def headerHome():
    with ui.element("div").style("display:grid;grid-template-columns:1fr auto;width:100%"):
        with ui.element("div"):
            ui.label("TROPHIES").style("font-size:30px;color:#666;")


def isDiamondTrophy(trophies, animal):
    for animalData in trophies.animals[animal]:
        if animalData.ratingIcon == 0:
            return True
    return False


def footer():
    pass
