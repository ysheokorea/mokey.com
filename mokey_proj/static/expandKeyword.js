/*main from button*/
const expand_btn_keywords_pc = document.getElementById('expand_btn_keywords_pc');
const expand_btn_keywords_mobile = document.getElementById('expand_btn_keywords_mobile');
/*spinner common*/
const spinner=document.getElementById('spinner');
const spinner_info=document.getElementById("spinner_info");
spinner_info.style.display='none';
/*keyword search input*/
const expand_search_keyword_pc=document.getElementById("expand_search_keyword_pc");
const expand_search_keyword_mobile=document.getElementById("expand_search_keyword_mobile");
/*keyword display table*/
const expandRelkeyword_table_pc=document.getElementById("expandRelkeyword_table_pc");
const expandRelkeyword_table_mobile=document.getElementById("expandRelkeyword_table_mobile");

const expand_keywords_pc=document.getElementById("expand_keywords_pc");
const expand_keywords_mobile=document.getElementById("expand_keywords_mobile");

/*검색결과 키워드 display*/
const expandKeyword_content=document.getElementById("expandKeyword_content");
const expandKeyword_keyword=document.getElementById("expandKeyword_keyword");
/*csv button common*/
const expand_csv_btn=document.getElementById("expand_csv_btn");
/*progress bar common*/
const expand_keyword_progress=document.getElementById("expand_keyword_progress");
const expand_keyword_progress_div=document.getElementById("expand_keyword_progress_div");
expand_keyword_progress_div.style.display="none";
/* body_content - main*/
const body_content=document.getElementById("body_content");

expand_search_keyword_pc.addEventListener('keyup', function(event){
    if(event.keyCode===13){
        event.preventDefault();
        expand_btn_keywords_pc.click();
    }
})

expand_search_keyword_mobile.addEventListener('keyup', function(event){
    if(event.keyCode===13){
        event.preventDefault();
        expand_btn_keywords_mobile.click();
    }
})

function progress(timeValue){
    if (timeValue==0){
        timeValue=1;
        var widthValue=1;
        var id=setInterval(frame, 1500);
        function frame(){
            if(widthValue>=100){
                clearInterval(id);
                timeValue=0;
                expand_keyword_progress.innerHTML='<span class="h5"><strong>결과를 정리중입니다</strong></span>';
            }else{
                widthValue++;
                expand_keyword_progress.style.width=widthValue+"%";
                expand_keyword_progress.innerHTML=`<span class="h5"><strong>${widthValue}%</strong></span>`;
            }
        }
    }else{
        return
    }
}


expand_btn_keywords_pc.addEventListener('click', (e)=>{
    e.preventDefault();
    
    const keyword=expand_search_keyword_pc.value; // pc input value 가져오기
    expand_search_keyword_pc.value=null; // pc input value 초기화
    
    spinner.style.display='block'; // spinner display
    spinner_info.style.display='block'; // spinner info display
    expandRelkeyword_table_pc.style.display='none'; // pc 테이블 display none
    expand_keywords_pc.style.display='none';
    
    expandKeyword_content.style.display='none'; // 키워드 검색결과 display none
    expandKeyword_keyword.innerHTML=""; // 키워드 검색결과 display none
    expandRelkeyword_table_pc.innerHTML=""; // pc 테이블 초기화
    expand_csv_btn.innerHTML=""; // csv button 초기화
    

    /* 버튼 클릭 후 모든 HTML 기능 비활성화 */
    body_content.style.pointerEvents="none";
    body_content.style.opacity="85%";

    /* progress bar */
    expand_keyword_progress_div.style.display="block";

    var timeValue=0;
    if (timeValue==0){
        timeValue=1;
        var widthValue=0;
        var id=setInterval(frame, 600);
        function frame(){
            if(widthValue>=100){
                clearInterval(id);
                timeValue=0;
                expand_keyword_progress.innerHTML='<span class="h3 pt-2"><strong>결과를 정리중입니다</strong></span>';
            }else{
                widthValue++;
                expand_keyword_progress.style.width=widthValue+"%";
                expand_keyword_progress.innerHTML=`<span class="h3 pt-2"><strong>${widthValue}%</strong></span>`;
            }
        }
    }else{
        return
    }

    // expand_keyword_progress.style.display="block";
    fetch('expandKeyword_js', {
        body:JSON.stringify({ keyword:keyword }),
        method:"POST",
        })
    .then((res)=>res.json())
    .then((result)=>{
        clearInterval(id);
        spinner.style.display='none';
        spinner_info.style.display='none';

        expandRelkeyword_table_pc.style.display='block';
        expand_keywords_pc.style.display='block';
        expandKeyword_content.style.display='block';

        /* fetch 완료 후 HTML 기능 재활성화 */
        body_content.style.pointerEvents="auto";
        body_content.style.opacity="100%";

        /* progress bar */
        expand_keyword_progress_div.style.display="none";

        expandKeyword_keyword.innerHTML+=`
            <h3><strong>${keyword}</strong> 검색결과</h3>
        `;
        expand_csv_btn.innerHTML+=`
            <a href="expand-export-csv/${keyword}"><i class="fas fa-file-csv h5 text-dark"></i></a>
        `;
        expandRelkeyword_table_pc.innerHTML+=`
    
        <tr>
            <th style="font-size:70%; width:5%; vertical-align:middle;">#</th>
            <th style="font-size:70%; width:50%; vertical-align:middle;">키워드</th>
            <th style="font-size:70%; width:15%;">PC 검색량<br>(월)</th>
            <th style="font-size:70%; width:15%;">Mobie 검색량<br>(월)</th>
            <th style="font-size:70%; width:15%;">블로그 발행량<br>(전체))</th>
            <th style="font-size:70%; width:20%; vertical-align:middle;">등급</th>
        </tr>
    
        `;
        for(var i=0; i<result.length; i++){
            expandRelkeyword_table_pc.innerHTML+= `

                <tr>
                    <th style="width:5%;" scope="row">${i+1}</th>
                    <td style="width:50%;"><a href="/search-l2/${result[i].keyword}"><strong>${result[i].keyword}</strong></a></td>
                    <td style="width:15%;"><strong>${result[i].monthlyPcQcCnt.toLocaleString('en-US')}</strong></td>
                    <td style="width:15%;"><strong>${result[i].monthlyMobileQcCnt.toLocaleString('en-US')}</strong></td>
                    <td style="width:15%;"><strong>${result[i].pubAmount.toLocaleString('en-US')}</strong></td>
                    <td style="width:20%;" class="text-danger"><strong>${result[i].keywordRating}</strong></td>
                </tr>

        `;
        }
    })
})

expand_btn_keywords_mobile.addEventListener('click', (e)=>{
    e.preventDefault();
    
    const keyword=expand_search_keyword_mobile.value;
    expand_search_keyword_mobile.value=null;
    
    spinner.style.display='block';
    spinner_info.style.display='block';
    expandRelkeyword_table_mobile.style.display='none';
    expand_keywords_mobile.style.display='none';

    expandKeyword_content.style.display='none';
    expandKeyword_keyword.innerHTML=""; // 키워드 검색결과 display none
    expandRelkeyword_table_mobile.innerHTML="";
    expand_csv_btn.innerHTML="";
    
    /* 버튼 클릭 후 모든 HTML 기능 비활성화 */
    body_content.style.pointerEvents="none";
    body_content.style.opacity="85%";

    /* progress bar */
    expand_keyword_progress_div.style.display="block";

    var timeValue=0;
    if (timeValue==0){
        timeValue=1;
        var widthValue=0;
        var id=setInterval(frame, 1000);
        function frame(){
            if(widthValue>=100){
                clearInterval(id);
                timeValue=0;
                expand_keyword_progress.innerHTML='<span class="h3 pt-2"><strong>결과를 정리중입니다</strong></span>';
            }else{
                widthValue++;
                expand_keyword_progress.style.width=widthValue+"%";
                expand_keyword_progress.innerHTML=`<span class="h3 pt-2"><strong>${widthValue}%</strong></span>`;
            }
        }
    }else{
        return
    }

    // expand_keyword_progress.style.display="block";
    fetch('expandKeyword_js', {
        body:JSON.stringify({ keyword:keyword }),
        method:"POST",
        })
    .then((res)=>res.json())
    .then((result)=>{
        clearInterval(id);
        spinner.style.display='none';
        spinner_info.style.display='none';
        expandRelkeyword_table_mobile.style.display='block';
        expand_keywords_mobile.style.display='block';
        expandKeyword_content.style.display='block';

        /* fetch 완료 후 HTML 기능 재활성화 */
        body_content.style.pointerEvents="auto";
        body_content.style.opacity="100%";

        /* progress bar */
        expand_keyword_progress_div.style.display="none";

        expandKeyword_keyword.innerHTML+=`
            <span style="font-size:1rem; margin-bottom:0px;"><strong>${keyword}</strong> 검색결과</span>
        `;
        expand_csv_btn.innerHTML+=`
            <a href="expand-export-csv/${keyword}"><i class="fas fa-file-csv h5 text-dark"></i></a>
        `;

        expandRelkeyword_table_mobile.innerHTML+=`
        <tr>
            <th style="font-size:70%; width:3%; vertical-align:middle;">#</th>
            <th style="font-size:70%; width:45%; vertical-align:middle;">KEY</th>
            <th style="font-size:70%; width:8%;">검색<br>(월)</th>
            <th style="font-size:70%; width:8%;">발행<br>(전체)</th>
            <th style="font-size:70%; width:8%;">등급</th>
        </tr>
        `;

        for(var i=0; i<result.length; i++){
            expandRelkeyword_table_mobile.innerHTML+=`
            <tr>
                <th scope="row" style="font-size:0.5rem">${i+1}</th>
                <td style="font-size:0.5rem"><a href="/search-l2/${result[i].keyword}"><strong>${result[i].keyword}</strong></a></td>
                <td style="font-size:0.5rem"><strong>${(result[i].monthlyPcQcCnt+result[i].monthlyMobileQcCnt).toLocaleString('en-US')}</strong></td>
                <td style="font-size:0.5rem"><strong>${result[i].pubAmount.toLocaleString('en-US')}</strong></td>
                <td class="text-danger" style="font-size:0.5rem"><strong>${result[i].keywordRating}</strong></td>
            </tr>
        `;
        }
    })
})

