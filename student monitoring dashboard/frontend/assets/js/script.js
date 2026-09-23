const submitForm = document.querySelector('form[class="contact-form"]')

async function HandleContactForm(e){
    e.preventDefault();
    console.log("Intializing contact form data for sending to backend !")

    const formData = {
        full_name: document.querySelector("#contact-name").value,
        email: document.querySelector("#contact-email").value,
        category: document.querySelector("#contact-category").value,
        message: document.querySelector("#message").value,
    }
    const response = await fetch("http://127.0.0.1:8000/api/contact-form", {
        method: "POST",
        headers:{
        "Content-Type": "application/json"
    },
    body: JSON.stringify(formData)
});
}

submitForm.addEventListener("submit", HandleContactForm);

