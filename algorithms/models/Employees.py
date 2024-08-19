from dataclasses import dataclass

@dataclass
class Model:
    key: str
    type: str
    text: str
    vector: str


employees: [Model] = [
    Model(
        key="2013310016",
        type="value",
        text="gusion persley 2013310016",
        vector="gusion persley 2013310016"
    ),
    Model(
        key="2013310017",
        type="value",
        text="aamon persley 2013310017",
        vector="aamon persley 2013310017"
    ),
    Model(
        key="2013310018",
        type="value",
        text="valentina persley 2013310018",
        vector="valentina persley 2013310018"
    ),
]