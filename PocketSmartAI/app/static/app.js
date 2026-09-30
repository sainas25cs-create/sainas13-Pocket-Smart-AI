function getToken() {
    return localStorage.getItem("token");
}


function authHeaders() {
    const token = getToken();

    if (!token) {
        return {};
    }

    return {
        Authorization: "Bearer " + token
    };
}


async function api(url, options = {}) {
    options.headers = {
        ...(options.headers || {}),
        ...authHeaders()
    };

    const response = await fetch(
        url,
        options
    );

    const data = await response
        .json()
        .catch(() => ({
            detail: "Invalid server response"
        }));

    if (!response.ok) {
        throw new Error(
            data.detail || "Request failed"
        );
    }

    return data;
}


function requireLogin() {
    if (!getToken()) {
        window.location.href = "/login";
    }
}


function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
}


function formatCurrency(value) {
    return Number(value).toLocaleString(
        "en-IN",
        {
            maximumFractionDigits: 2
        }
    );
}


function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function displayResults(data) {
    const resultContainer =
        document.getElementById("result");

    if (!resultContainer) {
        return;
    }

    resultContainer.classList.remove(
        "hidden"
    );

    const recommendations =
        data.recommendations
            .map(
                item => `
                <div class="recommendation">
                    <h3>
                        ${escapeHtml(item.name)}
                    </h3>

                    <p>
                        <strong>Category:</strong>
                        ${escapeHtml(item.category)}
                    </p>

                    <p>
                        <strong>Estimated budget:</strong>
                        ₹${formatCurrency(
                            item.estimated_price
                        )}
                    </p>

                    <p>
                        <strong>Platform:</strong>
                        ${escapeHtml(item.platform)}
                    </p>

                    <p>
                        ${escapeHtml(item.reason)}
                    </p>

                    <a
                        class="secondary-button"
                        href="${escapeHtml(item.url)}"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Search on
                        ${escapeHtml(item.platform)}
                    </a>
                </div>
                `
            )
            .join("");


    const tips = data.tips
        .map(
            tip =>
                `<li>${escapeHtml(tip)}</li>`
        )
        .join("");


    resultContainer.innerHTML = `
        <div class="card result-card">

            <span class="badge">
                ${escapeHtml(data.source)}
            </span>

            <h2>
                ${escapeHtml(data.summary)}
            </h2>

            <p>
                <strong>Total budget:</strong>
                ₹${formatCurrency(data.budget)}
            </p>

            <h3>Budget allocation</h3>

            <div class="allocation-grid">
                ${Object.entries(
                    data.allocation
                )
                    .map(
                        ([key, value]) => `
                        <div class="allocation">
                            <span>
                                ${escapeHtml(
                                    key
                                )}
                            </span>

                            <strong>
                                ₹${formatCurrency(
                                    value
                                )}
                            </strong>
                        </div>
                        `
                    )
                    .join("")}
            </div>

            <h3>
                Recommendations
            </h3>

            ${recommendations}

            <h3>
                Tips
            </h3>

            <ul>
                ${tips}
            </ul>

        </div>
    `;
}