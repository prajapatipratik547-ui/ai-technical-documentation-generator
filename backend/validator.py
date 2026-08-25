import re


# =========================================================
# Core documentation sections
# =========================================================

CORE_SECTIONS = {
    "Project Overview": [
        "project overview",
        "overview",
        "project summary",
    ],

    "Purpose and Main Features": [
        "purpose and main features",
        "purpose",
        "main features",
        "features",
        "purpose & features",
        "purpose and features",
    ],

    "Technology Stack": [
        "technology stack",
        "tech stack",
        "technologies used",
        "technology",
        "tech used",
    ],

    "Project Architecture": [
        "project architecture",
        "architecture",
        "system architecture",
        "application architecture",
    ],

    "Directory / File Structure": [
        "directory / file structure",
        "directory/file structure",
        "file structure",
        "directory structure",
        "project structure",
    ],

    "Important Components": [
        "important components",
        "key components",
        "components",
        "core components",
    ],

    "Installation Instructions": [
        "installation instructions",
        "installation",
        "setup",
        "getting started",
        "setup instructions",
    ],

    "How to Run the Project": [
        "how to run the project",
        "how to run",
        "running the project",
        "run the project",
        "running",
    ],

    "Dependencies": [
        "dependencies",
        "required packages",
        "packages",
        "libraries",
    ],

    "Summary": [
        "summary",
        "conclusion",
        "project summary",
    ],
}


# =========================================================
# Optional documentation sections
# =========================================================

OPTIONAL_SECTIONS = {
    "API Documentation": [
        "api documentation",
        "api",
        "api reference",
        "endpoints",
        "api endpoints",
    ],

    "Data Flow": [
        "data flow",
        "data flow diagram",
        "application flow",
        "request flow",
    ],

    "Configuration": [
        "configuration",
        "configuration settings",
        "environment variables",
        "environment configuration",
    ],

    "Usage Examples": [
        "usage examples",
        "usage",
        "examples",
        "example usage",
    ],

    "Design Decisions and Implementation Notes": [
        "design decisions and implementation notes",
        "design decisions",
        "implementation notes",
        "implementation details",
    ],

    "Limitations": [
        "limitations",
        "known limitations",
        "limitations and constraints",
    ],

    "Potential Improvements": [
        "potential improvements",
        "future improvements",
        "future enhancements",
        "possible improvements",
    ],
}


# =========================================================
# Supported source file extensions
# =========================================================

SUPPORTED_EXTENSIONS = (
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".html",
    ".css",
    ".java",
    ".cpp",
    ".c",
)


# =========================================================
# Common Python built-ins
# =========================================================

COMMON_FUNCTIONS = {
    "print",
    "len",
    "str",
    "int",
    "float",
    "list",
    "dict",
    "set",
    "tuple",
    "range",
    "open",
    "enumerate",
    "zip",
    "map",
    "filter",
    "sum",
    "min",
    "max",
    "abs",
    "round",
    "sorted",
    "reversed",
    "input",
    "type",
    "super",
    "isinstance",
    "getattr",
    "setattr",
    "hasattr",
    "vars",
    "dir",
    "id",
    "repr",
    "format",
    "all",
    "any",
    "bool",
    "bytes",
    "bytearray",
    "callable",
    "chr",
    "complex",
    "delattr",
    "eval",
    "exec",
    "frozenset",
    "globals",
    "hash",
    "help",
    "hex",
    "locals",
    "oct",
    "ord",
    "pow",
    "property",
    "round",
    "slice",
    "staticmethod",
    "sum",
}


# =========================================================
# Common Python exceptions
#
# These are classes, not project functions.
# =========================================================

COMMON_EXCEPTIONS = {
    "Exception",
    "BaseException",
    "ValueError",
    "TypeError",
    "KeyError",
    "IndexError",
    "NameError",
    "AttributeError",
    "ImportError",
    "ModuleNotFoundError",
    "RuntimeError",
    "RuntimeWarning",
    "Warning",
    "UserWarning",
    "FileNotFoundError",
    "PermissionError",
    "ZeroDivisionError",
    "OverflowError",
    "OSError",
    "IOError",
    "LookupError",
    "StopIteration",
    "StopAsyncIteration",
    "AssertionError",
    "NotImplementedError",
    "SyntaxError",
    "IndentationError",
    "TabError",
    "UnicodeError",
    "UnicodeDecodeError",
    "UnicodeEncodeError",
    "ConnectionError",
    "TimeoutError",
}


# =========================================================
# Normalize text
# =========================================================

def normalize_text(text: str) -> str:
    """
    Normalize Markdown heading text so that small formatting
    differences do not create false-positive warnings.
    """

    text = text.lower().strip()

    # Remove Markdown heading markers
    text = re.sub(
        r"^#{1,6}\s*",
        "",
        text,
    )

    # Remove Markdown bold / italic markers
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("*", "")
    text = text.replace("_", " ")

    # Remove numbered prefixes
    #
    # Examples:
    # 1. Project Overview
    # 1) Project Overview
    # 1 - Project Overview
    #
    text = re.sub(
        r"^\d+\s*[\.\)\-:]\s*",
        "",
        text,
    )

    # Normalize ampersand
    text = text.replace("&", "and")

    # Remove trailing punctuation
    text = re.sub(
        r"[\:\-–—]+$",
        "",
        text,
    )

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# =========================================================
# Extract Markdown headings
# =========================================================

def extract_headings(
    documentation: str,
) -> list:
    """
    Extract Markdown headings from generated documentation.
    """

    headings = re.findall(
        r"^\s*#{1,6}\s+(.+?)\s*$",
        documentation,
        re.MULTILINE,
    )

    normalized_headings = []

    for heading in headings:

        normalized = normalize_text(
            heading
        )

        if normalized:
            normalized_headings.append(
                normalized
            )

    return normalized_headings


# =========================================================
# Check whether a documentation section exists
# =========================================================

def section_exists(
    normalized_headings: list,
    aliases: list,
) -> bool:
    """
    Determine whether a documentation section exists.

    Supports:
    - exact aliases
    - numbered headings
    - headings with additional descriptive text
    """

    normalized_aliases = [
        normalize_text(alias)
        for alias in aliases
    ]

    for heading in normalized_headings:

        for alias in normalized_aliases:

            # Exact match
            if heading == alias:
                return True

            # Heading starts with expected section
            if heading.startswith(
                alias + " "
            ):
                return True

            # Heading contains expected phrase
            if alias in heading:
                return True

    return False


# =========================================================
# Detect whether project has API-related code
# =========================================================

def project_has_api(
    analyzed_files: list,
) -> bool:
    """
    Determine whether the analyzed project appears to
    contain API/backend functionality.
    """

    api_keywords = [
        "fastapi",
        "flask",
        "django",
        "express",
        "router",
        "route",
        "endpoint",
        "@app.get",
        "@app.post",
        "@app.put",
        "@app.delete",
        "http",
    ]

    for file in analyzed_files:

        content = file.get(
            "content",
            "",
        ).lower()

        for keyword in api_keywords:

            if keyword in content:
                return True

    return False


# =========================================================
# Detect whether project has configuration
# =========================================================

def project_has_configuration(
    analyzed_files: list,
) -> bool:
    """
    Determine whether the project appears to use
    configuration or environment variables.
    """

    configuration_files = {
        ".env",
        ".env.example",
        "config.py",
        "config.js",
        "config.ts",
        "settings.py",
    }

    configuration_keywords = [
        "os.getenv",
        "process.env",
        "environment variable",
        "dotenv",
        "config.",
        "settings.",
    ]

    for file in analyzed_files:

        path = file.get(
            "path",
            "",
        ).replace(
            "\\",
            "/",
        ).lower()

        content = file.get(
            "content",
            "",
        ).lower()

        filename = path.split("/")[-1]

        if filename in configuration_files:
            return True

        for keyword in configuration_keywords:

            if keyword in content:
                return True

    return False


# =========================================================
# Extract Python functions
# =========================================================

def extract_python_functions(
    content: str,
) -> set:
    """
    Extract Python function definitions.
    """

    matches = re.findall(
        r"^\s*(?:async\s+)?def\s+"
        r"([A-Za-z_][A-Za-z0-9_]*)\s*\(",
        content,
        re.MULTILINE,
    )

    return set(matches)


# =========================================================
# Extract JavaScript / TypeScript functions
# =========================================================

def extract_js_ts_functions(
    content: str,
) -> set:
    """
    Extract JavaScript / TypeScript function definitions.
    """

    functions = set()

    # Normal functions
    function_matches = re.findall(
        r"\bfunction\s+"
        r"([A-Za-z_][A-Za-z0-9_]*)\s*\(",
        content,
    )

    functions.update(
        function_matches
    )

    # Arrow functions
    arrow_matches = re.findall(
        r"\b(?:const|let|var)\s+"
        r"([A-Za-z_][A-Za-z0-9_]*)"
        r"\s*=\s*"
        r"(?:\([^)]*\)|[A-Za-z_][A-Za-z0-9_]*)"
        r"\s*=>",
        content,
    )

    functions.update(
        arrow_matches
    )

    return functions


# =========================================================
# Extract all actual functions
# =========================================================

def extract_actual_functions(
    analyzed_files: list,
) -> set:
    """
    Extract function definitions from the analyzed
    codebase.
    """

    actual_functions = set()

    for file in analyzed_files:

        content = file.get(
            "content",
            "",
        )

        language = file.get(
            "language",
            "",
        )

        if language == "Python":

            actual_functions.update(
                extract_python_functions(
                    content
                )
            )

        elif language in {
            "JavaScript",
            "TypeScript",
        }:

            actual_functions.update(
                extract_js_ts_functions(
                    content
                )
            )

    return actual_functions


# =========================================================
# Extract documented function references
# =========================================================

def extract_documented_functions(
    documentation: str,
) -> set:
    """
    Extract function-like references from Markdown.

    Only inline-code references and headings are checked
    to reduce false positives.
    """

    documented_functions = set()

    # Example:
    #
    # `calculate_total()`
    #
    inline_functions = re.findall(
        r"`([A-Za-z_][A-Za-z0-9_]*)\s*\(",
        documentation,
    )

    documented_functions.update(
        inline_functions
    )

    # Example:
    #
    # ### calculate_total(price)
    #
    heading_functions = re.findall(
        r"^#{1,6}\s+`?"
        r"([A-Za-z_][A-Za-z0-9_]*)"
        r"\s*\(",
        documentation,
        re.MULTILINE,
    )

    documented_functions.update(
        heading_functions
    )

    return documented_functions


# =========================================================
# Normalize file path
# =========================================================

def normalize_path(
    path: str,
) -> str:
    """
    Normalize Windows and Unix paths.
    """

    return path.replace(
        "\\",
        "/",
    ).strip()


# =========================================================
# Extract source files from documentation
# =========================================================

def extract_documented_files(
    documentation: str,
) -> set:
    """
    Extract source filenames from generated documentation.

    Correctly handles:

        `hello.py`

        `python hello.py`

        `python main.py`

        `node server.js`

    and avoids treating URLs such as:

        https://example.com/file.py

    as project files.
    """

    documented_files = set()

    # -----------------------------------------------------
    # Remove URLs before scanning for source filenames.
    #
    # This prevents:
    #
    # https://example.com/file.py
    #
    # from becoming a fake project file.
    # -----------------------------------------------------

    documentation_without_urls = re.sub(
        r"https?://[^\s`<>]+",
        " ",
        documentation,
        flags=re.IGNORECASE,
    )

    # Also remove protocol-relative URLs.
    #
    # Example:
    #
    # //www.example.com/file.py
    #
    documentation_without_urls = re.sub(
        r"//[^\s`<>]+",
        " ",
        documentation_without_urls,
    )

    # -----------------------------------------------------
    # Source filename pattern
    # -----------------------------------------------------

    source_extensions = (
        r"\.py|"
        r"\.js|"
        r"\.jsx|"
        r"\.ts|"
        r"\.tsx|"
        r"\.html|"
        r"\.css|"
        r"\.java|"
        r"\.cpp|"
        r"\.c"
    )

    # Require the filename/path to start with a normal
    # filename character rather than "/".
    filename_pattern = (
        r"(?<![\w./-])"
        r"[A-Za-z0-9_.-]+"
        r"(?:/[A-Za-z0-9_.-]+)*"
        r"(?:" + source_extensions + r")"
        r"(?![\w.-])"
    )

    matches = re.findall(
        filename_pattern,
        documentation_without_urls,
        re.IGNORECASE,
    )

    for match in matches:

        normalized = normalize_path(
            match
        )

        # Remove accidental punctuation.
        normalized = normalized.strip(
            "`'\".,;:()[]{}<>"
        )

        # Remove leading/trailing slash.
        normalized = normalized.strip(
            "/"
        )

        if not normalized:
            continue

        if normalized.lower().endswith(
            SUPPORTED_EXTENSIONS
        ):
            documented_files.add(
                normalized
            )

    return documented_files


# =========================================================
# Main validator
# =========================================================

def validate_documentation(
    documentation: str,
    analyzed_files: list,
) -> dict:
    """
    Validate generated documentation against the
    analyzed codebase.
    """

    errors = []
    warnings = []

    # =====================================================
    # 1. Check documentation exists
    # =====================================================

    if not documentation or not documentation.strip():

        errors.append(
            "Generated documentation is empty."
        )

        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings,
            "files_checked": 0,
            "functions_checked": 0,
        }

    # =====================================================
    # 2. Extract headings
    # =====================================================

    headings = extract_headings(
        documentation
    )

    # =====================================================
    # 3. Validate core sections
    # =====================================================

    for section_name, aliases in CORE_SECTIONS.items():

        if not section_exists(
            headings,
            aliases,
        ):

            warnings.append(
                "Documentation may be missing section: "
                f"{section_name}"
            )

    # =====================================================
    # 4. Validate API documentation only when relevant
    # =====================================================

    if project_has_api(
        analyzed_files
    ):

        aliases = OPTIONAL_SECTIONS[
            "API Documentation"
        ]

        if not section_exists(
            headings,
            aliases,
        ):

            warnings.append(
                "Documentation may be missing section: "
                "API Documentation"
            )

    # =====================================================
    # 5. Validate configuration only when relevant
    # =====================================================

    if project_has_configuration(
        analyzed_files
    ):

        aliases = OPTIONAL_SECTIONS[
            "Configuration"
        ]

        if not section_exists(
            headings,
            aliases,
        ):

            warnings.append(
                "Documentation may be missing section: "
                "Configuration"
            )

    # =====================================================
    # 6. Collect actual project files
    # =====================================================

    actual_files = {
        normalize_path(
            file.get(
                "path",
                "",
            )
        )
        for file in analyzed_files
        if file.get("path")
    }

    actual_filenames = {
        path.split("/")[-1]
        for path in actual_files
    }

    # =====================================================
    # 7. Extract documented source files
    # =====================================================

    documented_files = (
        extract_documented_files(
            documentation
        )
    )

    # =====================================================
    # 8. Validate documented files
    # =====================================================

    for documented_file in documented_files:

        normalized_file = normalize_path(
            documented_file
        )

        if not normalized_file.lower().endswith(
            SUPPORTED_EXTENSIONS
        ):
            continue

        filename_only = (
            normalized_file.split("/")[-1]
        )

        # File exists by complete path OR filename
        if (
            normalized_file not in actual_files
            and filename_only not in actual_filenames
        ):

            warnings.append(
                "Documentation references a source file "
                "not found in the analyzed project: "
                f"{documented_file}"
            )

    # =====================================================
    # 9. Extract actual functions
    # =====================================================

    actual_functions = (
        extract_actual_functions(
            analyzed_files
        )
    )

    # =====================================================
    # 10. Check whether actual functions are documented
    # =====================================================

    documentation_lower = (
        documentation.lower()
    )

    for function_name in actual_functions:

        function_pattern = (
            rf"\b{re.escape(function_name.lower())}\b"
        )

        if not re.search(
            function_pattern,
            documentation_lower,
        ):

            warnings.append(
                f"Function '{function_name}' exists "
                "in the source code but was not clearly "
                "documented."
            )

    # =====================================================
    # 11. Extract documented functions
    # =====================================================

    documented_functions = (
        extract_documented_functions(
            documentation
        )
    )

    # =====================================================
    # 12. Detect unknown documented functions
    # =====================================================

    actual_functions_lower = {
        name.lower()
        for name in actual_functions
    }

    common_functions_lower = {
        name.lower()
        for name in COMMON_FUNCTIONS
    }

    common_exceptions_lower = {
        name.lower()
        for name in COMMON_EXCEPTIONS
    }

    for function_name in documented_functions:

        function_lower = (
            function_name.lower()
        )

        # Ignore built-in functions
        if function_lower in common_functions_lower:
            continue

        # Ignore built-in Python exceptions
        if function_lower in common_exceptions_lower:
            continue

        # Ignore actual project functions
        if function_lower in actual_functions_lower:
            continue

        warnings.append(
            "Documentation references function "
            f"'{function_name}', but it was not found "
            "in the analyzed source code."
        )

    # =====================================================
    # 13. Remove duplicate warnings
    # =====================================================

    warnings = list(
        dict.fromkeys(
            warnings
        )
    )

    errors = list(
        dict.fromkeys(
            errors
        )
    )

    # =====================================================
    # 14. Calculate validation status
    # =====================================================

    valid = len(errors) == 0

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "files_checked": len(actual_files),
        "functions_checked": len(actual_functions),
    }