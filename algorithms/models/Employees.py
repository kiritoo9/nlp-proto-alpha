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
        text="gusion persley",
        vector="gusion persley"
    ),
    Model(
        key="2013310017",
        type="value",
        text="aamon persley",
        vector="aamon persley"
    ),
    Model(
        key="2013310018",
        type="value",
        text="valentina persley",
        vector="valentina persley"
    ),
]