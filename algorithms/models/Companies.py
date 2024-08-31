from dataclasses import dataclass

@dataclass
class Model:
    key: str
    type: str
    text: str
    vector: str


companies: [Model] = [
    Model(
        key="4551d565-a6af-4d15-a857-f61748f783aa",
        type="value",
        text="akatsuki",
        vector="akatsuki"
    ),
    Model(
        key="81333dc8-49b4-49d4-8c81-6f6c6fc827d4",
        type="value",
        text="hik",
        vector="hik"
    )
]