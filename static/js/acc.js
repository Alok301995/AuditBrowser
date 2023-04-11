import { get_attributes } from "../js/main.js";
let attributes = {};
attributes = get_attributes();

let data_point = [];
let data_display = document.getElementById("data");


// FUNCTIONS

function handleMotion(event) {
    data_point.push([
    event.acceleration.x,
    event.acceleration.y,
    event.acceleration.z,
    ]);
}

// function handleOrientation(event) {

//     data_point.push([
//     event.alpha,
//     event.beta,
//     event.gamma,
//     ]);
// }


// END OF FUNCTIONS


// if (
//     DeviceMotionEvent &&
//     typeof DeviceMotionEvent.requestPermission === "function"
// ) {
//     DeviceMotionEvent.requestPermission();
// }


window.addEventListener("devicemotion", handleMotion);
window.addEventListener("deviceorientation", handleOrientation);

attributes["accelerometer"] = data_point;

let testButton = document.getElementById('test-button');
let loader = document.getElementById('loader');
let buttonText = document.getElementById('button-text');
let boiContainer = document.getElementById('boi-container');
let info_1_p = document.getElementById('info-1-p');
let info_2_p = document.getElementById('info-2-p');
let chartContainer = document.getElementById('chart-container');
let statsContainer = document.getElementById('stats-container');
let hamNav = document.getElementById('ham-nav');
let hamMenu = document.getElementById('ham-menu');
let statsDiv = document.getElementById('stats-div');
let deskBoi = document.getElementById('desk-boi');
let mobileBoi = document.getElementById('mob-boi');



let clicked = false;
let hamClicked = false;
hamMenu.addEventListener('click', (event) => {
    event.preventDefault();
    
    if (!hamClicked) {
    hamClicked = true;
    hamNav.classList.remove('hidden');
    hamNav.classList.add("opacity-100");
    }
    else {
    hamClicked = false;
    hamNav.classList.add('hidden');
    hamNav.classList.remove("opacity-0");
    }


});




testButton.addEventListener('click', (event) => {
    event.preventDefault();

    if (!clicked) {
    clicked = true;
    loader.classList.remove('hidden');
    buttonText.classList.add('hidden');

    setTimeout(async () => {
        window.removeEventListener("devicemotion", handleMotion);
        attributes["accelerometer"] = data_point;
        console.log(attributes)


        // After loading data boiContainer will be shown and 
        boiContainer.classList.remove("hidden");
        info_1_p.classList.add("hidden");
        info_2_p.classList.add("hidden");
        chartContainer.classList.remove("hidden");
        statsContainer.classList.remove("hidden");


        const response = await fetch('/api/fetch_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Allow-Control-Allow-Origin': '*', // Required for CORS support to work
        },
        body: JSON.stringify(attributes)
        });

        const data = await response.json();

        // if status is true then data is returned and information is displayed

        if (data.status) {
        // create apex chart

        let desk_boi = data['data']['desktop']['bits_of_info'];
        let mobile_boi = data['data']['mobile']['bits_of_info'];

        deskBoi.innerText = desk_boi;
        mobileBoi.innerText = mobile_boi;




        let ctx = document.getElementById('chart');
        let cat = [];
        let dat = [];
        
        data['data']['attributes'].sort(function (a, b) {
            return b.bits_of_info - a.bits_of_info;
        });

        for (let i = 0; i < data['data']['attributes'].length; i++) {
            cat.push(data['data']['attributes'][i]['attribute']);
            dat.push(data['data']['attributes'][i]['bits_of_info']);
        }
        let options = {
            series: [{
            data: dat
            }],
            chart: {
            toolbar: {
                show: false
            },
            type: 'bar',
            height: 800,
            width: "100%",
            // foreColor: 'black',
            align: 'start',
            sparkline: {
                enabled: true
            },

            },
            legend: {
            show: false
            },
            plotOptions: {
            bar: {
                // columnWidth: 200,
                barHeight: '100%',
                barWidth: 100,
                distributed: true,
                horizontal: true,
                dataLabels: {
                position: 'bottom'
                },
                colors: {
                ranges: [ {
                    from: 0,
                    to: 100,
                    color: '#43A2FB'
                }],
                backgroundBarColors: ['#ECF2FF'],
                backgroundBarOpacity: 1,
                backgroundBarRadius: 5,
                },
            }
            },
            dataLabels: {
            enabled: true,
            textAnchor: 'start',
            style: {
                fontSize: '16px',
                // marginTop: '10px',
                colors: ['#5E5D5D'],
                fontFamily: 'Helvetica, Arial, sans-serif',
                fontWeight: 'medium',
                textShadow: 'none',
            },
            formatter: function (val, opt) {
                return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
            },
            offsetX: 0,
            dropShadow: {
                enabled: false
            }
            },
            stroke: {
            width: 1,
            colors: ['#ECF2FF']
            },
            xaxis: {
            categories: cat,
            },
            yaxis: {
            labels: {
                show: false
            }
            },
        };
        let chart = new ApexCharts(ctx, options);
        chart.render();




        let statsData = await data['data']['attributes']
        // remove all childs from statsDiv
        while (statsDiv.firstChild) {
            statsDiv.removeChild(statsDiv.firstChild);
        }
        for (let i = 0; i < statsData.length; i++) {

            let div = document.createElement("div");
            div.classList.add("flex", "justify-between", "px-4", "py-2");
            let span1 = document.createElement("span");
            span1.classList.add("text-[#5E5D5D]");
            let span2 = document.createElement("span");
            span2.classList.add("text-lg");
            let span3 = document.createElement("span");
            span3.classList.add("text-sm");
            span3.innerText = " Bits";
            span1.innerText = statsData[i]['attribute'];
            span2.innerText = statsData[i]['bits_of_info'];
            div.appendChild(span1);
            div.appendChild(span2);
            span2.appendChild(span3);
            statsDiv.appendChild(div);

        }
        }
        else {
        console.log("data not found");
        }



        loader.classList.add('hidden');
        buttonText.classList.remove('hidden');
        clicked = false;
    }, 5000);
    }





});