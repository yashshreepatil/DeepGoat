function uploadImage() {
    let imageInput = document.getElementById("imageInput");
    let resultText = document.getElementById("result");
    let previewImage = document.getElementById("preview");

    if (imageInput.files.length === 0) {
        resultText.style.display = "block";
        resultText.innerHTML = "⚠️ Please select an image!";
        resultText.className = "alert alert-warning";
        return;
    }

    let formData = new FormData();
    formData.append("file", imageInput.files[0]);

    // Show image preview
    let reader = new FileReader();
    reader.onload = function (e) {
        previewImage.src = e.target.result;
        previewImage.style.display = "block";
    };
    reader.readAsDataURL(imageInput.files[0]);

    // Send image to backend
    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        resultText.style.display = "block";
        resultText.innerHTML = `✅ Prediction: <strong>${data.prediction}</strong><br>💊 Medicine: ${data.medicine}`;
        resultText.className = "alert alert-success";
    })
    .catch(error => {
        resultText.style.display = "block";
        resultText.innerHTML = "❌ Error: " + error;
        resultText.className = "alert alert-danger";
    });
}
