/* reminderSection */
$(document).on('click', '#reminderSection #reminderToggle', function() {
    let focus = $('#reminderForm');
    let btnFocus = $(this);

    focus.toggleClass('expand');
    focus.one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function () {
        if(focus.hasClass('expand')) {
            btnFocus.addClass('active');
            btnFocus.text('Hide New Medication Reminder');
        }
        else {
            btnFocus.removeClass('active');
            btnFocus.text('New Medication Reminder');
        }
    });
});

/* appointmentSection */
$(document).on('click', '#appointmentSection #appointmentToggle', function() {
    let focus = $('#appointmentForm');
    let btnFocus = $(this);

    focus.toggleClass('expand');
    focus.one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function () {
        if(focus.hasClass('expand')) {
            btnFocus.addClass('active');
            btnFocus.text('Hide New Medical Appointment');
        }
        else {
            btnFocus.removeClass('active');
            btnFocus.text('New Medical Appointment');
        }
    });
});

/* historySection */
$(document).on('click', '#historySection #historyToggle', function() {
    let focus = $('#historyForm');
    let btnFocus = $(this);

    focus.toggleClass('expand');
    focus.one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function () {
        if(focus.hasClass('expand')) {
            btnFocus.addClass('active');
            btnFocus.text('Hide New Medical History');
        }
        else {
            btnFocus.removeClass('active');
            btnFocus.text('New Medical History');
        }
    });
});