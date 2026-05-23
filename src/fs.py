from pathlib import Path


def get_xlsx(folder_path: str) -> list[str]:
    folder = Path(folder_path)
    folder.mkdir(parents=True, exist_ok=True)
    # print([folder.glob("*.xlsx")])
    # xlsx_files = [
    #     str(file)
    #     for file in folder.glob("*.xlsx")
    #     if not file.name.startswith("~$")
    # ]
    xlsx_files = [
        file
        for file in folder.glob("*xlsx")
        if "~$" not in file.name
    ]

    return xlsx_files