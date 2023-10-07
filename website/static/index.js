function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


const button = document.querySelector('.navbar-toggler');
const navLinks = document.querySelector('.collapse.navbar-collapse');
button.addEventListener('click', () => {
  navLinks.classList.toggle('hide');
});

// Function to take the prompt and fetch the output from the /generate endpoint
document.getElementById('loading-spinner').style.display = 'none';
document.getElementById('generated-content').style.display = 'block';
const populate =  async () => {
  let prompt = document.querySelector('textarea').value;

  // Show the loading spinner and hide the generated content


  let response = await fetch('/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ prompt: prompt })
  });

  // Hide the loading spinner and display the generated content

  document.getElementById('loading-spinner').style.display = 'none';
  // Set the content
  document.getElementById('generated-content').innerHTML = await response.text();
}

const submitBtn = document.querySelector('#submitBtn');
submitBtn.addEventListener('click', () => {
  document.getElementById('loading-spinner').style.display = 'block';
  document.getElementById('generated-content').style.display = 'block';
  populate();
});