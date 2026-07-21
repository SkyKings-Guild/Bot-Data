import json
import re
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
                    "name": item["name"],
                }
            else:
                accessories[item["id"].lower()]["rarity"] = tier
                accessories[item["id"].lower()]["name"] = item["name"]
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
            if "recipes" in accessoryinfo:
                for recipe in accessoryinfo["recipes"]:
                    if recipe["type"] == "forge":
                        for resource in recipe["inputs"]:
                            item_id = resource.split(":")[0].lower()
                            if item_id in accessories:
                                accessories[item_id]["upgrade"] = accessoryinfo[
                                    "internalname"
                                ].lower()
                                break
                    elif recipe["type"] == "crafting":
                        item = recipe.get("B2", None)
                        if item:
                            item_id = item.split(":")[0].lower()
                            if item_id in accessories:
                                accessories[item_id]["upgrade"] = accessoryinfo[
                                    "internalname"
                                ].lower()
    # manually update parents if we missed anything
    parents_resp = requests.get(f"{BASE_URI}/constants/parents.json")
    if parents_resp.ok:
        pdata = parents_resp.json()
        parents = {}
        for k, v in pdata.items():
            for i in v:
                parents[i] = k
        for item in accessories:
            if accessories[item].get("upgrade") is None and item in parents:
                print(f"Manually setting upgrade for {item} to {parents[item]}")
                accessories[item]["upgrade"] = parents[item]
    with open("skyblock/accessories.json", "w") as f:
        json.dump(accessories, f, indent=4)


minecraft_fmt_regex = re.compile(r"§[a-z\d]")


def remove_mc_fmt(text: str) -> str:
    return minecraft_fmt_regex.sub("", text)


def update_bestiary():
    data = requests.get(f"{BASE_URI}/constants/bestiary.json").json()
    bestiary = {}
    brackets = data.pop("brackets", {})
    bestiary["brackets"] = brackets
    bestiary["islands"] = islands = {}
    for name, island in data.items():
        islands[name] = {
            "id": name,
            "name": island["name"],
        }
        if island.get("hasSubcategories", False):
            islands[name]["subcategories"] = subcategories = {}
            for subname, subcategory in island.items():
                if subname in ("name", "icon", "hasSubcategories"):
                    continue
                subcategories[subname] = {
                    "name": subcategory["name"],
                }
                subcategories[subname]["mobs"] = mobs = {}
                for mob in subcategory["mobs"]:
                    mobs[remove_mc_fmt(mob["name"])] = {
                        "name": remove_mc_fmt(mob["name"]),
                        "cap": mob["cap"],
                        "bracket": mob["bracket"],
                        "max_tier": sum(1 for cap in brackets.get(str(mob["bracket"]), {}) if cap <= mob["cap"]),
                        "mob_ids": mob["mobs"],
                    }
        else:
            islands[name]["mobs"] = mobs = {}
            for mob in island["mobs"]:
                mobs[remove_mc_fmt(mob["name"])] = {
                    "name": remove_mc_fmt(mob["name"]),
                    "cap": mob["cap"],
                    "bracket": mob["bracket"],
                    "max_tier": sum(1 for cap in brackets.get(str(mob["bracket"]), {}) if cap <= mob["cap"]),
                    "mob_ids": mob["mobs"],
                }
    with open("skyblock/bestiary.json", "w") as f:
        json.dump(bestiary, f, indent=4)


def update_forge():
    with open("skyblock/forge.json", "r") as f:
        data = json.load(f)
    for i, item in enumerate(data.keys()):
        print(f"Fetching forge recipe for {item} ({i + 1}/{len(data)})")
        resp = requests.get(f"{BASE_URI}/items/{item.upper()}.json")
        if not resp.ok:
            print(f"Failed to fetch data for {item}: {resp.status_code} - {resp.text}")
            continue
        item_data = resp.json()
        recipe = [r for r in item_data.get("recipes", []) if r.get("type") == "forge"]
        if not recipe:
            print(f"No forge recipe found for {item}")
            continue
        recipe = recipe[0]
        data[item]["time"] = recipe["duration"]
        data[item]["count"] = int(recipe["count"])
        data[item]["name"] = remove_mc_fmt(item_data["displayname"]).replace("{LVL}", "1")
        if "ingredients" not in data[item]:
            data[item]["ingredients"] = {}
        for finput in recipe.get("inputs", []):
            if finput.startswith("SKYBLOCK_COIN"):
                data[item]["coins"] = int(float(finput.split(":")[1]))
            else:
                craftitem, count = finput.split(":")
                data[item]["ingredients"][craftitem.upper()] = int(float(count))
    with open("skyblock/forge.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    update_reforges()
    update_accessories()
    update_bestiary()
    update_forge()
