// upload.js — handles CSV upload to Flask backend

document.addEventListener("DOMContentLoaded", () => {
  const submitButton = document.getElementById("submit_file");
  const fileInput = document.getElementById("csv_file");
  const status = document.getElementById("status");

  submitButton.addEventListener("click", async () => {
    // 1️⃣ Check if a file is selected
    if (!fileInput.files.length) {
      status.textContent = "⚠️ Please select a CSV file first.";
      return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file); // 👈 'file' key must match Flask route expectation

    status.textContent = "⏳ Uploading and processing...";

    try {
      // 2️⃣ Send file to Flask
      const response = await fetch("http://localhost:5000/upload_csv", {
        method: "POST",
        body: formData
      });

      // 3️⃣ Parse Flask response
      const result = await response.json();

      if (response.ok) {
        status.textContent = `✅ ${result.message}`;
        status.style.color = "green";
      } else {
        status.textContent = `❌ Error: ${result.error || "Unknown error"}`;
        status.style.color = "red";
      }

    } catch (error) {
      status.textContent = `❌ Request failed: ${error.message}`;
      status.style.color = "red";
    }
  });
});
