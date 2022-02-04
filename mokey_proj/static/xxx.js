const searchform = document.getElementById("searchform");
/* Ads Elements */
const ads_panel_main=document.querySelectorAll(".ads_panel_main")
const ads_panel_side=document.querySelectorAll(".ads_panel_side");

try{
    /* livekw DateChangeBtn */
    const livekw_btn_left=document.getElementById("livekw_btn_left");
    const livekw_btn_rigth=document.getElementById("livekw_btn_rigth");
    const dateValue=document.getElementById("dateValue");
    const live_keyword_table_pc=document.getElementById("live_keyword_table_pc");

    /* livekw DateChangeBtn */
    const livekw_btn_left_mobile=document.getElementById("livekw_btn_left_mobile");
    const dateValue_mobile=document.getElementById("dateValue_mobile");
    const livekw_btn_right_mobile=document.getElementById("livekw_btn_right_mobile");
const live_keyword_table_mobile=document.getElementById("live_keyword_table_mobile");

    /* change selected date */
    livekw_btn_left.addEventListener("click", (e)=>{
        e.preventDefault();
        // console.log(dateValue.innerHTML)
        
        fetch("/live-keyword",{
            body:JSON.stringify({ dateValue:dateValue.innerHTML, dateSignal:'left' }),
            method:"POST",
            })
            .then((res)=>res.json())
            .then((result)=>{
                live_keyword_table_pc.innerHTML="";
                dateValue.innerHTML=result.today;  
                for (var i=0; i<result.live_keywords.length; i++){
                    live_keyword_table_pc.innerHTML+=`
                        <div class="d-flex flex-row justify-content-between mx-1 mb-1 px-1 py-3 border"
                        style="background-color: rgb(243, 243, 243);">
                        <h3 class="pt-5 ml-4 text-danger">
                            <strong>${i+1}</strong>
                        </h3>
                            
                        <div class="mt-3">
                            <h3>
                                <strong>
                                    <a class="links text-dark" href="{% url 'search_l2' ${result.live_keywords[i].keyword} %}">${result.live_keywords[i].keyword}</a>
                                </strong>
                            </h3>
                            <hr>
                            <div>
                                <p><a class="text-primary" href="${result.live_keywords[i].keywordNewsLink}"
                                        target="_blank">${result.live_keywords[i].keywordNewsTitle}</a></p>
                            </div>
                        </div>
                            <div class="mr-4">
                                <h5 class="pt-5 mr-3 text-dark"><strong>${ result.live_keywords[i].amount.toLocaleString('en-US') }+</strong></h5>
                                <p class="text-muted">검색량</p>
                            </div>
                    </div>
                    `;
                }
                
            })   
    })

    livekw_btn_rigth.addEventListener("click", (e)=>{
        e.preventDefault();
        // console.log(dateValue.innerHTML)
        
        fetch("/live-keyword",{
            body:JSON.stringify({ dateValue:dateValue.innerHTML, dateSignal:'right' }),
            method:"POST",
            })
            .then((res)=>res.json())
            .then((result)=>{
                live_keyword_table_pc.innerHTML="";
                dateValue.innerHTML=result.today;  
                for (var i=0; i<result.live_keywords.length; i++){
                    live_keyword_table_pc.innerHTML+=`
                        <div class="d-flex flex-row justify-content-between mx-1 mb-1 px-1 py-3 border"
                            style="background-color: rgb(243, 243, 243);">
                            <h3 class="pt-5 ml-4 text-danger">
                                <strong>${i+1}</strong>
                            </h3>
                                
                            <div class="mt-3">
                                <h3>
                                    <strong>
                                        <a class="links text-dark" href="{% url 'search_l2' ${result.live_keywords[i].keyword} %}">${result.live_keywords[i].keyword}</a>
                                    </strong>
                                </h3>
                                <hr>
                                <div>
                                    <p><a class="text-primary" href="${result.live_keywords[i].keywordNewsLink}"
                                            target="_blank">${result.live_keywords[i].keywordNewsTitle}</a></p>
                                </div>
                            </div>
                                <div class="mr-4">
                                    <h5 class="pt-5 mr-3 text-dark"><strong>${ result.live_keywords[i].amount.toLocaleString('en-US') }+</strong></h5>
                                    <p class="text-muted">검색량</p>
                                </div>
                        </div>
                        `;
                }
            })   
    })

    livekw_btn_left_mobile.addEventListener("click", (e)=>{
        e.preventDefault();
        // console.log(dateValue_mobile.innerHTML)
        

        fetch("/live-keyword",{
            body:JSON.stringify({ dateValue:dateValue_mobile.innerHTML, dateSignal:'left' }),
            method:"POST",
            })
            .then((res)=>res.json())
            .then((result)=>{
                live_keyword_table_mobile.innerHTML="";
                dateValue_mobile.innerHTML=result.today;  
                for (var i=0; i<result.live_keywords.length; i++){
                    live_keyword_table_mobile.innerHTML+=`
                    <tbody id="live_keyword_table_mobile">
                        <tr>
                            <td>
                                <h5 style="color : rgb(241, 85, 85);"><strong>${i+1}</strong></h5>
                            </td>
                                
                            <td>
                                <a class="text-primary" href="${result.live_keywords[i].keywordNewsLink}"
                                        target="_blank"
                                        style="color:black; text-decoration: none;"><strong>${result.live_keywords[i].keyword}</strong></a>
                            </td>
                            <td><strong class="text-dark">${result.live_keywords[i].amount.toLocaleString('en-US')}+</strong></td>
                        </tr>
                    </tbody>
                    `;
                }
                
            })   
    })

    livekw_btn_right_mobile.addEventListener("click", (e)=>{
    e.preventDefault();
    // console.log(dateValue_mobile.innerHTML)
    
    fetch("/live-keyword",{
        body:JSON.stringify({ dateValue:dateValue_mobile.innerHTML, dateSignal:'right' }),
        method:"POST",
        })
        .then((res)=>res.json())
        .then((result)=>{
            live_keyword_table_mobile.innerHTML="";
            dateValue_mobile.innerHTML=result.today;  
            for (var i=0; i<result.live_keywords.length; i++){
                live_keyword_table_mobile.innerHTML+=`
                <tbody id="live_keyword_table_mobile">
                <tr>
                    <td>
                        <h5 style="color : rgb(241, 85, 85);"><strong>${i+1}</strong></h5>
                    </td>
                        
                    <td>
                        <a class="text-primary" href="${result.live_keywords[i].keywordNewsLink}"
                                target="_blank"
                                style="color:black; text-decoration: none;"><strong>${result.live_keywords[i].keyword}</strong></a>
                    </td>
                    <td><strong class="text-dark">${result.live_keywords[i].amount.toLocaleString('en-US')}+</strong></td>
                </tr>
            </tbody>
                    `;
            }
        })   
})
}catch(error){
    console.error(error);
}



function enterPress(f){
    if(f.keyCode==13){
        console.log('press is hit')
        searchform.submit();
    }
}
function getHistoryCount(){
    const hisotryCounter=document.getElementById("hisotryCounter");
    hisotryCounter.innerHTML="";
    fetch('/history',{
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


