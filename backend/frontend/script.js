async function uploadResume() {
  const fileInput = document.getElementById("resumeFile");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please upload a resume file.");
    return;
  }

  let formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:5000/analyze", {
    method: "POST",
    body: formData
  });

  const result = await response.json();

  if (result.error) {
    document.getElementById("result").innerHTML = `<p style="color:red">${result.error}</p>`;
    return;
  }

  document.getElementById("result").innerHTML = `
    <h3>Analysis Result</h3>
    <p><b>ATS Score:</b> ${result.ats_score}%</p>
    <p><b>Skills Found:</b> ${result.skills_found.join(", ") || "None"}</p>
    <p><b>Resume Length:</b> ${result.resume_length} words</p>
    <p><b>Email(s):</b> ${result.emails.join(", ") || "Not found"}</p>
    <p><b>Phone(s):</b> ${result.phone_numbers.join(", ") || "Not found"}</p>
    <p><b>Suggestions:</b> ${result.suggestions.join(" | ") || "Looks good!"}</p>
  `;
}
