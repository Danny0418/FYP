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