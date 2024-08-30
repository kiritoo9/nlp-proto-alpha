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
        key="attendances",
        type="value",
        text="presence",
        vector="presence"
    ),
    Model(
        key="leaves",
        type="value",
        text="leave",
        vector="leave"
    ),
    Model(
        key="leaves",
        type="value",
        text="vacation",
        vector="vacation"
    ),
    Model(
        key="leaves",
        type="value",
        text="permission",
        vector="permission"
    ),
    Model(
        key="leaves",
        type="value",
        text="permit",
        vector="permit"
    ),
    Model(
        key="overtimes",
        type="value",
        text="overtime",
        vector="overtime"
    ),
]