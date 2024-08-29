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
        text="attendance",
        vector="attendance"
    ),
    Model(
        key="leaves",
        type="value",
        text="leave",
        vector="leave"
    ),
    Model(
        key="overtimes",
        type="value",
        text="overtime",
        vector="overtime"
    ),
]