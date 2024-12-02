async function validateVersion() {
  const version = document.getElementById("version").value.trim();
  const resultDiv = document.getElementById("result");

  if (!version) {
    resultDiv.textContent = "Please enter a version number.";
    resultDiv.className = "result invalid";
    return;
  }

  try {
    const response = await fetch("/validate", {
      method: "POST",
      body: version,
    });

    if (response.ok) {
      const data = await response.json();
      resultDiv.textContent = `"${data.version}" is a valid SemVer.`;
      resultDiv.className = "result valid";
    } else {
      const data = await response.json();
      resultDiv.textContent = `"${data.version}" is not a valid SemVer.`;
      resultDiv.className = "result invalid";
    }
  } catch (error) {
    resultDiv.textContent = "An error occurred. Please try again.";
    resultDiv.className = "result invalid";
    console.error(error);
  }
}

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function () {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight) {
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}
