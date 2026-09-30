{% extends "base.html" %}


{% block title %}
Jewelry Planner — PocketSmart AI
{% endblock %}


{% block content %}

<main class="container">

    <div class="card">

        <span class="badge">
            Jewelry Planning
        </span>

        <h1>
            Jewelry Budget Planner
        </h1>

        <p class="muted">
            Get occasion and style-aware jewelry
            suggestions. You can optionally upload
            an outfit image.
        </p>


        <form
            id="jewelryForm"
            enctype="multipart/form-data"
        >

            <label for="budget">
                Budget ₹
            </label>

            <input
                id="budget"
                name="budget"
                type="number"
                min="1"
                required
            >


            <label for="occasion">
                Occasion
            </label>

            <input
                id="occasion"
                name="occasion"
                value="wedding"
                required
            >


            <label for="style">
                Style
            </label>

            <select
                id="style"
                name="style"
            >

                <option value="elegant">
                    Elegant
                </option>

                <option value="minimal">
                    Minimal
                </option>

                <option value="traditional">
                    Traditional
                </option>

                <option value="modern">
                    Modern
                </option>

            </select>


            <label for="metal">
                Metal Preference
            </label>

            <select
                id="metal"
                name="metal"
            >

                <option value="any">
                    Any
                </option>

                <option value="gold tone">
                    Gold Tone
                </option>

                <option value="silver tone">
                    Silver Tone
                </option>

                <option value="rose gold tone">
                    Rose Gold Tone
                </option>

            </select>


            <label for="notes">
                Additional Notes
            </label>

            <textarea
                id="notes"
                name="notes"
                placeholder="Example: Prefer lightweight jewelry"
            ></textarea>


            <label for="outfit_image">
                Outfit Image — Optional
            </label>

            <input
                id="outfit_image"
                name="outfit_image"
                type="file"
                accept="image/png,image/jpeg,image/webp"
            >


            <p
                id="message"
                class="error"
            ></p>


            <button type="submit">
                Generate Recommendations
            </button>

        </form>

    </div>


    <div
        id="result"
        class="hidden"
    ></div>

</main>

{% endblock %}


{% block scripts %}

<script>

requireLogin();


const form =
    document.getElementById(
        "jewelryForm"
    );

const message =
    document.getElementById(
        "message"
    );


form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        message.textContent = "";

        try {

            const formData =
                new FormData(form);


            const response =
                await api(
                    "/api/planners/jewelry",
                    {
                        method: "POST",

                        body: formData
                    }
                );


            displayResults(
                response
            );

        } catch (error) {

            message.textContent =
                error.message;

        }

    }
);

</script>

{% endblock %}