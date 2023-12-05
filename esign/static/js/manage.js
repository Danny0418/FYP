 // Load and render the first page of the PDF document
 const pdfUrl = '{{ document.pdf_file.url }}'; // Replace with the actual URL or path of your PDF document
 const canvas = document.getElementById('pdfCanvas');
 const context = canvas.getContext('2d');
 const parentDiv = canvas.parentElement;

 pdfjsLib.getDocument(pdfUrl).promise.then(function (pdf) {
     pdf.getPage(1).then(function (page) {
         const viewport = page.getViewport({ scale: 1 });
         canvas.height = viewport.height;
         canvas.width = parentDiv.clientWidth;
         const scale = canvas.width / viewport.width;

         const renderContext = {
             canvasContext: context,
             viewport: page.getViewport({ scale: scale }),
         };
         page.render(renderContext);
     });
 }).catch(function (error) {
     console.error('Error loading PDF:', error);
 });

 $(document).ready(function () {
    $(".edit-icon").click(function () {
        $("#editableTitle").hide();
        $("#editTitleInput").val($("#editableTitle b").text()).show().focus();
    });

    var isEventProcessed = false; // Flag to track event processing

    $("#editTitleInput").on('blur keypress', function (event) {
        if (event.type === 'blur' || (event.type === 'keypress' && event.which === 13)) {
            if (!isEventProcessed) { // Check if the event has already been processed
                isEventProcessed = true; // Set the flag to true to indicate event processing
                var newTitle = $(this).val();
                if (newTitle.trim() !== "") {
                    $("#editableTitle b").text(newTitle);

                    // AJAX call to update the document title in the database
                    var documentId = $('#pdfContainer').data('document-id'); // Replace with the actual document ID
                    
                    $.ajax({
                        type: 'POST',
                        url: `/esign/update_document_title/${documentId}/`,
                        data: {
                            new_title: newTitle,
                            csrfmiddlewaretoken: '{{ csrf_token }}', // Include CSRF token
                        },
                        dataType: 'json',
                        success: function (response) {
                            if (response.success) {
                                // Display a success message to the user
                    var successMessage = 'Document title updated successfully! '

                    // Show Bootstrap success modal
                    var successModal = $('<div class="modal fade" id="successModal" tabindex="-1" role="dialog" aria-labelledby="successModalLabel" aria-hidden="true" data-backdrop="static">' +
                        '<div class="modal-dialog" role="document">' +
                        '<div class="modal-content bg-success">' + // Set the background color to light green
                        '<div class="modal-header">' +
                        '<h5 class="modal-title text-white" id="successModalLabel">Success</h5>' +
                        '</div>' +
                        '<div class="modal-body text-white">' + // Set the text color to white
                        successMessage +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>');

                    $('body').append(successModal);
                    $('#successModal').modal('show');

                    // Close the success modal after 5 seconds
                    setTimeout(function () {
                        $('#successModal').modal('hide');
                        successModal.remove();
                    }, 5000);
                            } else {
                                // Handle failure if needed
                                alert('Error updating document title!');
                            }
                        },
                        error: function (xhr, errmsg, err) {
                            // Handle error if needed
                            alert('Error updating document title!');
                        },
                        complete: function () {
                            isEventProcessed = false; // Reset the flag after completing the AJAX call
                        }
                    });
                }
                $(this).hide();
                $("#editableTitle").show();
            }
        }
    });
});

$(document).ready(function () {
    var dateCheck = '{{ docDue }}';
    var selectedDate;
    if (dateCheck == "1900-01-01T00:00") {
        $('#expDate').val('');;
    }

    // Listen for changes in the datetime-local input field
    $('#expDate').on('change', function () {
        // Get the selected datetime value
        selectedDate = $(this).val();


        // Check if the selected date is not empty
        if (selectedDate) {
            // Show the Bootstrap confirmation modal
            $('#dateModal').modal('show');
        }
    });

    function formatDateTime(datetimeString) {
        const date = new Date(datetimeString);

        // Extract date components
        const day = date.getDate().toString().padStart(2, '0');
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const year = date.getFullYear();

        // Get hours and minutes
        let hours = date.getHours();
        const minutes = date.getMinutes().toString().padStart(2, '0');

        // Convert hours to 12-hour format and determine AM or PM
        const meridiem = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12 || 12; // Convert hours from 24-hour to 12-hour format

        // Format the datetime string
        const formattedDateTime = `${day}/${month}/${year} ${hours}:${minutes} ${meridiem}`;

        return formattedDateTime;
    }

    // Handle confirmation or cancellation within the modal if needed
    $('#dateConfirmAction').on('click', function () {
        // Get the selected datetime value
        var minExpDate = new Date(); // Get the minimum expiry time
        var formattedMinDate = formatDateTime(minExpDate);
        var selectedDateObject = new Date(selectedDate);


        if (selectedDateObject < minExpDate) {
            // Display an error message or take appropriate action
            alert('Expiry date could not be set before: ' + formattedMinDate);
            return; // Prevent further execution of the assignment logic
        }

        $.ajax({
            url: '/esign/update_due/', // Replace with your server-side endpoint URL
            method: 'POST',
            data: {
                new_due: selectedDate,
                document_id: '{{ docID }}',
                csrfmiddlewaretoken: '{{ csrf_token }}', // Include CSRF token
            },
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    dateCheck = $('#expDate').val();

                    // Hide the modal once the action is completed
                    $('#dateModal').modal('hide');

                    var formattedDateTime = formatDateTime(selectedDate);

                    // Display a success message to the user
                    var successMessage = 'Expiry date successfully updated to ' + formattedDateTime + '!';

                    // Show Bootstrap success modal
                    var successModal = $('<div class="modal fade" id="successModal" tabindex="-1" role="dialog" aria-labelledby="successModalLabel" aria-hidden="true" data-backdrop="static">' +
                        '<div class="modal-dialog" role="document">' +
                        '<div class="modal-content bg-success">' + // Set the background color to light green
                        '<div class="modal-header">' +
                        '<h5 class="modal-title text-white" id="successModalLabel">Success</h5>' +
                        '</div>' +
                        '<div class="modal-body text-white">' + // Set the text color to white
                        successMessage +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>');

                    $('body').append(successModal);
                    $('#successModal').modal('show');

                    // Close the success modal after 5 seconds
                    setTimeout(function () {
                        $('#successModal').modal('hide');
                        successModal.remove();
                    }, 5000);
                } else {
                    // Handle failure if needed
                    alert('Error updating expiry date!');
                }
            },
            error: function (xhr, errmsg, err) {
                // Handle error if needed
                alert('Error updating expiry date!');
            }
        });
    });
    // Handle cancellation within the modal if needed
    $('#dateCancelAction, #dateCloseAction').on('click', function () {
        // set expiry date back to original
        if (dateCheck == "1900-01-01T00:00") {
            $('#expDate').val('');;
        } else {
            $('#expDate').val(dateCheck);
        }

        // Hide the modal upon cancellation
        $('#dateModal').modal('hide');
    });

    $('#compSelect').select2({
        placeholder: 'Search for a company',
        allowClear: true // Optional - adds a clear button
    });

    // Event listener for company selection change
    $('#compSelect').on('change', function () {
        var selectedCompany = $(this).val();
        // console.log(typeof (selectedCompany));

        // Make an AJAX request to fetch associated names and emails for the selected company
        $.ajax({
            url: '/esign/get_names_emails/', // Replace with your server-side endpoint URL
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}' // Include the CSRF token here
            },
            data: {
                company_id: selectedCompany
            },
            traditional: true,
            success: function (response) {
                // Assuming the response contains options for names and emails
                var names = response.names;

                // Clear existing options
                $('#nameSelect').empty();
                //   $('#mailSelect').empty();

                // Populate name options
                names.forEach(function (name) {
                    $('#nameSelect').append($('<option>', {
                        value: name.value,
                        text: name.text
                    }));
                });

                // Trigger change event to update Select2 dropdown UI
                $('#nameSelect').trigger('change');
            },
            error: function (xhr, status, error) {
                console.error('Error fetching data:', error);
            }
        });
    });

    $('#nameSelect').select2({
        placeholder: 'Search for a name',
        allowClear: true // Optional - adds a clear button
    });

    var signerNames = []; // Array to store signer names

    // Function to update the signer list select element
    function updateSignerList(selectedID) {

        signerNames.push(selectedID); // Add selected name to the array
    }


    function getSignerList() {
        // loop through the existed signer list option and store the names in an array
        $('#signerListSelect option').each(function () {
            signerNames.push($(this).val());
        });
        console.log(signerNames);
    }
    getSignerList();

    // Retrieve selected values for organization, name, and role
    var selectedOrganization, selectedID, selectedName, selectedRole;

    // Assuming the assign button has an ID of 'assignButton'
    $('#assignButton').on('click', function () {
        // Retrieve selected values for organization, name, and role
        selectedOrganization = $('#compSelect').find('option:selected').text();
        selectedID = $('#nameSelect').val();
        selectedName = $('#nameSelect').find('option:selected').text();
        selectedRole = $('#roleSelect').find('option:selected').text();

        console.log(signerNames);
        console.log(selectedID);

        var selectedExpDate = $('#expDate').val(); // Get the value of the selected expiry time
        var minExpDate = $('#expDate').attr('min'); // Get the minimum expiry time
        var formattedMinDate = formatDateTime(minExpDate);


        if (selectedExpDate == "") {
            // Display an error message or take appropriate action
            alert('Please insert the expiry date before assigning signers.');
            return; // Prevent further execution of the assignment logic
        }

        if (selectedExpDate < minExpDate) {
            // Display an error message or take appropriate action
            alert('Expiry date could not be set before: ' + formattedMinDate);
            return; // Prevent further execution of the assignment logic
        }

        if (selectedRole == "Search for a role") {
            // Display an error message or take appropriate action
            alert('Please select a role before assigning signers.');
            return; // Prevent further execution of the assignment logic
        }

        // Check if all necessary fields are selected
        if (selectedOrganization && selectedID && selectedRole) {

            $('#confirmationModal').modal('show');
        } else {
            // Display an error message if all necessary fields are not selected
            alert('Please select organization, name, and role.');
        }
    });

    // Listen for confirmation within the modal
    $('#confirmAction').on('click', function () {

        // Create a string to represent the signer
        var signerInfo = selectedOrganization + ' (' + selectedName + ') ' + '(' + selectedRole + ')';
        var check = 0;
        if (signerNames.includes(selectedID[0])) {
            check = 1;
        }

        var role = $('#roleSelect').val();
        console.log(selectedRole);

        if (check === 1) {
            alert('Signer already exists in the list!');
        } else {
            $.ajax({
                url: '/esign/update_permission/',
                method: 'POST',
                data: {
                    selectedID: selectedID[0],
                    selectedRole: role,
                    document_id: '{{ docID }}',
                    csrfmiddlewaretoken: '{{ csrf_token }}', // Include CSRF token
                },
                dataType: 'json',
                success: function (response) {
                    if (response.success) {

                        // Hide the modal once the action is completed
                        $('#confirmationModal').modal('hide');

                        // Display a success message to the user
                        var successMessage = 'Signer list updated successfully! '

                        // Show Bootstrap success modal
                        var successModal = $('<div class="modal fade" id="successModal" tabindex="-1" role="dialog" aria-labelledby="successModalLabel" aria-hidden="true" data-backdrop="static">' +
                            '<div class="modal-dialog" role="document">' +
                            '<div class="modal-content bg-success">' + // Set the background color to light green
                            '<div class="modal-header">' +
                            '<h5 class="modal-title text-white" id="successModalLabel">Success</h5>' +
                            '</div>' +
                            '<div class="modal-body text-white">' + // Set the text color to white
                            successMessage +
                            '</div>' +
                            '</div>' +
                            '</div>' +
                            '</div>');

                        $('body').append(successModal);
                        $('#successModal').modal('show');

                        // Close the success modal after 5 seconds
                        setTimeout(function () {
                            $('#successModal').modal('hide');
                            successModal.remove();
                        }, 5000);

                        // Add the signer to the signer list select element
                        $('#signerListSelect').append($('<option>', {
                            value: selectedID,
                            text: signerInfo
                        }));
                        updateSignerList(selectedID);
                    } else {
                        // Handle failure if needed
                        alert('Error updating signer list!');
                    }
                },
                error: function (xhr, errmsg, err) {
                    // Handle error if needed
                    alert('Error updating signer list!');
                }
            });
        }
        // clear signerNames array
        signerNames = [];
        getSignerList();
    });
});