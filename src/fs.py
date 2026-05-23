from pathlib import Path


def get_xlsx(folder_path: str) -> list[str]:
    folder = Path(folder_path)
    folder.mkdir(parents=True, exist_ok=True)

    xlsx_files = [
        file
        for file in folder.glob("*xlsx")
        if not file.name.startswith("~$")
    ]

    return xlsx_files