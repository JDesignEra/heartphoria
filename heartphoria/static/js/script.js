let animationEnd = (function(el) {
        let animations = {
            "animation": "animationend",
            "OAnimation": "oAnimationEnd",
            "MozAnimation": "mozAnimationEnd",
           "WebkitAnimation": "webkitAnimationEnd"
        };

        for(var t in animations) {
            if (el.style[t] !== undefined) {
                return animations[t];
            }
        }
})(document.createElement("fakeelement"));

/* Scrolling Nav */
$(window).scroll(function() {
    let focus = $('nav');

    if (focus.offset().top > 100) {
        focus.removeClass('navbar-light bg-light py-3');
        focus.addClass('navbar-dark bg-gradient');

        let btnFocus = $('nav .btn-outline-success');
        btnFocus.removeClass('btn-outline-success');
        btnFocus.addClass('btn-success')
    }
    else {
        focus.removeClass('navbar-dark bg-gradient');
        focus.addClass('navbar-light bg-light py-3');

        let btnFocus = $('nav .btn-success');
        btnFocus.removeClass('btn-success');
        btnFocus.addClass('btn-outline-success');
    }
});

/* HomeSection */
if ($('#HomeSection').length) {
    $(document).on('click', '#HomeSection #WeatherDetailsToggle', function () {
        let btnFocus = $(this);

        if (btnFocus.hasClass('collapsed')) {
            btnFocus.text('Show More Details');
        }
        else {
            btnFocus.text('Hide More Details');
        }
    });
}

/* ReminderSection */
if ($('#ReminderSection').length) {
    $(document).on('click', '#ReminderSection #ReminderToggle', function() {
        let btnFocus = $(this);

        if (btnFocus.hasClass('collapsed')) {
            btnFocus.text('New Medication Reminder');
        }
        else {
            btnFocus.text('Hide New Medication Reminder');
        }
    });
}

/* AppointmentSection */
if ($('#AppointmentSection').length) {
    $(document).on('click', '#AppointmentSection #AppointmentToggle', function() {
        let btnFocus = $(this);

        if (btnFocus.hasClass('collapsed')) {
            btnFocus.text('New Medical Appointment');
        }
        else {
            btnFocus.text('Hide New Medical Appointment');
        }
    });

    /* Autcomplete */
    let substringMatcher = function(strs) {
        return function findMatches(q, cb) {
            let matches, substringRegex;

            matches = [];

            substrRegex = new RegExp(q, 'i');

            $.each(strs, function(i, str) {
                if (substrRegex.test(str)) {
                    matches.push(str);
                }
            });

            cb(matches);
        };
    };

    $('input#location').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        name: 'autocomplete',
        source: substringMatcher(autocomplete)
    });
}

/* HistorySection */
if ($('#HistorySection').length) {
    $(document).on('click', '#HistorySection #HistoryToggle', function() {
        let btnFocus = $(this);

        if (btnFocus.hasClass('collapsed')) {
            btnFocus.text('New Medical History');
        }
        else {
            btnFocus.text('Hide New Medical History');
        }
    });
}

/* EditProfileSection */
if ($('#UploadModal').length) {
    $(document).on('dragover', '#UploadModal #DragDropArea', function(e) {
        e.preventDefault();
    });

    $(document).on('dragleave', '#UploadModal #DragDropArea', function(e) {
        e.preventDefault();
    });

    $(document).on('drop', '#UploadModal #DragDropArea', function(e) {
        e.preventDefault();

        $('#UploadModal .feedback').addClass('d-none');

        let uploads = e.originalEvent.dataTransfer.files || (e.dataTransfer && e.dataTransfer.files) || e.target.files;

        if (uploads.length > 1) {
            let focus = $('#UploadModal .feedback');

            $(focus).text('Only 1 image is allowed');
            $(focus).removeClass('d-none');
        }
        else if (uploads[0].size > 2097152) {
            let focus = $('#UploadModal .feedback');

            $(focus).text('Image size cannot exceed 2MB');
            $(focus).removeClass('d-none');
        }
        else {
            $('#UploadModal input[name=file]').prop('files', uploads);
            $('#UploadModal #UploadForm').submit();
        }
    });

    $(document).on('click', '#UploadModal #DragDropArea', function() {
        $('#UploadModal input[name=file]').click();
    });

    $(document).on('change', '#UploadModal input[name=file]', function() {
        $('#UploadModal #UploadForm').submit();
    });

    $(document).on('mouseenter', '#EditProfileSection .card-body .dp', function() {
        $(this).css('padding-top', 'calc(80% + 24px)');
        $(this).find('.db-popup').removeClass('flipOutX d-none');
        $(this).find('.db-popup').addClass('flipInX')
    });

    $(document).on('mouseleave', '#EditProfileSection .card-body .dp', function() {
        $(this).css('padding-top', '');
        $(this).find('.db-popup').addClass('d-none');
    });
}

/* HospitalSection */
/* Search Function */
$(document).on('keyup', '#HospitalSection input#Search', function() {
    let search = $(this).val().toLowerCase();
    let listFocus = $('#HospitalSection button.list-group-item');

    for (let i = 0; i < listFocus.length; i++) {
        let itemFocus = $(listFocus[i]);

        if (itemFocus.hasClass('active') || itemFocus.data('name').indexOf(search) > -1 || itemFocus.data('address').indexOf(search) > -1) {
            itemFocus.removeClass('d-none');
        }
        else {
            itemFocus.addClass('d-none');
        }
    }
});

/* Clear Search */
$(document).on('click', '#HospitalSection .input-group button', function() {
    $('#HospitalSection input#Search').val('');
    $('#HospitalSection button.list-group-item').removeClass('d-none');
});

/* Map */
if ($('#HospitalSection #map').length && typeof token !== 'undefined') {
    $('.toast').toast({
        'autohide': false
    });
    $('.toast').toast('show');

    mapboxgl.accessToken = token;

    let map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v10',
        center: [103.8, 1.35],
        zoom: 11
    });

    map.addControl(new mapboxgl.NavigationControl());
    map.on('load', function() {
        map.addLayer({
            'id': '3d-buildings',
            'source': 'composite',
            'source-layer': 'building',
            'filter': ['==', 'extrude', 'true'],
            'type': 'fill-extrusion',
            'minzoom': 15,
            'paint': {
                'fill-extrusion-color': '#BB0564',
                'fill-extrusion-height': [
                    "interpolate", ["linear"], ["zoom"],
                    15, 0,
                    15.05, ["get", "height"]
                ],
                'fill-extrusion-base': [
                    "interpolate", ["linear"], ["zoom"],
                    15, 0,
                    15.05, ["get", "min_height"]
                ],
                'fill-extrusion-opacity': .6
            }
        });
    });

    /* Get current location & set user marker */
    if (navigator.geolocation) {
        $('#HospitalSection .alert').alert('close');

        let userMarker;
        let hospitalMarker;

        if (userMarker) {
            userMarker.remove();
        }

        let icon = document.createElement('i');
        icon.classList.add('fas', 'fa-street-view', 'fa-4x', 'text-primary');

        /* Create initial user marker */
        userMarker = new mapboxgl.Marker({
            element: icon,
            color: '#BB0564'
        })
        .setLngLat([103,8, 1.35])
        .addTo(map);

        /* User location watcher */
        let centerUserOnce = true;

        navigator.geolocation.watchPosition(function(pos) {
            let lat = pos.coords.latitude;
            let lng = pos.coords.longitude;

            if (centerUserOnce) {
                map.setCenter([lng, lat]);
                map.setZoom(16);
                map.setPitch(55);
                map.setBearing(-20);
                centerUserOnce = false;
            }

            userMarker.setLngLat([lng, lat])

            let btnFocus = $('button#ZoomMe');
            btnFocus.attr('data-lng', lng);
            btnFocus.attr('data-lat', lat);

            let locationLng = $('button#ZoomLocation').data('lng');
            let locationLat = $('button#ZoomLocation').data('lat');

            if (lng && lat && locationLng && locationLat) {
                drawDirection(map, lng, lat, locationLng, locationLat);
            }
        });

        /* Locations List Buttons */
        $(document).on('click', '.list-group button.list-group-item', function() {
            $('.list-group button.list-group-item').removeClass('active');
            $(this).addClass('active');

            let lng = $(this).data('lng')
            let lat = $(this).data('lat');

            if (hospitalMarker) {
                hospitalMarker.remove();
            }

            /* Add hospital marker, popup and fly to marker */
            hospitalMarker = new mapboxgl.Marker({
                color: '#FCA904'
            })
            .setLngLat([
                lng,
                lat
            ])
            .addTo(map);

            map.flyTo({
                center: [
                    lng,
                    lat
                ]
            });

            /* Set ZoomLocation data attributes */
            let btnFocus = $('button#ZoomLocation');

            if (btnFocus.hasClass('d-none')) {
                btnFocus.removeClass('d-none');
                btnFocus.addClass('fadeIn shortest').one(animationEnd, function() {
                    $(this).removeClass('fadeIn shortest');
                });
            }

            btnFocus.attr('data-lng', lng);
            btnFocus.attr('data-lat', lat);

            /* Draw Direction */
            let userLng = $('button#ZoomMe').data('lng');
            let userLat = $('button#ZoomMe').data('lat');

            if (userLng && userLat && lng && lat) {
                drawDirection(map, userLng, userLat, lng, lat);
            }
        });

        /* ZoomLocation Button */
        $(document).on('click', 'button#ZoomLocation', function() {
            map.flyTo({
                center: [
                    $(this).data('lng'),
                    $(this).data('lat')
                ]
            });
        });

        /* ZoomMe Button */
        $(document).on('click', 'button#ZoomMe', function() {
            map.flyTo({
                center: [
                    $(this).data('lng'),
                    $(this).data('lat')
                ]
            });
        });
    }
}

function drawDirection(map, fromLng, fromLat, toLng, toLat) {
    if (map.getSource('route')) {
        map.removeLayer('route')
        map.removeSource('route')
    }

    $.get(
        'https://api.mapbox.com/directions/v5/mapbox/driving/' + fromLng + ',' + fromLat + ';' + toLng + ',' + toLat,
        {
            geometries: 'geojson',
            steps: 'true',
            access_token: token
        },
        function(data) {
            if (data['code'] == 'Ok') {
                map.addLayer({
                    'id': 'route',
                    'type': 'line',
                    'source': {
                        'type': 'geojson',
                        'data': {
                            'type': 'Feature',
                            'properties': {},
                            'geometry': data['routes'][0]['geometry']
                        }
                    },
                    'layout': {
                        'line-join': 'round',
                        'line-cap': 'round'
                    },
                    'paint': {
                        'line-color': '#BB0564',
                        'line-width': 10
                    }
                });
            }
        }
    , 'json');
}