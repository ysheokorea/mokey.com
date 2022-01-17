const searchform = document.getElementById("searchform");


function enterPress(f){
    if(f.keyCode==13){
        console.log('press is hit')
        searchform.submit();
    }
}
function getHistoryCount(){
    const hisotryCounter=document.getElementById("hisotryCounter");
    hisotryCounter.innerHTML="";
    fetch('history',{
        method:"POST",
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        }
    })
    .then((res)=>res.json())
    .then((result)=>{
        // hisotryCounter.insertAdjacentHTML('afterend',result)
        hisotryCounter.innerHTML+=`<strong>${result}</strong>`;
    })
}

//Get the button:
mybutton = document.getElementById("topBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
} else {
    mybutton.style.display = "none";
}
}

// When the user clicks on the button, scroll to the top of the document
function goToTop() {
    window.setTimeout(()=>{
        document.body.scrollTop = 0; // For Safari
        document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    }, 0)
}

document.onload=getHistoryCount();


