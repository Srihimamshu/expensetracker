// console.log("register here");
const usernameField = document.querySelector("#usernameField");
const feedbackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#emailField");
const emailFeedbackArea = document.querySelector(".emailFeedbackArea");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const passwordField = document.querySelector("#passwordField");
const submitButton = document.querySelector(".submit-btn");

showPasswordToggle.addEventListener('click', (e)=>{
    if (showPasswordToggle.textContent=="SHOW"){
        showPasswordToggle.textContent="HIDE";
        passwordField.setAttribute("type","text");
    }else{
        showPasswordToggle.textContent="SHOW";
        passwordField.setAttribute("type","password");
    }
});

emailField.addEventListener('keyup',(e)=>{
    const emailVal=e.target.value;
    console.log("emailVal",emailVal);
    emailField.classList.remove('is-invalid');
    emailFeedbackArea.style.display="none";

    if( emailVal.length>0){
        fetch("/authentication/validate-email",{
            body:JSON.stringify({email: emailVal}),
            method: "POST",
    
        })
        .then(res=>res.json())
        .then(data=>{
            console.log("data",data);
            if(data.email_error){
                submitButton.disabled=true;
                emailField.classList.add('is-invalid');
                emailFeedbackArea.style.display="block";
                emailFeedbackArea.innerHTML=`<p>${data.email_error}</p>`;
            }else{
                submitButton.removeAttribute("disabled");
            }
        });
    }
    

});



usernameField.addEventListener('keyup',(e)=>{
    // console.log("8888",8888);
    const usernameVal=e.target.value;
    console.log("usernameVal",usernameVal);
    usernameSuccessOutput.style.display="block";
    usernameSuccessOutput.textContent=`Checking username availability...`;
    usernameField.classList.remove('is-invalid');
    feedbackArea.style.display="none";

    if( usernameVal.length>0){
        fetch("/authentication/validate-username",{
            body:JSON.stringify({username: usernameVal}),
            method: "POST",
    
        })
        .then(res=>res.json())
        .then(data=>{
            console.log("data",data);
            usernameSuccessOutput.style.display="none";
            if(data.username_error){
                submitButton.disabled=true;
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display="block";
                feedbackArea.innerHTML=`<p>${data.username_error}</p>`;
            }else{
                submitButton.removeAttribute("disabled");
            }
        });
    }
    
});