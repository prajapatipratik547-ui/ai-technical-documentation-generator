import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def generate_documentation(codebase_context: str) -> str:
    """
    Generate professional technical documentation
    from the analyzed project source code.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    client = genai.Client(
        api_key=api_key
    )

    prompt_parts = [
        "You are a senior software architect and "
        "professional technical documentation writer.",

        "Analyze the provided software project and "
        "generate accurate, professional, developer-friendly "
        "technical documentation.",

        "The provided source code is the ONLY source of truth.",

        "==================================================",
        "STRICT SOURCE-OF-TRUTH RULES",
        "==================================================",

        "1. Analyze ALL provided source files.",

        "2. Every factual statement must be supported "
        "by the provided source code.",

        "3. NEVER invent files, folders, functions, classes, "
        "APIs, dependencies, databases, services, features, "
        "commands, technologies, configuration files, or "
        "runtime behavior.",

        "4. NEVER mention a filename unless that exact "
        "filename appears in the provided project source.",

        "5. NEVER assume conventional project files exist. "
        "For example, do not mention setup.py, pyproject.toml, "
        "package.json, README.md, Dockerfile, .gitignore, "
        "docker-compose.yml, Makefile, or similar files unless "
        "they are explicitly present in the provided source.",

        "6. Before mentioning any file, verify that the exact "
        "filename exists in the supplied project source.",

        "7. Do not infer project structure from common conventions. "
        "Use only the actual structure provided.",

        "8. Do not infer technologies from filenames alone. "
        "Only identify a technology when there is evidence "
        "in the provided source.",

        "9. If information cannot be determined from the "
        "source code, write exactly: "
        "'Not specified in the provided source code.'",

        "10. Identify relationships between files using "
        "evidence such as imports, function calls, routes, "
        "class usage, or component usage.",

        "11. Clearly distinguish existing functionality "
        "from recommended improvements.",

        "12. NEVER describe recommendations as existing "
        "features.",

        "13. Never expose API keys, passwords, tokens, "
        "credentials, or other secrets.",

        "14. Do not reproduce large amounts of source code.",

        "15. Do not claim that something was tested unless "
        "the provided source code contains explicit evidence "
        "of testing.",

        "16. Do not invent installation or execution commands.",

        "17. Do not invent API endpoints. Only document "
        "endpoints explicitly supported by the provided code.",

        "18. Do not invent environment variables. Only document "
        "variables explicitly referenced by the provided code.",

        "19. Do not invent dependencies. Only document packages "
        "supported by imports, dependency files, or other "
        "explicit evidence in the provided source.",

        "20. Do not assume a database, cloud service, external "
        "API, authentication system, or deployment platform "
        "exists unless supported by the source code.",

        "21. If the project does not contain an HTTP API, clearly "
        "state that no HTTP API is exposed by the provided "
        "source code.",

        "22. If a requested documentation section cannot be "
        "supported by the source code, state that the information "
        "is not specified rather than guessing.",

        "==================================================",
        "FILE VERIFICATION RULE",
        "==================================================",

        "Before producing the final documentation, mentally "
        "create a list of every actual file provided in the "
        "PROJECT SOURCE CODE.",

        "Every filename mentioned in the final documentation "
        "must match one of those actual filenames exactly.",

        "If a filename is not present in the provided project, "
        "DO NOT mention it.",

        "Do not add conventional files simply because they "
        "would normally exist in a similar project.",

        "==================================================",
        "DOCUMENTATION STRUCTURE",
        "==================================================",

        "# Technical Documentation: <Project Name>",

        "## 1. Project Overview",
        "Explain what the project does, its purpose, and "
        "the type of application.",

        "## 2. Purpose and Main Features",
        "Describe the features actually implemented.",

        "## 3. Technology Stack",
        "Identify verified programming languages, frameworks, "
        "libraries, databases, APIs, external services, "
        "and runtime technologies.",

        "## 4. Project Architecture",
        "Explain major components, their responsibilities, "
        "relationships between files, execution flow, "
        "and important dependencies.",

        "## 5. Directory / File Structure",
        "Show the ACTUAL project structure and explain the "
        "responsibility of important files.",

        "Do not invent files or folders.",

        "## 6. Important Components",
        "Document important functions, classes, modules, "
        "routes, services, and components.",

        "For important functions explain their purpose, "
        "inputs, outputs, and important behavior.",

        "## 7. API Documentation",
        "If HTTP APIs exist, document method, endpoint, "
        "purpose, parameters, request body, response, "
        "and important errors.",

        "If there is no HTTP API, clearly state that no HTTP "
        "API is exposed by the provided source code.",

        "## 8. Data Flow",
        "Explain how data moves through the application. "
        "Only describe flows supported by the source code.",

        "## 9. Installation Instructions",
        "Provide installation instructions only when they "
        "can be determined from the project.",

        "Do not invent commands.",

        "## 10. Configuration",
        "Document actual configuration files, environment "
        "variables, constants, ports, and runtime settings.",

        "Never expose secret values.",

        "## 11. How to Run the Project",
        "Explain the actual execution process when it can "
        "be determined from the source code.",

        "Do not invent commands.",

        "## 12. Usage Examples",
        "Provide realistic examples based only on implemented "
        "functionality.",

        "Do not invent functionality.",

        "## 13. Dependencies",
        "List important dependencies and explain their purpose. "
        "Distinguish standard library, external packages, "
        "and project-local modules.",

        "## 14. Design Decisions and Implementation Notes",
        "Explain important implementation choices visible "
        "in the source code, including modularization, "
        "error handling, validation, configuration, "
        "security, and code organization.",

        "## 15. Limitations",
        "Identify limitations directly visible in the "
        "current implementation.",

        "Do not present speculation as fact.",

        "## 16. Potential Improvements",
        "Provide practical recommendations for improving "
        "the existing implementation.",

        "Clearly label these as recommendations.",

        "## 17. Summary",
        "Summarize the project purpose, major components, "
        "architecture, execution flow, and current state.",

        "==================================================",
        "MARKDOWN REQUIREMENTS",
        "==================================================",

        "Return ONLY Markdown documentation.",

        "Use clean Markdown headings.",

        "Use bullet points and tables when useful.",

        "Use code blocks for directory structures and "
        "short commands when appropriate.",

        "Keep explanations concise and technically accurate.",

        "Avoid unnecessary repetition.",

        "Do not invent information.",

        "Do not expose secrets.",

        "Make the documentation suitable for a GitHub "
        "repository or professional developer documentation.",

        "==================================================",
        "FINAL VERIFICATION",
        "==================================================",

        "Before responding, perform a final consistency check.",

        "Verify that EVERY filename mentioned in the "
        "documentation exists in the provided project.",

        "Verify that EVERY function, class, dependency, "
        "API endpoint, environment variable, and command "
        "mentioned is supported by the provided source.",

        "Remove any unsupported filename or claim.",

        "If something cannot be verified, do not guess.",

        "Use only evidence from the supplied project.",

        "Now generate the documentation.",
    ]

    prompt = "\n\n".join(prompt_parts)

    prompt += (
        "\n\n"
        "==================================================\n"
        "PROJECT SOURCE CODE\n"
        "==================================================\n\n"
    )

    prompt += codebase_context

    prompt += (
        "\n\n"
        "==================================================\n"
        "END PROJECT SOURCE CODE\n"
        "==================================================\n"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text.strip()