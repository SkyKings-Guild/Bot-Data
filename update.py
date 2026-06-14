import difflib
import json
from typing import TypedDict

import requests

BASE_URI = "https://raw.githubusercontent.com/NotEnoughUpdates/NotEnoughUpdates-REPO/refs/heads/master"


def update_reforges():
    data = requests.get(f"{BASE_URI}/constants/reforgestones.json").json()
    reforges = {}
    for reforgestone in data.values():
        reforges[
            reforgestone.get("nbtModifier", reforgestone["reforgeName"]).lower()
        ] = reforgestone["internalName"].lower()
    with open("skyblock/reforges.json", "w") as f:
        json.dump(reforges, f, indent=4)


class AccessoryData(TypedDict):
    rarity: str
    upgrade: str | None


def update_accessories():
    data = requests.get("https://api.hypixel.net/v2/resources/skyblock/items").json()
    with open("skyblock/accessories.json", "r") as f:
        accessories: dict[str, AccessoryData] = json.load(f)
    for item in data["items"]:
        if item.get("category", "") == "ACCESSORY":
            tier = item.get("tier", "COMMON").lower()
            if item["id"].lower() not in accessories:
                print(f"Adding accessory {item['id']} with rarity {tier}")
                accessories[item["id"].lower()] = {
                    "rarity": tier,
                    "upgrade": None,
                }
            else:
                accessories[item["id"].lower()]["rarity"] = tier
    for i, item in enumerate(accessories):
        if (levelstr := item.split("_")[-1]).isnumeric():
            level = int(levelstr)
            base_item = "_".join(item.split("_")[:-1])
            upgraded = f"{base_item}_{level + 1}"
            if upgraded in accessories:
                accessories[item]["upgrade"] = upgraded
        else:
            # some accessories are upgradable by crafting, so we fetch the recipe and check
            print(
                f"{i}/{len(accessories)} Checking if {item} is upgradable by crafting"
            )
            resp = requests.get(f"{BASE_URI}/items/{item.upper()}.json")
            if not resp.ok:
                print(
                    f"Failed to fetch data for {item}: {resp.status_code} - {resp.text}"
                )
                continue
            accessoryinfo = resp.json()
            if "recipe" in accessoryinfo:
                item = accessoryinfo["recipe"].get("B2", None)
                if item:
                    item_id = item.split(":")[0].lower()
                    if item_id in accessories:
                        accessories[item_id]["upgrade"] = accessoryinfo[
                            "internalname"
                        ].lower()
    with open("skyblock/accessories.json", "w") as f:
        json.dump(accessories, f, indent=4)


if __name__ == "__main__":
    update_reforges()
    update_accessories()
