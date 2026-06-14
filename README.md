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

## Validation

Run the included `check.py` script to verify that all JSON files parse correctly:

```bash
pip install -r requirements.txt
python check.py
```

## Contributing

If you spot missing or incorrect data, please open an issue or submit a pull request. When adding new entries make sure to run `check.py` to confirm your changes are valid JSON.

## Licensing

Parts of this project utilize data from [NotEnoughUpdates/NotEnoughUpdates-REPO](https://github.com/NotEnoughUpdates/NotEnoughUpdates-REPO/blob/master/LICENSE), which is licensed under the MIT License. See the included [NEU-LICENSE.md](./NEU-LICENSE.md) file for the full copyright notice.
