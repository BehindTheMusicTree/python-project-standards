# String enumerations (`StrEnum`)

Part of the organization **[development baseline](development.md)**.

Organization baseline for enumerations whose members are strings (API keys, error codes, filter field names, etc.).

## Requirement

Target **Python 3.11+**. For those enumerations, subclass **`enum.StrEnum`** from the standard library. Do **not** use the older **`class Foo(str, Enum)`** mixin pattern.

- **`StrEnum`** is the documented stdlib base for string enums: members behave as `str` in most contexts, with `__str__` / `__format__` aligned to `str` (see the [enum module](https://docs.python.org/3/library/enum.html#enum.StrEnum)).
- **`(str, Enum)`** is discouraged for new code in org repositories.

**Good:**

```python
from enum import StrEnum

class FieldKey(StrEnum):
    NAME = "name"
```

**Bad:**

```python
from enum import Enum

class FieldKey(str, Enum):
    NAME = "name"
```

## `isinstance` and built-in `str`

Rare code uses `type(x) is str` instead of `isinstance(x, str)`. Enum members are instances of the enum class; if a true built-in `str` is required, pass **`str(member)`**.

## Enforcement

**Prefer lint (Ruff).** Ruff **[UP042](https://docs.astral.sh/ruff/rules/replace-str-enum/)** (`replace-str-enum`, pyupgrade) reports `class Foo(str, Enum)` (and the `enum.Enum` + `str` ordering) and can suggest migrating to **`StrEnum`**. It is active whenever **`UP`** appears in **[`tool.ruff.lint` `select`](https://docs.astral.sh/ruff/settings/#lint_select)** and your **`target-version`** is **3.11+**. The org **`templates/pyproject/pyproject.toml`** baseline already includes **`UP`** in `select`, so **`pre-commit`** / CI running **`ruff check`** is the normal enforcement path.

**Optional extras:**

- A **duplicate** pre-commit hook or small AST script (fail on `(str, Enum)` bases) if you want belt-and-suspenders or stricter failure modes than Ruff alone — keep it aligned with this doc if you keep it.
- **Cursor** / contributor **`.mdc`** rules that point here for editor and agent behavior.

If you **disable** `UP042` explicitly or drop **`UP`** from `select`, you are opting out of lint enforcement; document that choice in the consumer repo.
