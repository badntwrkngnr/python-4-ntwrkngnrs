# Lab: Packets and Python (Leonardo Furtado)

> **Source:** exercises from Leonardo Furtado's material (kept from the original folder name `02-packets-and-python-leonardo-furtado`). Add the link to the exact course or repository here.

The numbering below is the original one. Items `03` and `04` are not in this repository.

| # | File | What it practises | Level |
| :-: | :--- | :--- | :--- |
| 01 | [`01-basic-monitoring-scenario.py`](01-basic-monitoring-scenario.py) | Variables, arithmetic, `str()` conversion and string concatenation | Guide 01 |
| 02 | [`02-bandwidth-calculation-for-a-link.py`](02-bandwidth-calculation-for-a-link.py) | Integer maths (speed × channels) and building output strings | Guide 01 |
| 05 | [`05-think-like-a-programmer/network-inventory-manager.py`](05-think-like-a-programmer/network-inventory-manager.py) | First version: classes (`NetworkDevice`, `InventoryManager`), a menu loop, list comprehension | Classes needed |
| 05 | [`05-think-like-a-programmer/network-inventory-manager-refactored.py`](05-think-like-a-programmer/network-inventory-manager-refactored.py) | Same program refactored: logic moved into `update_device_status()`, a `main()` function, `match`/`case`, `if __name__ == "__main__"` | Classes needed, **Python 3.10+** |

## Reading the two inventory managers side by side

Compare them after you have written your own version. The refactoring changes *structure*, not behaviour:

- the update logic leaves the menu loop and becomes a method that returns `True`/`False`;
- the main program is wrapped in `main()` so the file can be imported without running;
- the `if / elif / else` chain becomes `match` / `case`.

## Run

```bash
cd labs/leonardo-furtado
python 01-basic-monitoring-scenario.py
python 02-bandwidth-calculation-for-a-link.py
python 05-think-like-a-programmer/network-inventory-manager-refactored.py
```
