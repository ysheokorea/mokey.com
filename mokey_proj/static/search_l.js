const spinner = document.getElementById("spinner");
const search_input_bx = document.getElementById("search_input_bx");
const content = document.getElementById("content");
content.style.visibility = 'hidden';
search_input_bx.style.visibility = 'hidden';
const form_input = document.getElementById("form_input");
const textVal = document.getElementById("relKeyword").textContent;
console.log(textVal)
const monthlyPcQcCnt_desktop=document.getElementById("monthlyPcQcCnt_desktop"); 
const monthlyMobileQcCnt_desktop=document.getElementById("monthlyMobileQcCnt_desktop");
const mothlyTotal_desktop=document.getElementById("mothlyTotal_desktop");

const monthlyPcQcCnt_mobile=document.getElementById("monthlyPcQcCnt_mobile"); 
const monthlyMobileQcCnt_mobile=document.getElementById("monthlyMobileQcCnt_mobile");
const mothlyTotal_mobile=document.getElementById("mothlyTotal_mobile");

const blog_total_count=document.getElementById("blog_total_count");
const blog_total_count_mobile=document.getElementById("blog_total_count_mobile");

const keyword_rating=document.getElementById("keyword_rating");
const keyword_rating_mobile=document.getElementById("keyword_rating_mobile");
const relkeyword_table=document.getElementById("relkeyword_table");
const relkeyword_table_main=document.getElementById("relkeyword_table_main");

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

function search_fetch_desktop(){
    fetch('search', {
        body: JSON.stringify({ textVal: textVal }),
        method: "POST",
        })
        .then((res) => res.json())
        .then((result) => {
            spinner.classList.add('no-display');
            content.style.visibility = 'visible';
            search_input_bx.style.visibility = 'visible';
            monthlyPcQcCnt_desktop.innerHTML += `
                <div class="h4"><i class="fas fa-desktop mb-4 text-muted"></i><br><strong style="font-size:100%;">${result.monthlyPcQcCnt.toLocaleString('en-US')}</strong></div>
            `;
            monthlyMobileQcCnt_desktop.innerHTML += `
                <div class="h4"><i class="fas fa-mobile-alt mb-4 text-muted"></i><br><strong style="font-size:100%;">${result.monthlyMobileQcCnt.toLocaleString('en-US')}</strong></div>
            `;
            mothlyTotal_desktop.innerHTML += `
                <div class="h4"><i class="fas fa-equals mb-4 text-muted"></i><br><strong style="font-size:100%;">${result.mothlyTotal.toLocaleString('en-US')}</strong></div> 
            `;
            blog_total_count.innerHTML += `
                <div class="mb-0 h4"><span class="text-muted">블로그</span> | <strong style="font-size:100%;">${result.blog_total_count.toLocaleString('en-US')}</strong></div>    
                <hr>
                <div class="mb-0 h4"><span class="text-muted">지식iN</span> | <strong style="font-size:100%;">${result.knin_total_count.toLocaleString('en-US')}</strong></div>                    
            `;
            keyword_rating.innerHTML += `
                <h1 class="text-danger"><strong>${result.keywordRating}</strong></h1>
            `;
            
            for (var i = 0; i < result.keyword_search_lists.length; i++) {
                relkeyword_table.insertAdjacentHTML('beforeend', `
                <tr>
                    <th scope="row">${i+1}</th>
                    <td><a href="/search-l2/${result.keyword_search_lists[i].relKeyword}"><strong>${result.keyword_search_lists[i].relKeyword}</strong></a></td>
                    <td>${result.keyword_search_lists[i].monthlyPcQcCnt.toLocaleString('en-US')}</td>
                    <td>${result.keyword_search_lists[i].monthlyMobileQcCnt.toLocaleString('en-US')}</td>
                </tr>    

                `)
            }
            if(result.keyword_search_lists.length<1){
                relkeyword_table_main.insertAdjacentHTML('afterend', `
                    <h3><i class="fas fa-exclamation-triangle text-warning"></i> 연관검색어를 찾을 수 없습니다</h3>
                `)
            }
        searchTrend_renderChart(result.period, result.trend, result.trend_mobile)
        searchTrendYear_renderChart(result.period_year, result.trend_year)
        setTimeout(getHistoryCount, 50);
    })
}

function search_fetch_mobile(){
    fetch('search', {
        body: JSON.stringify({ textVal: textVal }),
        method: "POST",
        })
        .then((res) => res.json())
        .then((result) => {
            spinner.classList.add('no-display');
            content.style.visibility = 'visible';
            search_input_bx.style.visibility = 'visible';
            monthlyPcQcCnt_mobile.innerHTML += `
                <div class="text-muted">PC</div>
                <div class="h5"><strong>${result.monthlyPcQcCnt.toLocaleString('en-US')}</strong></div>
            `;
            monthlyMobileQcCnt_mobile.innerHTML += `
                <div class="text-muted">Mobile</div>
                <div class="h5"><strong>${result.monthlyMobileQcCnt.toLocaleString('en-US')}</strong></div>
            `;
            mothlyTotal_mobile.innerHTML += `
                <div class="text-muted">Total</div>
                <div class="h5"><strong>${result.mothlyTotal.toLocaleString('en-US')}</strong></div> 
            `;
            blog_total_count_mobile.innerHTML += `
                <div class="">
                    <span class="text-muted">블로그</span>
                    <div class="mt-1 mb-2 h5"><strong>${result.blog_total_count.toLocaleString('en-US')}</strong> 건 </div>
                </div>
                
                <div class="">
                    <span class="text-muted">지식iN</span>
                    <div class="mb-0 h5"><strong>${result.knin_total_count.toLocaleString('en-US')}</strong> 건 </div>
                </div>
                
            `;
            keyword_rating_mobile.innerHTML += `
                <h1 class="text-danger"><strong>${result.keywordRating}</strong></h1>
            `;
            for (var i = 0; i < result.keyword_search_lists.length; i++) {
                relkeyword_table.insertAdjacentHTML('beforeend', `
                    <tr>
                        <th scope="row">${i+1}</th>
                        <td style="font-size:80%;"><a href="/search-l2/${result.keyword_search_lists[i].relKeyword}"><strong>${result.keyword_search_lists[i].relKeyword}</strong></a></td>
                        <td>${result.keyword_search_lists[i].monthlyPcQcCnt.toLocaleString('en-US')}</td>
                        <td>${result.keyword_search_lists[i].monthlyMobileQcCnt.toLocaleString('en-US')}</td>
                    </tr>
                `)
            }
        searchTrend_renderChart2(result.period, result.trend, result.trend_mobile)
        searchTrendYear_renderChart2(result.period_year, result.trend_year)
    })
}

function search_fetch_del_desktop(){
    monthlyPcQcCnt_desktop.innerHTML = ``;
    monthlyMobileQcCnt_desktop.innerHTML = ``;
    mothlyTotal_desktop.innerHTML = ``;
    blog_total_count.innerHTML = ``;
    keyword_rating.innerHTML = ``;
    relkeyword_table.innerHTML=``;
}

function search_fetch_del_mobile(){
    monthlyPcQcCnt_mobile.innerHTML = ``;
    monthlyMobileQcCnt_mobile.innerHTML = ``;
    mothlyTotal_mobile.innerHTML = ``;
    blog_total_count_mobile.innerHTML = ``;
    keyword_rating_mobile.innerHTML = ``;
    relkeyword_table.innerHTML=``;
}

const searchTrend_renderChart = (labels, datas, datas_mobile)=>{
    var ctx = document.getElementById('searchTrendChart_desktop');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label:'전체 검색량',
                data: datas,
                fill:false,
                backgroundColor: [
                    // 'rgba(255, 99, 132, 0.2)',
                    // 'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    // 'rgba(75, 192, 192, 0.2)',
                    // 'rgba(153, 102, 255, 0.2)',
                    // 'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    // 'rgba(255, 99, 132, 1)',
                    // 'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    // 'rgba(75, 192, 192, 1)',
                    // 'rgba(153, 102, 255, 1)',
                    // 'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 2
            },      
            {
                label:'모바일 검색량',
                data: datas_mobile,
                fill:false,
                backgroundColor: [
                    // 'rgba(255, 99, 132, 0.2)',
                    // 'rgba(54, 162, 235, 0.2)',
                    // 'rgba(255, 206, 86, 0.2)',
                    // 'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    // 'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    // 'rgba(255, 99, 132, 1)',
                    // 'rgba(54, 162, 235, 1)',
                    // 'rgba(255, 206, 86, 1)',
                    // 'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    // 'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 2
            },
        ]
        },
        options: {
            // animations: {
            //     tension: {
            //       duration: 500,
            //       easing: 'linear',
            //       from: 1,
            //       to: 0,
            //       loop: true
            //     }
            //   },
            scales:{
                y:{
                    beginAtZero:true,
                }
            },
            plugins:{
                title : {
                    display : true,
                    text : "검색량 트렌드",
                },
                legend:{
                    display:true,
                },
            }
            
        },
    });
}
const searchTrend_renderChart2 = (labels, datas, datas_mobile)=>{
    var ctx = document.getElementById('searchTrendChart_mobile');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label:'전체 검색량',
                data: datas,
                fill:false,
                backgroundColor: [
                    // 'rgba(255, 99, 132, 0.2)',
                    // 'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    // 'rgba(75, 192, 192, 0.2)',
                    // 'rgba(153, 102, 255, 0.2)',
                    // 'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    // 'rgba(255, 99, 132, 1)',
                    // 'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    // 'rgba(75, 192, 192, 1)',
                    // 'rgba(153, 102, 255, 1)',
                    // 'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 2
            },
            {
                label:'모바일 검색량',
                data: datas_mobile,
                fill:false,
                backgroundColor: [
                    // 'rgba(255, 99, 132, 0.2)',
                    // 'rgba(54, 162, 235, 0.2)',
                    // 'rgba(255, 206, 86, 0.2)',
                    // 'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    // 'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    // 'rgba(255, 99, 132, 1)',
                    // 'rgba(54, 162, 235, 1)',
                    // 'rgba(255, 206, 86, 1)',
                    // 'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    // 'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 2
            },
        ]
        },
        options: {
            // animations: {
            //     tension: {
            //       duration: 500,
            //       easing: 'linear',
            //       from: 1,
            //       to: 0,
            //       loop: true
            //     }
            //   },
            scales:{
                y:{
                    beginAtZero:true,
                }
            },
            plugins:{
                title : {
                    display : true,
                    text : "검색량 트렌드",
                },
                legend:{
                    display:true,
                },
            }
            
        },
    });
}
const searchTrendYear_renderChart = (labels_year, datas_year)=>{
    var ctx = document.getElementById('searchTrendYearChart_desktop');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels_year,
            datasets: [{
                label:'검색량 트렌드(월별)',
                data: datas_year,
                fill:false,
                backgroundColor: [
                    // 'rgba(255, 99, 132, 0.2)',
                    // 'rgba(54, 162, 235, 0.2)',
                    // 'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    // 'rgba(153, 102, 255, 0.2)',
                    // 'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    // 'rgba(255, 99, 132, 1)',
                    // 'rgba(54, 162, 235, 1)',
                    // 'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    // 'rgba(153, 102, 255, 1)',
                    // 'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 2
            },      
        ]
        },
        options: {
            // animations: {
            //     tension: {
            //       duration: 500,
            //       easing: 'linear',
            //       from: 1,
            //       to: 0,
            //       loop: true
            //     }
            //   },
            scales:{
                y:{
                    beginAtZero:true,
                }
            },
            plugins:{
                title : {
                    display : true,
                    text : "검색량 트렌드",
                },
                legend:{
                    display:false,
                },
            }
            
        },
    });
}
const searchTrendYear_renderChart2 = (labels, datas)=>{
    var ctx = document.getElementById('searchTrendYearChart_mobile');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label:'검색량 트렌드(월별)',
                data: datas,
                fill:false,
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                ],
                borderWidth: 2
            },
        ]
        },
        options: {
            // animations: {
            //     tension: {
            //       duration: 500,
            //       easing: 'linear',
            //       from: 1,
            //       to: 0,
            //       loop: true
            //     }
            //   },
            scales:{
                y:{
                    beginAtZero:true,
                }
            },
            plugins:{
                title : {
                    display : true,
                    text : "검색량 트렌드",
                },
                legend:{
                    display:false,
                },
            }
            
        },
    });
}

// document.onload = search_fetch();

var mql = window.matchMedia("screen and (min-width: 850px)");

mql.addEventListener('change', function(e) {
    if(e.matches) {
        console.log('데스크탑 화면 입니다.');
        search_fetch_del_desktop();
        search_fetch_desktop();
        
    } else {
        console.log('모바일 화면 입니다.');
        search_fetch_del_mobile();
        search_fetch_mobile();
        
    }
});

if (window.matchMedia("(min-width: 850px)").matches) {
    console.log('데스크탑 화면 입니다.');
    search_fetch_del_desktop();
    search_fetch_desktop();
} else {
    console.log('모바일 화면 입니다.');
    search_fetch_del_mobile();
    search_fetch_mobile();
}




















// function search_fetch_desktop(){
//     fetch('search', {
//         body: JSON.stringify({ textVal: textVal }),
//         method: "POST",
//         })
//         .then((res) => res.json())
//         .then((result) => {
//             spinner.classList.add('no-display');
//             content.style.visibility = 'visible';
//             search_input_bx.style.visibility = 'visible';
//             monthlyPcQcCnt_desktop.innerHTML += `
//                 <div class=""><i class="fas fa-desktop"></i><br><strong>${result.monthlyPcQcCnt.toLocaleString('en-US')}</strong></div>
//             `;
//             monthlyMobileQcCnt_desktop.innerHTML += `
//                 <div class=""><i class="fas fa-mobile-alt"></i><br><strong>${result.monthlyMobileQcCnt.toLocaleString('en-US')}</strong></div>
//             `;
//             mothlyTotal_desktop.innerHTML += `
//                 <div class=""><i class="fas fa-equals"></i><br><strong>${result.mothlyTotal.toLocaleString('en-US')}</strong></div> 
//             `;
//             blog_total_count.innerHTML += `
//                 <div class="mb-0 h4">월간 : <strong>${result.blog_month_count.toLocaleString('en-US')}</strong> 건 </div>
//                 <hr>
//                 <div class="mb-0 h4">전체 : <strong>${result.blog_total_count.toLocaleString('en-US')}</strong> 건 </div>
//             `;
//             if (result.keywordRating > 1) {
//                 keyword_rating.innerHTML += `
//                 <h1 class="text-success"><strong>AAA</strong></h1>
//                 `
//             }
//             else if (result.keywordRating > 0.5) {
//                 keyword_rating.innerHTML += `
//                 <h1 class="text-success"><strong>BBB</strong></h1>
//             `
//             }
//             else if (result.keywordRating > 0.1) {
//                 keyword_rating.innerHTML += `
//                 <h1 class="text-success"><strong>CCC</strong></h1>
//                 `
//             }
//             else {
//                 keyword_rating.innerHTML += `
//                 <h1 class="text-success"><strong>DDD</strong></h1>
//                 `
//             }
//             for (var i = 0; i < result.keyword_search_lists.length; i++) {
//                 relkeyword_table.insertAdjacentHTML('beforeend', `
//                     <tr>
//                         <th scope="row">${i}</th>
//                         <td><a href="/search-l2/${result.keyword_search_lists[i].relKeyword}">${result.keyword_search_lists[i].relKeyword}</a></td>
//                         <td>${result.keyword_search_lists[i].monthlyPcQcCnt.toLocaleString('en-US')}</td>
//                         <td>${result.keyword_search_lists[i].monthlyMobileQcCnt.toLocaleString('en-US')}</td>
//                     </tr>

//             `)
//         }
//         const [labelsPC, dataPC, labelsMOBILE, dataMOBILE]=[Object.keys(result['searchPCMomentum']), Object.values(result['searchPCMomentum']), Object.keys(result['searchMOBILEMomentum']), Object.values(result['searchMOBILEMomentum'])]
//         const [labelsPub, dataPub]=[Object.keys(result['pubAmountTotalMomentum']), Object.values(result['pubAmountTotalMomentum'])]
//         searchAmount_renderChart(labelsPC, dataPC, labelsMOBILE, dataMOBILE);
//         searchAmount_renderChart2(labelsPub, dataPub);
//     })
// }