# Bot-Data

Data used by the [SkyKings](https://discord.gg/skykings) Public Discord bot.

All data is stored as JSON and is validated by `check.py` on every commit.

## Repository Structure

```
Bot-Data/
├── skyblock/          # Hypixel SkyBlock game data
│   ├── networth/      # Data used for networth calculations
│   └── *.json
├── misc/              # Miscellaneous bot data (emojis, aliases, etc.)
├── check.py           # JSON validation script
└── requirements.txt   # Python dependencies for check.py
```

---

## `skyblock/`

### `accessories.json`

A map of accessory/talisman item IDs to their rarity and upgrade information.

```json
{
  "<item_id>": {
    "rarity": "common | uncommon | rare | epic | legendary | ...",
    "upgrade": "<upgraded_item_id> | null"
  }
}
```

The `upgrade` field points to the next tier of the same accessory family, or `null` if there is no upgrade.

---

### `bestiary.json`

Bestiary mob data organised by location. Each mob entry contains the maximum kill-count level and whether the mob is a boss.

```json
{
  "mobs": {
    "<location>": {
      "<mob_id>": {
        "maxLevel": <integer> | null,
        "boss": <boolean>
      }
    }
  }
}
```

---

### `bit-prices.json`

Prices (in bits) for items available in the Community Shop. The special `_enchants` key holds a sub-object of enchant name → bit cost mappings.

```json
{
  "<item_name>": <bit_cost>,
  "_enchants": {
    "<enchant_name> <level>": <bit_cost>
  }
}
```

---

### `crimson.json`

Crimson Isle Dojo data. Currently stores the minimum point thresholds required to achieve each belt rank.

```json
{
  "dojo_belts": {
    "<belt_colour>": <minimum_points>
  }
}
```

---

### `dungeons.json`

Cumulative XP required to reach each Catacombs level. The array is zero-indexed, so index `n` holds the total XP needed for level `n`.

```json
{
  "catacombs": [<xp_at_level_0>, <xp_at_level_1>, ...]
}
```

---

### `enchants.json`

Metadata for every SkyBlock enchantment.

```json
{
  "<enchant_name_lowercase>": {
    "name": "<Display Name>",
    "id": "<internal_api_id>",
    "max_table": <max level obtainable from an enchanting table>,
    "max": <absolute maximum level>,
    "stacking": true,          // present only when the enchant is a stacking enchant
    "ultimate": true,          // present only when the enchant is an ultimate enchant
    "upgrade_stones": {
      "<level>": "<ITEM_ID>"   // present only for levels that require an upgrade stone
    }
  }
}
```

---

### `forge.json`

Forge recipes for the Dwarven Mines / Crystal Hollows forge.

```json
{
  "<ITEM_ID>": {
    "hotm": <minimum HotM tier required>,
    "time": <forge duration in seconds>,
    "collections": {           // optional – collection requirements
      "<ITEM_ID>": <tier>
    },
    "ingredients": {
      "<ITEM_ID>": <quantity>
    }
  }
}
```

---

### `garden.json`

Data related to the Garden island.

- **`matter`** – Crop item IDs and their equivalent Garden Matter value (used for composter calculations).
- **`fuel`** – Fuel item IDs and their equivalent composter fuel value.

```json
{
  "matter": { "<ITEM_ID>": <matter_value> },
  "fuel":   { "<ITEM_ID>": <fuel_value> }
}
```

---

### `gemstones.json`

Stats granted by each gemstone type at every quality tier and slot position (0–6, where position index maps to the slot type used by the SkyBlock API).

```json
{
  "<GEMSTONE_TYPE>": {
    "name": "<Display Name>",
    "color": "<minecraft_colour_code>",
    "stats": {
      "<QUALITY>": {
        "<stat_name>": [<slot_0_value>, <slot_1_value>, ..., <slot_6_value>]
      }
    }
  }
}
```

`null` in a stat array means the gemstone cannot be placed in that slot type.

---

### `hotm.json`

Cumulative XP required to reach each Heart of the Mountain (HotM) tier. Index `n` holds the total XP needed for tier `n`.

```json
{
  "experience": [<xp_at_tier_0>, <xp_at_tier_1>, ...]
}
```

---

### `lily_weight.json`

Constants used for the Lily weight formula.

- **`dungeons`** – Per-floor completion buffs and a full catacombs XP table used to convert raw XP to level.
- **`skills`** – Per-skill weight constants.
- **`slayer`** – Per-slayer weight constants.

---

### `minions.json`

The number of unique minion recipes needed to unlock each additional minion slot.

```json
{
  "slot_unlocks": [<recipes_for_slot_1>, <recipes_for_slot_2>, ...]
}
```

---

### `pets.json`

Cumulative XP required to reach each pet level. Index `n` holds the total XP needed for level `n + 1`.

```json
{
  "levels": [<xp>, ...]
}
```

---

### `rarities.json`

Minecraft formatting colour codes for each item rarity.

```json
{
  "<RARITY>": {
    "color": "<minecraft_colour_code>"
  }
}
```

---

### `reforges.json`

Maps each reforge name to the item ID of the reforge stone required to apply it.

```json
{
  "<reforge_name>": "<REFORGE_STONE_ITEM_ID>"
}
```

---

### `skills.json`

Cumulative XP required to reach each level for different skill categories.

- **`runecrafting`** – XP table for the Runecrafting skill (max level 25).
- **`skills`** – XP table used by all standard skills (Farming, Mining, Combat, etc.).
- **`dungeoneering`** *(if present)* – XP table for Dungeoneering.

```json
{
  "<skill_category>": [<xp_at_level_1>, <xp_at_level_2>, ...]
}
```

---

### `slayers.json`

XP thresholds and XP-per-kill values for each slayer type.

```json
{
  "<slayer_type>": {
    "levels": [<xp_for_tier_1>, <xp_for_tier_2>, ...],
    "xp_gain": [<xp_per_kill_tier_1>, <xp_per_kill_tier_2>, ...]
  }
}
```

---

### `weight.json`

Constants used by the Senither weight formula.

- **`dungeon_groups`** – Weight multipliers for the Catacombs dungeon and each class.
- **`skill_groups`** – Per-skill weight constants including the exponent, divider, and max level.

```json
{
  "dungeon_groups": { "<key>": <multiplier> },
  "skill_groups": {
    "<skill>": {
      "exponent": <float>,
      "divider": <integer>,
      "maxLevel": <integer>
    }
  }
}
```

---

## `skyblock/networth/`

Data used when calculating a player's networth.

### `allowed_enchants.json`

List of enchantment IDs whose levels are factored into an item's networth value.

```json
{ "data": ["<enchant_id>", ...] }
```

### `blocked_enchants.json`

Per-item overrides listing enchantment IDs that should **not** count toward networth for that specific item.

```json
{ "<item_id>": ["<enchant_id>", ...] }
```

### `essence_tiers.json`

Essence costs (in units) for each upgrade tier of essence-upgradeable items.

```json
{ "tiers": [<cost_tier_1>, <cost_tier_2>, ...] }
```

### `price_overrides.json`

Manual price overrides for specific items (keyed by item ID). An empty object means no overrides are currently set.

```json
{ "<ITEM_ID>": <price_in_coins> }
```

---

## `misc/`

### `enrichment-emojis.json`

Discord emoji strings for each accessory enrichment stat, used in bot responses.

```json
{ "<stat_id>": "<discord_emoji_string>" }
```

### `guild.json`

Guild XP requirements per level. The `xpreq` array is zero-indexed — index `n` holds the XP needed to advance from level `n` to level `n + 1`.

```json
{ "xpreq": [<xp>, ...] }
```

### `item-id-aliases.json`

Maps legacy or alternative SkyBlock item IDs to their canonical API ID. Used to normalise item IDs that may appear in different forms across the API.

```json
{ "<legacy_id>": "<canonical_id>" }
```

### `profile-emojis.json`

Discord emoji strings (or Unicode characters) for each SkyBlock profile fruit icon.

```json
{ "<fruit_name>": "<emoji_or_unicode>" }
```

### `rarity-emojis.json`

Discord emoji strings for each item rarity tier.

```json
{ "<rarity_lowercase>": "<discord_emoji_string>" }
```

---

## Validation

Run the included `check.py` script to verify that all JSON files parse correctly:

```bash
pip install -r requirements.txt
python check.py
```

## Contributing

If you spot missing or incorrect data, please open an issue or submit a pull request. When adding new entries make sure to run `check.py` to confirm your changes are valid JSON.
