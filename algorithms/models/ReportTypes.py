from dataclasses import dataclass

@dataclass
class Model:
    key: str
    type: str
    text: str
    vector: str


report_types: [Model] = [
    Model(
        key="attendances",
        type="value",
        text="attendances reports",
        vector="attendances reports"
    ),
    Model(
        key="leaves",
        type="value",
        text="leaves reports",
        vector="leaves reports"
    ),
    Model(
        key="overtimes",
        type="value",
        text="overtimes reports",
        vector="overtimes reports"
    ),
]