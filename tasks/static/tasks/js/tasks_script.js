document.addEventListener('DOMContentLoaded', function() {
    // Function to mark a task as completed via AJAX
    function markCompleted(task_id) {
        $.ajax({
            type: "POST",
            url: `/tasks/mark-completed/${task_id}/`,
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}', // Include the CSRF token
            },
            success: function(data) {
                // Handle success (e.g., update the UI)
                alert(data.message);
            },
            error: function(xhr, status, error) {
                // Handle errors if needed
                console.error(error);
            },
        });
    }

    // Function to mark a task as postponed via AJAX
    function markPostponed(task_id) {
        $.ajax({
            type: "POST",
            url: `/tasks/mark-postponed/${task_id}/`,
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}', // Include the CSRF token
            },
            success: function(data) {
                // Handle success (e.g., update the UI)
                alert(data.message);
            },
            error: function(xhr, status, error) {
                // Handle errors if needed
                console.error(error);
            },
        });
    }
});