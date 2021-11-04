chartFunc = {
    barChart: (el, data, labels) => {
        var myChart = new Chart(el, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: "",
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: false,
                    },
                    //   subtitle: {
                    //       display: true,
                    //       text: 'Custom Chart Subtitle'
                    //   },
                    //   title: {
                    //       display: true,
                    //       text: 'Custom Chart Title'
                    //   },

                    tooltip: {
                        callbacks: {
                            labelColor: function(context) {

                                return {
                                    borderColor: 'rgb(0, 0, 255)',
                                    backgroundColor: '#fff',
                                    borderWidth: 0,
                                    //  borderDash: [6, 6],
                                    borderRadius: 2,
                                };
                            },
                            labelTextColor: function(context) {
                                return '#fff';
                            },
                            labelPointStyle: function(context) {
                                return {
                                    pointStyle: 'square',
                                    rotation: 20
                                };
                            }
                        }
                    }
                },


                scales: {
                    y: {
                        beginAtZero: true,
                        suggestedMax: 15,
                        ticks: {
                            stepSize: 2
                        }
                    },
                }
            }
        });
    },

    doughnutChart: (el, data, labels, destroy = false) => {
        var pie = () => {
            var myChart = new Chart(el, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
                        hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
                        hoverBorderColor: "rgba(234, 236, 244, 1)",
                    }],
                },
                options: {
                    cutout: 95,
                    maintainAspectRatio: false,
                    tooltips: {
                        backgroundColor: "rgb(255,255,255)",
                        bodyFontColor: "#858796",
                        borderColor: '#dddfeb',
                        borderWidth: 1,
                        xPadding: 15,
                        yPadding: 15,
                        displayColors: false,
                        caretPadding: 10,
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: { enabled: true },
                    },
                },
            });
            return myChart
        }

        pie()
    },

    pieChart: (el, data, labels, destroy = false) => {
        var pie = () => {
            var myChart = new Chart(el, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: '# of Tomatoes',
                        data: data,
                        backgroundColor: [
                            '#7928ca',
                            '#17ad37',
                            '#2152ff',
                        ],
                        //   borderColor: [
                        //       'rgba(255,99,132,1)',
                        //       'rgba(54, 162, 235, 1)',
                        //       'rgba(255, 206, 86, 1)',
                        //       'rgba(75, 192, 192, 1)'
                        //   ],
                        //   borderWidth: 1
                    }]
                },
                options: {
                    cutoutPercentage: 40,
                    //   responsive: true,
                    //maintainAspectRatio: true,

                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: { enabled: true },
                    }
                }
            });
            return myChart
        }

        pie()
    },

    groupedBar: (el, set1, set2, lbl1, lbl2) => {
        var gbarChart = new Chart(el, {
            type: 'bar',
            data: {
                labels: ["1900", "1950", "1999", "2050"],
                datasets: [{
                    label: "Africa",
                    backgroundColor: "#3e95cd",
                    data: [133, 221, 783, 2478]
                }, {
                    label: "Europe",
                    backgroundColor: "#8e5ea2",
                    data: [408, 547, 675, 734]
                }]
            },
            options: {
                title: {
                    display: true,
                    text: 'Population growth (millions)'
                },
                plugins: {
                    legend: {
                        display: false,
                    }
                },

                scales: {
                    y: {
                        beginAtZero: true,
                        suggestedMax: 3000,
                        ticks: {
                            stepSize: 200
                        }
                    },
                }

            }
        });

    },

    lineMixedChart: (el) => {
        var linechart = new Chart(el, {
            type: 'line',
            data: {
                labels: [1500, 1600, 1700, 1750, 1800, 1850, 1900, 1950, 1999, 2050],
                datasets: [{
                    data: [86, 114, 106, 106, 107, 111, 133, 221, 783, 2478],
                    label: "Africa",
                    borderColor: "rgba(255, 99, 132, 1)",
                    fill: false
                }, {
                    data: [282, 350, 411, 502, 635, 809, 947, 1402, 3700, 5267],
                    label: "Asia",
                    borderColor: "rgba(54, 162, 235, 1)",
                    fill: false
                }, {
                    data: [168, 170, 178, 190, 203, 276, 408, 547, 675, 734],
                    label: "Europe",
                    borderColor: "rgba(255, 206, 86, 1)",
                    fill: false
                }, {
                    data: [40, 20, 10, 16, 24, 38, 74, 167, 508, 784],
                    label: "Latin America",
                    borderColor: "rgba(75, 192, 192, 1)",
                    fill: false
                }, {
                    data: [6, 3, 2, 2, 7, 26, 82, 172, 312, 433],
                    label: "North America",
                    borderColor: "rgba(153, 102, 255, 1)",
                    fill: false
                }]
            },
            options: {
                plugins: {
                    title: {
                        display: false,
                        text: 'World population per region (in millions)'
                    }
                },
            }
        });

    },
}


sync = {
    constArr: ['get_full_name'],


    getCookie: (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },


    isEmpty: obj => {
        if (obj == null) return true;
        if (obj === undefined) return true;
        if (obj.length === 0) return true;
        if (!obj.length > 0) return true;
        for (var key in obj) {
            if (!obj.hasOwnProperty(prop)) return true;
        }
        return true;
    },


    ws: () => {
        let http = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        var socket = new WebSocket(http + window.location.host + window.location.pathname);
        return socket
    },

    scrollToLast: (el) => {
        let div;
        const scrollIntoViewOptions = { behavior: "smooth", block: "end", inline: "center" };
        if (fn.select('#chat__page')) {
            div = fn.select("#chat__page").lastElementChild;
        }

        let e = div || el;
        if (e) {
            e.scrollIntoView(scrollIntoViewOptions);
            return
        }

    },


    socket: (reload = false, requestUser = null) => {
        let ws = sync.ws()

        if (reload) {
            $(fn.select("#users__pie")).remove();
            $(fn.select('#online')).remove();
            $(fn.select('div#pie__chart')).append(`<canvas id ="users__pie" data-url="/user/api/chart/data/"> </canvas>`)
            $(fn.select('table#tables')).append(`<tbody id="online" class="table online" data-url="/user/api/logs/data/"></tbody>`);
        }

        const deleteWeb = e => {
            data = {
                'id': parseInt(e.target.value),
                'delete_temp': true,
            }
            ws.send(JSON.stringify(data));
        }

        window.addEventListener('load', (event) => {
            if (fn.select('#chat__form')) fn.select('#chat__form').reset();
            sync.scrollToLast();
        });

        function connect() {
            ws.onopen = function(e) {
                console.log("Socket is open");

                const updatePieChart = () => {
                    $.ajax({
                        url: $("#users__pie").attr("data-url"),
                        dataType: 'json',
                        success: obj => {
                            sync.updatePieChartOnLoad(obj, true)
                        }
                    });

                }

                const updateUsersTable = () => {
                    $.ajax({
                        url: $("#online").attr("data-url"),
                        dataType: 'json',
                        success: obj => {
                            sync.updateUsersTableOnLoad(obj, true)
                        }
                    });
                }

                fn.on('keypress', "#id_message", e => {
                    e = e || window.event;
                    let charCode = null;
                    charCode = (typeof e.which == "number") ? e.which : e.keyCode;
                    const typing_data = {
                        "delete": false,
                        'create': false,
                        'update': false,
                        'typing': true,
                        'user': requestUser,
                    }
                    if (charCode) ws.send(JSON.stringify(typing_data))
                });

                fn.on('click', "[data-delete='deleteChat']", e => {
                    //   console.log(e.target.value);
                    const delete_data = {
                        "delete": true,
                        'create': false,
                        'update': false,
                        'typing': false,
                        'user': requestUser,
                        'uuid': e.target.value
                    }
                    console.log(delete_data);
                    ws.send(JSON.stringify(delete_data));
                }, true)

                fn.on('click', "[data-edit='editChat']", e => {
                    return sync.editChatMessage(e.target)
                }, true);

                fn.on('submit', '#update_chat__form', e => {
                    e.preventDefault();
                    let picker = ['message', 'uuid']
                    const update_data = {
                        "update": true,
                        'create': false,
                        'delete': false,
                        'typing': false,
                        'user': requestUser,
                    }
                    let form = e.target

                    for (var i = 0; i < form.elements.length; i++) {
                        let el = form.elements[i];
                        if (picker.includes(el.name)) {
                            update_data[el.name] = el.value;
                        }
                    }
                    // console.log('sendupdate', update_data)
                    ws.send(JSON.stringify(update_data));
                    fn.select('#update_chat__form').reset()
                });

                fn.on('reset', "#update_chat__form", e => {
                    if (fn.select('#update_chat__form')) {
                        fn.select('#chat__form').style.display = 'block';
                        fn.select('#update_chat__form').style.display = 'none';
                    }

                });

                fn.on('submit', '#chat__form', e => {
                    e.preventDefault();
                    let uuid = sync.generateUUID()
                    const message_data = {
                            'uuid': uuid,
                            'message': fn.select('#id_message').value,
                            'user': requestUser,
                            "create": true,
                            'update': false,
                            'delete': false,
                            'typing': false,
                        }
                        //   console.log(message_data)
                    ws.send(JSON.stringify(message_data));
                    fn.select('#chat__form').reset()
                });

                if (fn.select('#dashboard__page')) {
                    updatePieChart();
                    updateUsersTable();
                }

                if (fn.select("#del__content")) {
                    fn.select("#del__content", true).forEach(element => {
                        element.addEventListener('click', deleteWeb)
                    });
                }

                reload = false;
            }
            ws.onmessage = function(e) {
                let data = JSON.parse(e.data);
                // console.log("Socket on message", data);
                if (data.chart) {
                    let data = JSON.parse(e.data).data;
                    sync.updatePieChartOnLoad(data, true);
                }

                if (data.users) {
                    let data = JSON.parse(e.data).data;
                    sync.updateUsersTableOnLoad(data, true, requestUser);
                }

                if (data.delete_temp) {
                    fn.select("#del__content", true).forEach(element => {
                        let el = element.value === data.id.toString() ? element : null;
                        if (el) {
                            el.parentElement.parentElement.style.backgroundColor = '#00000034';
                            el.parentElement.innerHTML = data.msg;
                        }
                    });
                }

                if (data.create) {
                    sync.createChatMessage(data, requestUser);
                }

                if (data.delete) {
                    if (document.getElementById(data.uuid)) {
                        document.getElementById(data.uuid).remove();
                    }
                }

                if (data.update) {
                    console.log(`[data-ctm='${data.uuid}']`);
                    fn.select(`[data-ctm='${data.uuid}']`).innerHTML = data.message
                }

                if (!data.typing) {
                    let el = fn.select(`#typing__mercury`);
                    if (data.user !== requestUser) {
                        if (el) el.classList.remove('show__typing');
                    }

                }

                if (data.typing) {
                    let el = fn.select("#typing__mercury");
                    if (data.user !== requestUser) {
                        el.classList.add('show__typing');
                        setTimeout(() => {
                            el.classList.remove('show__typing');
                        }, 5500);
                    }
                }
            }
            ws.onerror = function(e) {
                console.log("Socket on error")
            }
            ws.onclose = function(e) {
                console.log("Socket on close", )
                setTimeout(function() {
                    console.log("Socket reconnecting")
                    sync.socket(true);
                }, 1000);
            }
        }
        return connect()
    },


    generateUUID: () => {
        var d = new Date().getTime(); //Timestamp
        var d2 = (performance && performance.now && (performance.now() * 1000)) || 0; //Time in microseconds since page-load or 0 if unsupported
        var id = null,
            checker = [];
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16; //random number between 0 and 16
            if (d > 0) { //Use timestamp until depleted
                r = (d + r) % 16 | 0;
                d = Math.floor(d / 16);
            } else { //Use microseconds since page-load if supported
                r = (d2 + r) % 16 | 0;
                d2 = Math.floor(d2 / 16);
            }
            return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
    },


    sendRequest: (method, url, data) => {
        console.log(data);
        // Remember there is use of Async for best performance in the callee of this.
        //create a ne romise object then promisify the XMLHTTResuest with resolve and reject
        const promise = new Promise((resolve, reject) => {
            var xhr = new XMLHttpRequest();
            xhr.open(method, url);
            // Required by Django
            xhr.setRequestHeader('HTTP_X_REQUEST_WITH', 'XMLHttpRequest');
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            // Django needs csrf token
            xhr.setRequestHeader("X-CSRFToken", sync.getCookie("csrftoken"));
            xhr.onload = () => {
                    //We have to check for status codes here from the server then reject them or resolve
                    // However Django can be set to do that by logically handling that in the backend hence,
                    // no need to write all status codes here with if else 
                    if (xhr.status >= 400) reject(xhr.response);
                    // For the case of django returns this
                    // return JsonResponse(serialized, status=200, safe=False)
                    if (xhr.status === 200) resolve(xhr.response)
                }
                //  For failure of network connection but not from the server
            xhr.onerror = () => {
                reject('Something went wrong!')
            }

            //not neccesary. Just for testing
            // data = { 'request': 'I am requesting to delete this' }
            //we only send JSON data if we passed real data
            if (data) xhr.send(JSON.stringify(data));
            else xhr.send();
        });
        return promise
    },

    sendPaypalBackEnd: (url, dict) => {
        sync.sendRequest('POST', url, dict).then(response => {
            var data = JSON.parse(response)
            window.location.href = `${window.location.origin}/innovest-view-detail/`;
            if (data.success) {
                console.log(data);
            }

        }).catch(error => {
            console.log(error);
        });
    },

    sendPayPalPaypal: (amount) => {
        let amt = parseFloat(amount.innerHTML).toFixed(2);


        const buttons = paypal.Buttons({
            style: {
                color: 'blue'
            },
            createOrder: function(data, actions) {
                return actions.order.create({
                    purchase_units: [{
                        amount: {
                            value: amt
                        }
                    }]
                });
            },
            onApprove: function(data, actions) {
                return actions.order.capture().then(function(orderData) {
                    sync.sendRequest('POST', window.location.pathname, orderData).then(response => {
                        var datas = JSON.parse(response)
                        window.location.href = `${window.location.origin}/innovest-view-detail/`;
                    }).catch(error => {
                        console.log(error);
                    });

                });
            }
        }).render('#paypal-button-container');
        return buttons
    },

    productListApi: (url) => {

        sync.sendRequest('GET', url).then(response => {
                var data = JSON.parse(response);

                data.forEach(e => {
                    let card = `<div class="img-container"><img src="https://colorlib.com/preview/theme/seogo/img/case_study/2.png"></div>
                                <h4>${e.title}</h4><p>${e.description}</p><h6>$${e.price}.00</h6><ul><li><i class="bi-star-fill"></i></li>
                                <li><i class="bi-star-fill"></i></li><li><i class="bi-star-fill"></i></li><li><i class="bi-star-fill">
                                </i></li></ul><a class="button"href="${e.url}">Buy Now</a>`;
                    let div = document.createElement('div');
                    div.classList.add("local_product");
                    div.innerHTML = card;
                    fn.select('#products').append(div)
                })
                return data
            }).then(data => {
                // console.log(fn.select('.carousel__cards .cards', true))
            })
            .catch(error => {
                console.log(error);
            });
    },


    deleteChatMessage: (event) => {
        // event.parentElement.remove() web socket will remove the element since
        // there is a trigger for DB change singnal is listening in the back end
        sync.sendRequest('POST', event.name, { 'real data': event.name }).then(response => {
            console.log(response);
            //catch block to do something with error from server,
            // ofcourse from status code
        }).catch(error => {
            console.log(error);
        });
    },


    editChatMessage: e => {
        let update_form = fn.select('#update_chat__form');
        let update_msg = fn.select(`[data-ctm='${e.value}']`).innerHTML;
        // console.log(update_msg);
        for (var i = 0; i < update_form.elements.length; i++) {
            let el = update_form.elements[i];
            el.name == 'message' ? el.value = update_msg.trim() : null;
            el.name == 'uuid' ? el.value = e.value : null;
        }
        if (fn.select('#chat__form')) {
            fn.select('#chat__form').style.display = 'none';
            update_form.style.display = 'block';
            sync.scrollToLast(update_form);
        }
    },


    createChatMessage: (o, user) => {
        let icon = document.createElement('i');
        icon.classList.add('icon-note');
        let delBtn = document.createElement('button');
        delBtn.value = o.uuid;
        delBtn.classList.add("me-1", "btn", "btn-outline-danger", "btn-sm");
        delBtn.innerHTML = "Delete";
        delBtn.setAttribute('name', `/chat/chat-delete/${o.uuid}`);
        delBtn.onclick = function() {
            sync.deleteChatMessage(this)
        };

        let editBtn = document.createElement('button');
        editBtn.value = o.uuid;
        editBtn.classList.add("btn", "btn-outline-info", "btn-sm");

        editBtn.innerHTML = "Edit";
        editBtn.setAttribute('data-edit', 'editChat');
        editBtn.onclick = function() {
            sync.editChatMessage(this)
        };

        let p = document.createElement('p');
        p.setAttribute('data-ctm', o.uuid)
        p.append(document.createTextNode(o.message));

        let div1 = document.createElement('div');
        div1.classList.add('container', 'darker', 'annimated');
        div1.id = o.uuid;

        let div2 = document.createElement('div');
        div2.classList.add('container', 'annimated');
        div2.id = o.uuid;

        let img1 = document.createElement('img');
        img1.setAttribute('src', "/w3images/avatar_g2.jpg");
        img1.classList.add('right');

        let img2 = document.createElement('img');
        img2.setAttribute('src', "/w3images/avatar_g2.jpg");
        img2.classList.add('left');

        let span1 = document.createElement('span');
        span1.classList.add('time-left', 'me-2');
        span1.append(new Date().toLocaleTimeString());

        let span2 = document.createElement('span');
        span2.classList.add('time-right');
        span2.append(new Date().toLocaleTimeString());

        if (o.user === user) {
            div1.appendChild(img1);
            div1.appendChild(p);
            div1.appendChild(span1);
            div1.appendChild(delBtn);
            div1.appendChild(editBtn);
            fn.select('#chat__page').appendChild(div1)
        } else {
            div2.appendChild(img2);
            div2.appendChild(p);
            div2.appendChild(span2);
            fn.select('#chat__page').appendChild(div2)
        }
        sync.scrollToLast(`#${o.uuid}`);
    },


    updateUsersTableOnLoad: (o, rem = false, current_user = null) => {
        if (o.length) {
            if (rem) {
                $(fn.select('#online')).remove();
                $(fn.select('table#tables')).append('<tbody id="online" class="table online" data-url="/user/api/logs/data/"></tbody>');
                rem = false;
            }
            let t1 = fn.select('#online');
            o.forEach(obj => {
                //  console.log(o);
                if (current_user !== obj.user.username) { sync.genTable(t1, obj, obj.user.username); }
            });
        } else {
            fn.select('#no__content').firstElementChild.remove();
        }
    },


    updatePieChartOnLoad: (o, rem = false) => {
        //   console.log(o.ordinary);
        var data = Object.values(o.ordinary);
        var labels = Object.keys(o.ordinary);
        if (rem) {
            $(fn.select("#users__pie")).remove();
            $(fn.select('div#pie__chart')).append('<canvas id="users__pie" ></canvas>');
            rem = false;
        }
        chartFunc.pieChart(fn.select("#users__pie"), data, labels);
        fn.select(".chart-table .admin").innerHTML = `Admin - ${data[0]}`
        fn.select(".chart-table .staff").innerHTML = `Staff - ${data[1]}`
        fn.select(".chart-table .active").innerHTML = `Active - ${data[2]}`
    },


    genTableHead: (t, d) => {
        if (d.length) {
            let thead = t.createTHead();
            let row = thead.insertRow();
            for (let key of d) {
                if (sync.constArr.includes(key)) {
                    let th = document.createElement("th");
                    let text = document.createTextNode(key);
                    th.appendChild(text);
                    row.appendChild(th);
                }
            }
        }
    },


    genTable: (t, d, u = null) => {
        let a = document.createElement('a')
        a.innerHTML = 'Chat'
        a.setAttribute('href', `/chat/chat-me/${u}`)
        let row = t.insertRow();
        for (key in d.user) {
            if (sync.constArr.includes(key)) {
                console.log(u);
                let cell = row.insertCell();
                let text = document.createTextNode(d.user[key]);
                cell.appendChild(text);
            }
        }
        let chat = row.insertCell();
        let online = row.insertCell();
        online.classList.add('text-success')
        if (d.logged) {
            let text = document.createTextNode('online');
            online.appendChild(text);
        }
        chat.appendChild(a)
    },

}