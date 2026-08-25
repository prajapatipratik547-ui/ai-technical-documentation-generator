from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from analyzer import analyze_project, build_codebase_context
from ai_engine import generate_documentation
from validator import validate_documentation


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title="AI Technical Documentation Generator",
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Project Directories
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DOCS_DIR = BASE_DIR / "docs"

DOCS_DIR.mkdir(exist_ok=True)

DOCUMENTATION_FILE = DOCS_DIR / "documentation.md"


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "AI Technical Documentation Generator API is running!"
    }


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# ---------------------------------------------------------
# Analyze Codebase
# ---------------------------------------------------------

@app.post("/analyze")
async def analyze_codebase(file: UploadFile = File(...)):
    """
    Upload a ZIP project, analyze its source files,
    send the codebase to Gemini, generate documentation,
    validate the documentation, and save it as Markdown.
    """

    # -----------------------------------------------------
    # Validate uploaded file
    # -----------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided.",
        )

    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Only ZIP files are supported.",
        )


    # -----------------------------------------------------
    # Temporary project processing
    # -----------------------------------------------------

    with TemporaryDirectory() as temp_dir:

        zip_path = Path(temp_dir) / file.filename

        contents = await file.read()

        zip_path.write_bytes(contents)


        # -------------------------------------------------
        # Step 1: Analyze uploaded project
        # -------------------------------------------------

        try:

            analyzed_files = analyze_project(
                str(zip_path)
            )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=f"Project analysis failed: {str(e)}",
            )


        if not analyzed_files:

            raise HTTPException(
                status_code=400,
                detail="No supported source files found in the ZIP.",
            )


        # -------------------------------------------------
        # Step 2: Build codebase context
        # -------------------------------------------------

        try:

            codebase_context = build_codebase_context(
                analyzed_files
            )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=f"Failed to build codebase context: {str(e)}",
            )


        # -------------------------------------------------
        # Step 3: Generate documentation using Gemini
        # -------------------------------------------------

        try:

            documentation = generate_documentation(
                codebase_context
            )

        except Exception as e:

            error_message = str(e)

            # ---------------------------------------------
            # Gemini quota / rate-limit error
            # ---------------------------------------------

            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
                or "quota" in error_message.lower()
            ):

                raise HTTPException(
                    status_code=429,
                    detail=(
                        "Gemini API quota has been exhausted. "
                        "Please wait for the quota to reset or "
                        "use a Gemini API project with available quota."
                    ),
                )


            # ---------------------------------------------
            # Other Gemini errors
            # ---------------------------------------------

            raise HTTPException(
                status_code=500,
                detail=(
                    "AI documentation generation failed: "
                    + error_message
                ),
            )


    # -----------------------------------------------------
    # Step 4: Validate generated documentation
    # -----------------------------------------------------

    try:

        validation_result = validate_documentation(
            documentation,
            analyzed_files,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Documentation validation failed: {str(e)}",
        )


    # -----------------------------------------------------
    # Step 5: Save documentation
    # -----------------------------------------------------

    try:

        DOCUMENTATION_FILE.write_text(
            documentation,
            encoding="utf-8",
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save documentation: {str(e)}",
        )


    # -----------------------------------------------------
    # Step 6: Return complete response
    # -----------------------------------------------------

    return {
        "filename": file.filename,

        "files_found": len(analyzed_files),

        "documentation_file": "documentation.md",

        "download_endpoint": "/download",

        "validation": validation_result,

        "documentation": documentation,
    }


# ---------------------------------------------------------
# Download Documentation
# ---------------------------------------------------------

@app.get("/download")
def download_documentation():
    """
    Download the latest generated Markdown documentation.
    """

    if not DOCUMENTATION_FILE.exists():

        raise HTTPException(
            status_code=404,
            detail="Documentation has not been generated yet.",
        )

    return FileResponse(
        path=DOCUMENTATION_FILE,
        media_type="text/markdown",
        filename="documentation.md",
    )