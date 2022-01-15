const expand_recomm_keywords = document.getElementById('expand_recomm_keywords');
const recommend_keywords_pc = document.getElementById('recommend_keywords_pc');
const spinner=document.getElementById('spinner');
const spinner_info=document.getElementById("spinner_info");
spinner_info.style.display='none';
const expand_search_keyword=document.getElementById("expand_search_keyword");
const expandRelkeyword_table=document.getElementById("expandRelkeyword_table");

const expandKeyword_content=document.getElementById("expandKeyword_content");
const expandKeyword_keyword=document.getElementById("expandKeyword_keyword");

const expand_csv_btn=document.getElementById("expand_csv_btn");

const process_before=document.getElementById("process_before");


const body_content=document.getElementById("body_content");

const expand_keyword_progress=document.getElementById("expand_keyword_progress");
const expand_keyword_progress_div=document.getElementById("expand_keyword_progress_div");
expand_keyword_progress_div.style.display="none";


expand_search_keyword.addEventListener('keyup', function(event){
    if(event.keyCode===13){
        event.preventDefault();
        expand_recomm_keywords.click();
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


expand_recomm_keywords.addEventListener('click', (e)=>{
    e.preventDefault();
    
    expandRelkeyword_table.innerHTML="";
    
    const keyword=expand_search_keyword.value;
    expand_search_keyword.value=null;
    
    spinner.style.display='block';
    spinner_info.style.display='block';
    recommend_keywords_pc.style.display='none';

    expandKeyword_content.style.display='none';
    expandKeyword_keyword.innerHTML="";
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
        recommend_keywords_pc.style.display='block';

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

        for(var i=0; i<result.length; i++){
            expandRelkeyword_table.innerHTML+=`
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
    })
})

