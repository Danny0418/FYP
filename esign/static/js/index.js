// Get the modal
const modal = document.getElementById("uploadModal");
const errorMessage = document.getElementById("errorMessage");

// Get the button that opens the modal
const createButton = document.getElementById("createButton");
const createDocumentBtn = document.getElementById("createDocumentBtn");

// When the user clicks the button, open the modal
createButton.addEventListener("click", function () {
    modal.style.display = "block";
});

// When the user clicks on the close button, close the modal
modal.querySelector(".close").addEventListener("click", function () {
    modal.style.display = "none";
});

// Simulate file upload process
document.getElementById("fileInput").addEventListener("change", function () {
    const progressBar = document.getElementById("uploadProgress");
    const uploadMessage = document.getElementById("uploadMessage");
    const successMessage = document.getElementById("successMessage");

    const file = this.files[0];
    if (file) {
        if (file.type === "application/pdf") {
            errorMessage.style.display = "none";
            // Continue with upload logic here
            // Simulate upload progress
            let progress = 0;
            const interval = setInterval(function () {
                progress += 10;
                if (progress <= 100) {
                    progressBar.value = progress;
                } else {
                    clearInterval(interval);
                    // Simulate successful upload with a delay
                    setTimeout(function () {
                        successMessage.style.display = "block";
                        createDocumentBtn.style.display = "block";
                        // Display the first page of the PDF
                        renderPDF(file);


                        setTimeout(function () {
                            successMessage.style.display = "none";
                        }, 5000); // Hide success message after 3 seconds
                    }, 2000);
                    setTimeout(function () {
                        // Display PDF details after delay
                        uploadMessage.innerText = `Title: ${file.name}`;
                        // Add logic to display PDF preview and create document button here
                    }, 2000); // 2 seconds delay
                }
            }, 500); // 0.5 seconds interval
        } else {
            errorMessage.style.display = "block";
        }
    }
});

// Render the PDF using PDF.js
function renderPDF(file) {
    const fileReader = new FileReader();
    fileReader.onload = function (event) {
        const pdfData = new Uint8Array(event.target.result);

        // Use PDF.js to render the PDF
        pdfjsLib.getDocument({ data: pdfData }).promise.then(function (pdf) {
            // Render the first page
            pdf.getPage(1).then(function (page) {
                const canvas = document.getElementById("pdfCanvas");
                const context = canvas.getContext("2d");
                const viewport = page.getViewport({ scale: 1.5 });

                canvas.width = viewport.width;
                canvas.height = viewport.height;

                page.render({
                    canvasContext: context,
                    viewport: viewport
                });
            });
        });
    };
    fileReader.readAsArrayBuffer(file);
}

// Function to get the CSRF token from the cookie
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
    return cookieValue;
}

// Use the CSRF token in AJAX requests
const csrftoken = getCSRFToken();

// Event listener for "Create Document" button click
createDocumentBtn.addEventListener("click", function () {
    // Send the PDF file data to Django for saving
    const file = document.getElementById("fileInput").files[0];
    const formData = new FormData();
    formData.append('pdf_file', file);

    fetch('/esign/save_pdf_to_db/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken  // Add the CSRF token to the request headers
        },
        body: formData
    })
        .then(response => {
            if (response.ok) {
                return response.json(); // Extract JSON data on success
            } else {
                throw new Error('File creation failed');
            }
        })
        .then(data => {
            const newURL = data.newURL; // Assuming the JSON response contains the newest primary key
            if (newURL) {
                window.location.href = `/esign/management/${newURL}/`; // Redirect with newest primary key
            } else {
                throw new Error('Primary key not found');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to create document');
        });
});

function searchTable() {
    // Get the search term
    const searchTerm = document.getElementById('searchBar').value.toLowerCase();

    // Get the file table and its rows
    const fileTable = document.getElementById('fileTable');
    const rows = fileTable.getElementsByTagName('tr');

    // Loop through the rows and hide those that don't match the search term
    for (let i = 0; i < rows.length; i++) {
        const titleCell = rows[i].getElementsByTagName('td')[0];
        if (titleCell) {
            const titleText = titleCell.textContent.toLowerCase();
            if (titleText.includes(searchTerm)) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }
    }
}

//Show document details
function showDocumentDetails(clickedRow, fileId) {
    const documentDetails = document.getElementById('documentDetails');
    const documentTitles = document.getElementById('documentTitles');
    const createdDate = document.getElementById('createdDate');
    const dueDate = document.getElementById('dueDate');
    const username = document.getElementById('username');
    const email = document.getElementById('email');

    const assignedUsersListElement = document.getElementById('assignedUsersList');

    documentDetails.style.display = 'block';

    const xhr = new XMLHttpRequest();
    xhr.open('GET', `/esign/get_document_details/?doc_id=${fileId}`, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const response = JSON.parse(xhr.responseText);
            console.log('File details element:', response);

            const { document, assigned_users } = response;

            documentTitles.textContent = `${document.title}`;
            createdDate.textContent = `${document.created_date}`;
            dueDate.textContent = `${document.due_date}`;
            username.textContent = `${assigned_users.map(user => user.username).join(', ')}`;
            email.textContent = `${assigned_users.map(user => user.email).join(', ')}`;


            assignedUsersListElement.innerHTML = ''; // Clear previous content

            assigned_users.forEach(user => {
                const listItem = document.createElement('li');
                listItem.textContent = `UserID: ${user.userID}, Username: ${user.username}, Email: ${user.email}, Position: ${user.position}`;
                assignedUsersListElement.appendChild(listItem);
            });
        } else if (xhr.readyState == 4 && xhr.status != 200) {
            console.log('Error fetching file details', xhr.status, xhr.statusText);
        }
    };
    xhr.send();
}