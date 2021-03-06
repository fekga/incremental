# save_load_game.py
from browser import alert
from browser.local_storage import storage
# from browser.widgets.dialog import InfoDialog
from core.app_version import version_label
from core.resource import *
import time

class SaveLoadGame:
    bought_upgrades = [] # time sequence of upgrades

    def __init__(self, converters, resources, playtimeMeasurement):
        self.converters = converters
        self.resources = resources
        self.playtimeMeasurement = playtimeMeasurement

        self.save_version_key = "save_version"
        self.save_resources_key = "save_resources"
        self.save_updrages_key = "save_upgrades"
        self.save_playtime_key = "save_playtime"


    def reset_game(self):
        SaveLoadGame.bought_upgrades.clear()
        # Delete saves
        del storage[self.save_version_key]
        del storage[self.save_resources_key]
        del storage[self.save_updrages_key]
        del storage[self.save_playtime_key]
        # HACK: reload page from HTML button


    def save_game(self):
        # Version save
        versionString = version_label

        # Resource save
        resourcesString = ""
        first = True
        for resource in Resource.resources:
            if first:
                first = False
            else:
                resourcesString += "|"
            resourcesString += f'{resource.name}:{resource.amount}'

        #Upgrade save
        bought_upgrades = SaveLoadGame.bought_upgrades
        if len(bought_upgrades) > 0:
            upgradesString = "|".join(bought_upgrades)
        else:
            upgradesString = ""

        # Playtime
        playtimeString = str(int(self.playtimeMeasurement.getElapsedSeconds()))

        storage[self.save_version_key] = versionString
        storage[self.save_resources_key] = resourcesString
        storage[self.save_updrages_key] = upgradesString
        storage[self.save_playtime_key] = playtimeString


    def load_game(self):
        try:
            versionString = storage[self.save_version_key]
            resourcesString = storage[self.save_resources_key]
            upgradesString = storage[self.save_updrages_key]

            # Version warning
            if versionString != version_label:
                msg = "The game has newer version than your save."
                msg += "We will try to load the saved data, however maybe some data won't be loaded..."
                alert(msg)

            # Resource load
            resources = resourcesString.split("|")
            for res_str in resources:
                name, amount = res_str.split(":")
                for res in self.resources:
                    if res.name == name:
                        res.amount = float(amount)

            # Upgrade load
            upgrades = upgradesString.split("|")
            SaveLoadGame.bought_upgrades.clear()
            for bought_upgrade in upgrades:
                for converter in self.converters:
                    for upg in converter.upgrades:
                        if upg.name == bought_upgrade:
                            upg.apply_changes() # set the SaveLoadGame.bought_upgrades automatically

            ## Playtime
            playtimeString = storage[self.save_playtime_key]
            self.playtimeMeasurement.start_time = time.time() - int(playtimeString)

        except:
            # print("Load failed")  # local save not exists yet
            pass