/*main from button*/
const bulk_btn_keywords_pc = document.getElementById('bulk_btn_keywords_pc');
const bulk_btn_keywords_mobile = document.getElementById('bulk_btn_keywords_mobile');
/*spinner common*/
const spinner=document.getElementById('spinner');
const spinner_info=document.getElementById("spinner_info");
spinner_info.style.display='none';
/*keyword search input*/
const bulk_search_keyword_pc=document.getElementById("bulk_search_keyword_pc");
const bulk_search_keyword_mobile=document.getElementById("bulk_search_keyword_mobile");
/*keyword display table*/
const bulkRelkeyword_table_pc=document.getElementById("bulkRelkeyword_table_pc");
const bulkRelkeyword_table_mobile=document.getElementById("bulkRelkeyword_table_mobile");

const bulk_keywords_pc=document.getElementById("bulk_keywords_pc");
const bulk_keywords_mobile=document.getElementById("bulk_keywords_mobile");

/*검색결과 키워드 display*/
const bulkKeyword_content=document.getElementById("bulkKeyword_content");
const bulkKeyword_keyword=document.getElementById("bulkKeyword_keyword");
/*csv button common*/
const bulk_csv_btn=document.getElementById("bulk_csv_btn");
/*progress bar common*/
const bulk_keyword_progress=document.getElementById("bulk_keyword_progress");
const bulk_keyword_progress_div=document.getElementById("bulk_keyword_progress_div");
bulk_keyword_progress_div.style.display="none";
/* body_content - main*/
const body_content=document.getElementById("body_content");

// bulk_search_keyword_pc.addEventListener('keyup', function(event){
//     if(event.keyCode===13){
//         event.preventDefault();
//         bulk_btn_keywords_pc.click();
//     }
// })

// bulk_search_keyword_mobile.addEventListener('keyup', function(event){
//     if(event.keyCode===13){
//         event.preventDefault();
//         bulk_btn_keywords_mobile.click();
//     }
// })

function progress(timeValue){
    if (timeValue==0){
        timeValue=1;
        var widthValue=1;
        var id=setInterval(frame, 1500);
        function frame(){
            if(widthValue>=100){
                clearInterval(id);
                timeValue=0;
                bulk_keyword_progress.innerHTML='<span class="h5"><strong>결과를 정리중입니다</strong></span>';
            }else{
                widthValue++;
                bulk_keyword_progress.style.width=widthValue+"%";
                bulk_keyword_progress.innerHTML=`<span class="h5"><strong>${widthValue}%</strong></span>`;
            }
        }
    }else{
        return
    }
}


bulk_btn_keywords_pc.addEventListener('click', (e)=>{
    e.preventDefault();
    
    const keyword=bulk_search_keyword_pc.value.split('\n'); // pc input value 가져오기
    bulk_search_keyword_pc.value=null; // pc input value 초기화
    
    spinner.style.display='block'; // spinner display
    spinner_info.style.display='block'; // spinner info display

    // bulkRelkeyword_table_pc.style.display='none'; // pc 테이블 display none
    bulk_keywords_pc.style.display='none';
    
    bulkKeyword_content.style.display='none'; // 키워드 검색결과 display none
    bulkKeyword_keyword.innerHTML=""; // 키워드 검색결과 display none
    bulkRelkeyword_table_pc.innerHTML=""; // pc 테이블 초기화
    bulk_csv_btn.innerHTML=""; // csv button 초기화
    

    /* 버튼 클릭 후 모든 HTML 기능 비활성화 */
    body_content.style.pointerEvents="none";
    body_content.style.opacity="85%";

    /* progress bar */
    bulk_keyword_progress_div.style.display="block";

    var timeValue=0;
    if (timeValue==0){
        timeValue=1;
        var widthValue=0;
        var id=setInterval(frame, 1000);
        function frame(){
            if(widthValue>=100){
                clearInterval(id);
                timeValue=0;
                bulk_keyword_progress.innerHTML='<span class="h3 pt-2"><strong>결과를 정리중입니다</strong></span>';
            }else{
                widthValue++;
                bulk_keyword_progress.style.width=widthValue+"%";
                bulk_keyword_progress.innerHTML=`<span class="h3 pt-2"><strong>${widthValue}%</strong></span>`;
            }
        }
    }else{
        return
    }

    // bulk_keyword_progress.style.display="block";
    fetch('search-bulk', {
        body:JSON.stringify({ keyword:keyword }),
        method:"POST",
        })
    .then((res)=>res.json())
    .then((result)=>{
        clearInterval(id);
        spinner.style.display='none';
        spinner_info.style.display='none';

        // bulkRelkeyword_table_pc.style.display='block';
        bulk_keywords_pc.style.display='block';
        bulkKeyword_content.style.display='block';

        /* fetch 완료 후 HTML 기능 재활성화 */
        body_content.style.pointerEvents="auto";
        body_content.style.opacity="100%";

        /* progress bar */
        bulk_keyword_progress_div.style.display="none";

        bulkKeyword_keyword.innerHTML+=`
            <h3><strong>${keyword}</strong> 검색결과</h3>
        `;
        bulk_csv_btn.innerHTML+=`
            <a href="expand-export-csv/${keyword}"><i class="fas fa-file-csv h5 text-dark"></i></a>
        `;
        for(var i=0; i<result.length; i++){
            if (result[i].keywordRating != 'blank'){
                bulkRelkeyword_table_pc.innerHTML+=`
                <tr>
                    <th scope="row">${i+1}</th>
                    <td><a href="/search-l2/${result[i].keyword}"><strong>${result[i].keyword}</strong></a></td>
                    <td><strong>${result[i].monthlyPcQcCnt.toLocaleString('en-US')}</strong></td>
                    <td><strong>${result[i].monthlyMobileQcCnt.toLocaleString('en-US')}</strong></td>
                    <td><strong>${result[i].pubAmount.toLocaleString('en-US')}</strong></td>
                    <td class="text-danger"><strong>${result[i].keywordRating}</strong></td>
                </tr>
            `;
            }
        }
    })
})

bulk_btn_keywords_mobile.addEventListener('click', (e)=>{
    console.log("hello world")
    e.preventDefault();
    
    const keyword=bulk_search_keyword_mobile.value.split('\n');
    bulk_search_keyword_mobile.value=null;
    
    spinner.style.display='block';
    spinner_info.style.display='block';

    bulk_keywords_mobile.style.display='none';

    bulkKeyword_content.style.display='none';
    bulkKeyword_keyword.innerHTML=""; // 키워드 검색결과 display none
    bulkRelkeyword_table_mobile.innerHTML="";
    bulk_csv_btn.innerHTML="";
    
    /* 버튼 클릭 후 모든 HTML 기능 비활성화 */
    body_content.style.pointerEvents="none";
    body_content.style.opacity="85%";

    /* progress bar */
    bulk_keyword_progress_div.style.display="block";

    var timeValue=0;
    if (timeValue==0){
        timeValue=1;
        var widthValue=0;
        var id=setInterval(frame, 1000);
        function frame(){
            if(widthValue>=100){
                clearInterval(id);
                timeValue=0;
                bulk_keyword_progress.innerHTML='<span class="h3 pt-2"><strong>결과를 정리중입니다</strong></span>';
            }else{
                widthValue++;
                bulk_keyword_progress.style.width=widthValue+"%";
                bulk_keyword_progress.innerHTML=`<span class="h3 pt-2"><strong>${widthValue}%</strong></span>`;
            }
        }
    }else{
        return
    }

    // bulk_keyword_progress.style.display="block";
    fetch('search-bulk', {
        body:JSON.stringify({ keyword:keyword }),
        method:"POST",
        })
    .then((res)=>res.json())
    .then((result)=>{
        clearInterval(id);
        spinner.style.display='none';
        spinner_info.style.display='none';

        bulk_keywords_mobile.style.display='block';
        bulkKeyword_content.style.display='block';

        /* fetch 완료 후 HTML 기능 재활성화 */
        body_content.style.pointerEvents="auto";
        body_content.style.opacity="100%";

        /* progress bar */
        bulk_keyword_progress_div.style.display="none";

        bulkKeyword_keyword.innerHTML+=`
            <p><strong>${keyword}</strong> 검색결과</p>
        `;
        bulk_csv_btn.innerHTML+=`
            <a href="expand-export-csv/${keyword}"><i class="fas fa-file-csv h5 text-dark"></i></a>
        `;

        for(var i=0; i<result.length; i++){
            if (result[i].keywordRating != 'blank'){
                bulkRelkeyword_table_mobile.innerHTML+=`
                <tr>
                    <th scope="row" style="font-size:0.5rem">${i+1}</th>
                    <td style="font-size:0.5rem"><a href="/search-l2/${result[i].keyword}"><strong>${result[i].keyword}</strong></a></td>
                    <td style="font-size:0.5rem"><strong>${(result[i].monthlyPcQcCnt+result[i].monthlyMobileQcCnt).toLocaleString('en-US')}</strong></td>
                    <td style="font-size:0.5rem"><strong>${result[i].pubAmount.toLocaleString('en-US')}</strong></td>
                    <td class="text-danger" style="font-size:0.5rem"><strong>${result[i].keywordRating}</strong></td>
                </tr>
            `;
            }
            
        }
    })
})

