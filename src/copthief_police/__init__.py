"""copthief_police — the cop agent's brain and role-specific configuration (NOT mirrored).

Role-repo package (M5-2, docs/PRD_police_brain.md): `PoliceBrain` — capture-commit +
expectimax over the truncated belief + barrier graph-surgery, all knobs config-owned
(`[strategy.police]` over the `features.DEFAULT_OPTIONS` data table). Wire role
string: ``"police"`` (book App B). Selected via the book §6.2 dotted notation
`copthief_police.brain:PoliceBrain`.
"""

from copthief_police.brain import PoliceBrain

__all__ = ["PoliceBrain", "__version__"]
__version__ = "1.00"
