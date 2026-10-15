# python-4-ntwrkngnrs

Python for network engineers: study notes, exercises and small labs collected while moving from CLI-driven operations to network automation.

The goal of this repository is to **gather everything in one place first** and later **merge it into a single study-and-review guide**. Until then, each piece keeps a record of where it came from (`source`) and how finished it is (`status`).

## Repository map

```text
.
├── 01-fundamentals-and-syntax/     guide.md   (Week 1)
├── 02-data-types-files-and-lists/  guide.md   (Week 2)
├── 03-flow-control/                guide.md   (Week 3)
└── labs/
    ├── how-network-devices-behave/ hub, ARP cache, switch and router in Python
    ├── leonardo-furtado/           packets-and-Python exercises
    └── gustavo-kalau/              "Do CLI ao Código": containerlab labs + Netmiko
```

One topic per numbered folder. Hands-on material that is tied to a specific author lives in `labs/`, grouped by source.

## Learning path

| # | Guide | Topics | Status |
| :-: | :--- | :--- | :-: |
| 01 | [Fundamentals and syntax](01-fundamentals-and-syntax/guide.md) | `venv` and `pip`, IPython REPL, PEP 8 and naming, `input`/`print`, running scripts (shebang, `chmod`) | needs review |
| 02 | [Data types, files and lists](02-data-types-files-and-lists/guide.md) | numbers, booleans and `None`, files and `with`, lists, mutable vs. immutable, shallow vs. deep copy, tuples | needs review |
| 03 | [Flow control](03-flow-control/guide.md) | `if`/`elif`/`else`, `for`, `while`, `break`/`continue`, list comprehensions, generator expressions | needs review |

Each guide follows the same pattern: network analogy → concept → hands-on exercises with solutions → cheat sheet.

**Not covered yet:** dictionaries, sets, functions, classes and modules. The labs already use them (see below), so expect the next guides to start there.

## Labs

| Lab | Description | Prerequisites |
| :--- | :--- | :--- |
| [`labs/how-network-devices-behave`](labs/how-network-devices-behave/) | Simulates an Ethernet hub, an ARP cache, a MAC-learning switch and an IP router with longest-prefix match | Guides 01–03 plus dicts, functions and classes |
| [`labs/leonardo-furtado`](labs/leonardo-furtado/) | Basic scripts and a small OOP inventory manager | Guide 01 (scripts 01–02); classes (script 05) |
| [`labs/gustavo-kalau`](labs/gustavo-kalau/) | Containerlab topologies plus Netmiko scripts from the *Do CLI ao Código* series | Guides 01–03 plus dicts and f-strings; Docker and containerlab |

See [`labs/README.md`](labs/README.md) for details.

## Sources and attribution

| Material | Source | Notes |
| :--- | :--- | :--- |
| Guides 01–03 | Kirk Byers, *Learning Python for Network Engineers* ([twin-bridges/learning_python](https://github.com/twin-bridges/learning_python)) | Personal study notes written while following the course |
| `labs/leonardo-furtado/` | Leonardo Furtado | Exercises collected from his material; add the exact link |
| `labs/gustavo-kalau/` | Gustavo Kalau, [*Do CLI ao Código*](https://gustavokalau.com.br/do-cli-ao-codigo/) | My own practice code written while following the series; the original material belongs to the author |
| `labs/how-network-devices-behave/` | **Origin to be documented** | Add the author or course link |

Before publishing or redistributing any of this material, check the license of each original source. The MIT license in this repository covers only the original work in it.

## Setup

Python 3.10 or newer is required (the refactored inventory manager uses `match`/`case`).

```bash
python3 -m venv netauto_venv
source netauto_venv/bin/activate      # Windows: netauto_venv\Scripts\activate
python -m pip install --upgrade pip
```

The [Week 1 guide](01-fundamentals-and-syntax/guide.md) explains what a virtual environment is (spoiler: it is a VRF for your Python packages) and how to use IPython for quick experiments.

## Adding new material

Start every Markdown file with this header so the sources stay traceable when everything is merged later:

```yaml
---
title: "Short title"
source: "Who or what this is based on"
status: draft | needs-review | reviewed
---
```

## License

[MIT](LICENSE)
