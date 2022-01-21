const analyze_post_btn = document.getElementById('analyze_post_btn');
const analyze_post_pc = document.getElementById('analyze_post_pc');
const spinner=document.getElementById('spinner');
const spinner_info=document.getElementById("spinner_info");
spinner_info.style.display='none';
const analyze_post_input=document.getElementById("analyze_post_input");
const analyze_post_table=document.getElementById("analyze_post_table");
const analyze_post_content=document.getElementById('analyze_post_content');
const analyze_post_keyword=document.getElementById('analyze_post_keyword');

const body_content=document.getElementById("body_content");

analyze_post_input.addEventListener('keyup', function(event){
    if(event.keyCode===13){
        event.preventDefault();
        analyze_post_btn.click();
    }
})

analyze_post_btn.addEventListener('click', (e)=>{
    e.preventDefault();
    analyze_post_table.innerHTML="";

    const keyword=analyze_post_input.value;
    analyze_post_input.value=null;
    
    spinner.style.display='block';
    spinner_info.style.display='block';
    analyze_post_pc.style.display='none';

    analyze_post_keyword.style.display='none';
    analyze_post_content.innerHTML="";

    /* 버튼 클릭 후 모든 HTML 기능 비활성화 */
    body_content.style.pointerEvents="none";
    body_content.style.opacity="70%";

    fetch('blogAnaylize_js', {
        body:JSON.stringify({ keyword:keyword }),
        method:"POST",
        })
    .then((res)=>res.json())
    .then((result)=>{
        console.log(result)
        spinner.style.display='none';
        spinner_info.style.display='none';
        analyze_post_pc.style.display='block';

        analyze_post_content.style.display='block';

        /* fetch 완료 후 HTML 기능 재활성화 */
        body_content.style.pointerEvents="auto";
        body_content.style.opacity="100%";

        analyze_post_keyword.innerHTML+=`
            <h3><strong>${keyword}</strong> 검색결과</h3>
        `;

        for(var i=0; i<result.length; i++){
            analyze_post_table.innerHTML+=`
            <tr>
                <th scope="row">${i+1}</th>
                <td><strong>${result[i].textLen.toLocaleString('en-US')}</strong></td>
                <td><strong>${result[i].imageCount.toLocaleString('en-US')}</strong></td>
                <td><strong>${result[i].vedioCount.toLocaleString('en-US')}</strong></td>
                <td class="text-danger"><strong>${result[i].keywordCount.toLocaleString('en-US')}</strong></td>
            </tr>
        `;
        }
    })
})