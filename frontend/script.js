const API_URL = "https://ai-technical-documentation-generator.onrender.com";


/* =========================
   ELEMENTS
========================= */

const zipFile =
    document.getElementById("zipFile");

const uploadArea =
    document.getElementById("uploadArea");

const fileInfo =
    document.getElementById("fileInfo");

const fileName =
    document.getElementById("fileName");

const fileSize =
    document.getElementById("fileSize");

const removeFile =
    document.getElementById("removeFile");

const analyzeButton =
    document.getElementById("analyzeButton");

const loading =
    document.getElementById("loading");

const resultSection =
    document.getElementById("resultSection");

const errorMessage =
    document.getElementById("errorMessage");

const documentation =
    document.getElementById("documentation");

const filesChecked =
    document.getElementById("filesChecked");

const functionsChecked =
    document.getElementById("functionsChecked");

const warningsCount =
    document.getElementById("warningsCount");

const statusBadge =
    document.getElementById("statusBadge");

const validationMessage =
    document.getElementById("validationMessage");

const validationIcon =
    document.getElementById("validationIcon");

const warningsContainer =
    document.getElementById("warningsContainer");

const downloadButton =
    document.getElementById("downloadButton");

const copyButton =
    document.getElementById("copyButton");

const newAnalysisButton =
    document.getElementById("newAnalysisButton");


/* =========================
   FILE SELECTION
========================= */

uploadArea.addEventListener(
    "click",
    () => {
        zipFile.click();
    }
);


zipFile.addEventListener(
    "change",
    () => {

        const file =
            zipFile.files[0];

        if (!file) {
            return;
        }

        handleFile(file);
    }
);


/* =========================
   HANDLE FILE
========================= */

function handleFile(file) {

    if (
        !file.name
            .toLowerCase()
            .endsWith(".zip")
    ) {

        showError(
            "Please select a ZIP file."
        );

        resetFile();

        return;
    }


    fileName.textContent =
        file.name;


    fileSize.textContent =
        `${formatFileSize(file.size)} • Ready for analysis`;


    fileInfo.classList.remove(
        "hidden"
    );


    analyzeButton.disabled =
        false;


    hideError();


    resultSection.classList.add(
        "hidden"
    );
}


/* =========================
   FILE SIZE
========================= */

function formatFileSize(bytes) {

    if (bytes === 0) {
        return "0 Bytes";
    }


    const units = [
        "Bytes",
        "KB",
        "MB",
        "GB"
    ];


    const index =
        Math.floor(
            Math.log(bytes) /
            Math.log(1024)
        );


    return (
        parseFloat(
            (
                bytes /
                Math.pow(
                    1024,
                    index
                )
            ).toFixed(2)
        ) +
        " " +
        units[index]
    );
}


/* =========================
   DRAG AND DROP
========================= */

uploadArea.addEventListener(
    "dragover",
    (event) => {

        event.preventDefault();

        uploadArea.classList.add(
            "dragover"
        );
    }
);


uploadArea.addEventListener(
    "dragleave",
    () => {

        uploadArea.classList.remove(
            "dragover"
        );
    }
);


uploadArea.addEventListener(
    "drop",
    (event) => {

        event.preventDefault();

        uploadArea.classList.remove(
            "dragover"
        );


        const files =
            event.dataTransfer.files;


        if (!files.length) {
            return;
        }


        const file =
            files[0];


        if (
            !file.name
                .toLowerCase()
                .endsWith(".zip")
        ) {

            showError(
                "Please drop a ZIP file."
            );

            return;
        }


        const dataTransfer =
            new DataTransfer();


        dataTransfer.items.add(file);

        zipFile.files =
            dataTransfer.files;


        handleFile(file);
    }
);


/* =========================
   REMOVE FILE
========================= */

removeFile.addEventListener(
    "click",
    () => {
        resetFile();
    }
);


function resetFile() {

    zipFile.value = "";


    fileInfo.classList.add(
        "hidden"
    );


    analyzeButton.disabled =
        true;


    resultSection.classList.add(
        "hidden"
    );


    hideError();
}


/* =========================
   ANALYZE PROJECT
========================= */

analyzeButton.addEventListener(
    "click",
    async () => {

        const file =
            zipFile.files[0];


        if (!file) {

            showError(
                "Please select a ZIP file first."
            );

            return;
        }


        hideError();


        resultSection.classList.add(
            "hidden"
        );


        loading.classList.remove(
            "hidden"
        );


        analyzeButton.disabled =
            true;


        const formData =
            new FormData();


        formData.append(
            "file",
            file
        );


        try {

            const response =
                await fetch(
                    `${API_URL}/analyze`,
                    {
                        method: "POST",
                        body: formData
                    }
                );


            let data;


            try {

                data =
                    await response.json();

            } catch {

                throw new Error(
                    "The server returned an invalid response."
                );
            }


            /* =========================
               GEMINI QUOTA ERROR
            ========================= */

            if (response.status === 429) {

                throw new Error(
                    data.detail ||
                    "Gemini API quota has been exhausted. Please wait for the quota to reset and try again."
                );
            }


            /* =========================
               OTHER SERVER ERRORS
            ========================= */

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Failed to analyze the project."
                );
            }


            /* =========================
               SUCCESS
            ========================= */

            displayResults(data);


        } catch (error) {

            console.error(
                "Analysis error:",
                error
            );


            if (
                error instanceof TypeError
            ) {

                showError(
                    "Unable to connect to the backend server. Make sure FastAPI is running on https://ai-technical-documentation-generator.onrender.com."
                );

            } else {

                showError(
                    error.message ||
                    "Something went wrong while analyzing the project."
                );
            }


        } finally {

            loading.classList.add(
                "hidden"
            );


            analyzeButton.disabled =
                false;
        }
    }
);


/* =========================
   DISPLAY RESULTS
========================= */

function displayResults(data) {

    resultSection.classList.remove(
        "hidden"
    );


    /* =========================
       MARKDOWN DOCUMENTATION
    ========================= */

    const markdown =
        data.documentation ||
        "No documentation generated.";


    if (
        typeof marked !== "undefined"
    ) {

        const renderedMarkdown =
            marked.parse(markdown);


        /*
         * Use DOMPurify when available.
         * This prevents unsafe HTML from being
         * inserted into the page.
         */

        if (
            typeof DOMPurify !== "undefined"
        ) {

            documentation.innerHTML =
                DOMPurify.sanitize(
                    renderedMarkdown
                );

        } else {

            documentation.innerHTML =
                renderedMarkdown;
        }

    } else {

        /*
         * Fallback if the Markdown library
         * cannot be loaded.
         */

        documentation.textContent =
            markdown;
    }


    /* =========================
       VALIDATION
    ========================= */

    const validation =
        data.validation;


    if (validation) {

        filesChecked.textContent =
            validation.files_checked ??
            data.files_found ??
            0;


        functionsChecked.textContent =
            validation.functions_checked ??
            0;


        const warnings =
            validation.warnings ||
            [];


        warningsCount.textContent =
            warnings.length;


        /* =========================
           VALID
        ========================= */

        if (validation.valid) {

            statusBadge.textContent =
                "✓ Valid";


            statusBadge.classList.remove(
                "invalid"
            );


            validationIcon.textContent =
                "✓";


            validationMessage.textContent =
                "Documentation passed validation.";


            validationIcon.style.background =
                "#dcfce7";


            validationIcon.style.color =
                "#15803d";

        }


        /* =========================
           INVALID
        ========================= */

        else {

            statusBadge.textContent =
                "Needs Review";


            statusBadge.classList.add(
                "invalid"
            );


            validationIcon.textContent =
                "!";


            validationMessage.textContent =
                "Documentation requires review.";


            validationIcon.style.background =
                "#fee2e2";


            validationIcon.style.color =
                "#b42318";
        }


        /* =========================
           WARNINGS
        ========================= */

        warningsContainer.innerHTML =
            "";


        warnings.forEach(
            (warning) => {

                const warningElement =
                    document.createElement(
                        "div"
                    );


                warningElement.className =
                    "warning";


                warningElement.textContent =
                    `⚠️ ${warning}`;


                warningsContainer.appendChild(
                    warningElement
                );
            }
        );

    } else {

        filesChecked.textContent =
            data.files_found ||
            0;


        functionsChecked.textContent =
            "—";


        warningsCount.textContent =
            "—";
    }


    /* =========================
       DOWNLOAD
    ========================= */

    downloadButton.href =
        `${API_URL}/download`;


    /* =========================
       SUMMARY
    ========================= */

    const fileCount =
        filesChecked.textContent;


    const functionCount =
        functionsChecked.textContent;


    document.getElementById(
        "resultSummary"
    ).textContent =
        `${fileCount} files analyzed • ${functionCount} functions detected • Documentation generated successfully.`;


    /* =========================
       SCROLL TO RESULTS
    ========================= */

    resultSection.scrollIntoView({
        behavior: "smooth"
    });
}


/* =========================
   COPY DOCUMENTATION
========================= */

copyButton.addEventListener(
    "click",
    async () => {

        /*
         * Read the original Markdown
         * from the rendered documentation.
         */

        const markdownText =
            documentation.innerText ||
            documentation.textContent;


        if (!markdownText) {
            return;
        }


        try {

            await navigator.clipboard.writeText(
                markdownText
            );


            copyButton.textContent =
                "✓ Copied";


            setTimeout(
                () => {

                    copyButton.textContent =
                        "📋 Copy";

                },
                1800
            );


        } catch (error) {

            console.error(
                "Copy error:",
                error
            );


            showError(
                "Unable to copy documentation."
            );
        }
    }
);


/* =========================
   NEW ANALYSIS
========================= */

newAnalysisButton.addEventListener(
    "click",
    () => {

        resetFile();


        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }
);


/* =========================
   ERROR
========================= */

function showError(message) {

    errorMessage.textContent =
        `❌ ${message}`;


    errorMessage.classList.remove(
        "hidden"
    );
}


function hideError() {

    errorMessage.classList.add(
        "hidden"
    );
}