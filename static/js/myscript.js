$(document).ready(function(){
// Prepare the preview for profile picture
    $("#wizard-picture").change(function(){
        readURL(this);
    });
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#wizardPicturePreview').attr('src', e.target.result).fadeIn('slow');
            }
            reader.readAsDataURL(input.files[0]);
        }
    }


//////////  Materializecss Initialization   /////////
    $('.collapsible').collapsible();
    $('select').material_select();
    document.querySelectorAll('.select-wrapper').forEach(t => t.addEventListener('click', e=>e.stopPropagation())) // fixes first click
    $(".button-collapse").sideNav();
    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 15, // Creates a dropdown of 15 years to control year,
        today: 'Today',
        clear: 'Clear',
        close: 'Ok',
        closeOnSelect: false, // Close upon selecting a date,
        defaultTime: 'now'

    });
    $('.datepicker').on('mousedown',function(event){ event.preventDefault(); })
    $('.carousel').carousel({

    });
    $('.modal').modal();
    $('.parallax').parallax();

});


function openModal() {

    //call the specific div (modal)
    $('#modal').modal('open');


    var pleaseWait = $('#pleaseWaitDialog');

    showPleaseWait = function () {
        pleaseWait.modal('open');
        //$('#modal').modal('open');
    };

    hidePleaseWait = function () {
        pleaseWait.modal('close');
        //('#modal').modal('open');
    };

    showPleaseWait();
};




// Thermometer  https://codepen.io/GeorgePark/pen/oVgGyM

document.addEventListener("DOMContentLoaded", () => {

    const emoji = document.querySelector('.emoji'),
        slider = document.querySelector('.slider'),
        tempOutput = document.querySelector('.temperature-output'),
        displayTemp = temperature => {
            //Display temperature
            tempOutput.textContent = temperature;

            //Display emoji
            if (temperature >= 0 && temperature <= 8) {
                emoji.textContent = '🥶';
                emoji.setAttribute('aria-label', 'freezing face');
            } else if (temperature > 8 && temperature <= 16) {
                emoji.textContent = '😬';
                emoji.setAttribute('aria-label', 'cold face');
            } else if (temperature > 16 && temperature <= 24) {
                emoji.textContent = '😊';
                emoji.setAttribute('aria-label', 'happy face');
            } else if (temperature > 24 && temperature <= 32) {
                emoji.textContent = '😅';
                emoji.setAttribute('aria-label', 'warm face');
            } else {
                emoji.textContent = '🥵';
                emoji.setAttribute('aria-label', 'hot face');
            }
        }

    slider.addEventListener('input', () => displayTemp(slider.value));

    //CodePen preview window
    if (location.pathname.includes('fullcpgrid')) {

        let temperature = 0;

        const interval = setInterval(() => {

            //Remove interval if max temperature is reached
            if (temperature === 40) clearInterval(interval);

            //Update slider value
            slider.value = temperature;

            //Display temperature and emoji
            displayTemp(temperature);

            //Increase temperature
            temperature++;

        }, 95);
    }
});

// Thermometer  https://codepen.io/GeorgePark/pen/oVgGyM




