document.addEventListener("DOMContentLoaded", function() {
    let spinner = document.getElementById("spinner");
    spinner.style.display = "none";
});

// email user and admin when contact form is used 
function sendMail(contactForm){
    spinner.style.display = "block";
    emailjs.send("outlook", "lotr_contact", {
        "from_name": contactForm.name.value,
        "from_email": contactForm.email.value,
        "subject": contactForm.subject.value,
        "message": contactForm.message.value
    })
    .then(
        function(response) {
            console.log("SUCCESS", response);
            contactForm.reset();
            console.log("Form is reset");
            spinner.style.display = "none";
        },
        function(error) {
            console.log("FAILED", error);
        }
    );
    return false;
}

function newAlert() {
    alert("If you have completed the form correctly you will receive a confirmation email once the form resets!");
}

  
// email admin when user posts a recipe or comment

function adminNotification() {
    emailjs.send("outlook","lotrAPPROVE")
    .then(
        function(response) {
            console.log("SUCCESS", response);
            contactForm.reset();
            console.log("Form is reset");
        },
        function(error) {
            console.log("FAILED", error);
        }
    );
    return false;
}


setTimeout(function() {
    let messages = document.getElementById('msg');
    let alert = new bootstrap.Alert(messages);
    alert.close();
}, 3000);


var myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})

