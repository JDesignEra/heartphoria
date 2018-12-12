$('#bmi').submit(function (e) {
    e.preventDefault();
    //clear error message

    var weight = $('weight').val();
    var height = $('height').val();

    if ($.isNumeric(weight) && $.isNumeric(height)) {
        //bmi formula

        //bmi range

        //$('...').text(bmi);
        //$('...').text(bmiText);
    } else {
        //show error message
    }
});
