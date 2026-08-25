from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile


SUPPORTED_EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".html": "HTML",
    ".css": "CSS",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
}


def analyze_project(zip_path: str):
    """
    Extract a ZIP project and analyze supported source files.
    """

    analyzed_files = []

    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        with ZipFile(zip_path, "r") as zip_file:
            zip_file.extractall(temp_path)

        for file_path in temp_path.rglob("*"):
            if not file_path.is_file():
                continue

            extension = file_path.suffix.lower()

            if extension not in SUPPORTED_EXTENSIONS:
                continue

            try:
                content = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            except Exception:
                continue

            analyzed_files.append(
                {
                    "path": str(file_path.relative_to(temp_path)),
                    "language": SUPPORTED_EXTENSIONS[extension],
                    "content": content,
                }
            )

    return analyzed_files


def build_codebase_context(analyzed_files):
    """
    Convert analyzed source files into a structured
    text context that can be sent to Gemini.
    """

    sections = []

    for file in analyzed_files:
        section = (
            f'FILE: {file["path"]}\n'
            f'LANGUAGE: {file["language"]}\n\n'
            f'```{file["language"].lower()}\n'
            f'{file["content"]}\n'
            f'```\n'
        )

        sections.append(section)

    return "\n\n".join(sections)