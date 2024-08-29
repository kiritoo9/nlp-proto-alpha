from dataclasses import dataclass

@dataclass
class Model:
    key: str
    type: str
    text: str
    vector: str


companies: [Model] = [
    Model(
        key="001",
        type="value",
        text="pt akatsuki",
        vector="pt akatsuki"
    ),
    Model(
        key="002",
        type="value",
        text="hik",
        vector="hik"
    ),
    Model(
        key="003",
        type="value",
        text="pt others",
        vector="pt others"
    ),
]