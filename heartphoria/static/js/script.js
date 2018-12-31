var animationEnd = (function(el) {
        var animations = {
            "animation": "animationend",
            "OAnimation": "oAnimationEnd",
            "MozAnimation": "mozAnimationEnd",
           "WebkitAnimation": "webkitAnimationEnd"
        };

        for(var t in animations) {
            if(el.style[t] !== undefined) {
                return animations[t];
            }
        }
})(document.createElement("fakeElement"));

/* reminderSection */
$(document).on('click', '#reminderSection #reminderToggle', function() {
    $('#reminderForm').toggleClass('expand');
});

/* appointmentSection */
$(document).on('click', '#appointmentSection #appointmentToggle', function() {
    $('#appointmentForm').toggleClass('expand');
});

/* historySection */
$(document).on('click', '#historySection #historyToggle', function() {
    $('#historyForm').toggleClass('expand');
});