(function () {

	function transformRawDataForChart(rawData, date) {

		const viewOption = {
			"Количество брака": {
				label: "Количество брака",
				backgroundColor: 'rgba(0, 191, 255, 0.2)',
				borderColor: '#B0E0E6',
				borderWidth: 4,
				xAxisID: "bar-x-axis1",
			},
			"Количество годных": {
				label: "Количество годных",
				backgroundColor: 'rgba(65, 105, 225, 0.2)',
				borderColor: '#00BFFF',
				borderWidth: 4,
				xAxisID: "bar-x-axis1",
			},
			"Количество неопределённых": {
				label: "Количество неопределённых",
				backgroundColor: 'rgba(72, 209, 204, 0.2)',
				borderColor: '#B0E0E6',
				borderWidth: 4,
				xAxisID: "bar-x-axis1",
			},
			"Общее количество Обработанных труб": {
				label: "Общее количество Обработанных труб",
				backgroundColor: 'rgba(153, 50, 204, 0.3)',
				borderColor: '#9932CC',
				borderWidth: 4,
				xAxisID: "bar-x-axis2",
			},
		}

		function prepareDate(inputDate) {
			const date = new Date(inputDate)
			let month = date.getMonth() + 1;
			if (month < 10) {
				month = '0' + month;
			}
			let day = date.getDate();
			if (day < 10) {
				day = '0' + day;
			}
			return day + '/' + month + '/' + date.getFullYear()
		}

		const searchDate = prepareDate(date);

		console.log(searchDate)

		let dataDaily;
		for (let index = 0; index < rawData.length; index++) {
			const element = rawData[index]
			if (element[searchDate]) {
				dataDaily = element[searchDate]
			}
		}

		dataDaily = dataDaily[0]


		const dataForChar = {}
		const labels = [];
		for (const factoryName in dataDaily) {

			labels.push(factoryName)

			const summData = {}
			if (Object.hasOwnProperty.call(dataDaily, factoryName)) {
				const factoryDataArray = dataDaily[factoryName];

				for (let index = 0; index < factoryDataArray.length; index++) {
					const factoryData = factoryDataArray[index];

					for (const dataKey in factoryData) {

						if (Object.hasOwnProperty.call(factoryData, dataKey)) {

							if (dataKey == "id") {
								continue;
							}

							const value = factoryData[dataKey];

							if (Number.isInteger(value)) {
								if (summData[dataKey] === undefined) {
									summData[dataKey] = 0
								}
								summData[dataKey] += value

							}
						}
					}
				}
			}

			for (const key in summData) {
				if (Object.hasOwnProperty.call(summData, key)) {
					const value = summData[key];
					if (dataForChar[key] === undefined) {
						dataForChar[key] = []
					}
					dataForChar[key].push(value)
				}
			}

		}

		let datasets = []
		for (const key in viewOption) {
			if (Object.hasOwnProperty.call(viewOption, key)) {
				const value = viewOption[key];
				value.data = dataForChar[key]
				datasets.push(value)
			}
		}

		const dataChart = {}
		dataChart.labels = labels
		dataChart.datasets = datasets

		console.log('dataChart', dataChart)

		return dataChart
	}

	function updateChart(dataChart) {

		var ctx = document.getElementById("my89Chart").getContext("2d");
		var myBarChart = new Chart(ctx, {
			type: 'bar',
			data: dataChart,
			options: {
				scales: {
					xAxes: [{
						stacked: true,
						id: "bar-x-axis1",
						barThickness: 30,
					}, {
						display: false,
						stacked: true,
						id: "bar-x-axis2",
						barThickness: 70,
						type: 'category',
						categoryPercentage: 0.8,
						barPercentage: 0.9,
						gridLines: {
							offsetGridLines: true
						},
						offset: true
					}],
					yAxes: [{
						stacked: false,
						ticks: {
							beginAtZero: true
						},
					}]
				}
			}
		});
	}

	function loadDataByDate(date) {

		const form = document.querySelector("#form");
		var data = new FormData(form);


		fetch('static/example.json')
		    .then((res) => {
		        console.log(res.json());
		    })

            .then((out) => {
                console.log(out);
//                let listOfFactory = [];
//
//                for(const values of Object.values(elem))
//                {
//                    for(const x of Object.values(values))
//                    {
//                        for(const [k, n ] of Object.entries(x))
//                        {
//                        listOfFactory.push(k);
//                        console.log(k);
//                        console.log(n);
//                            for(const z of Object.values(n))
//                            {
////                                if(z['Общее количество Обработанных труб'])
////                                {
////                                    const m = z['Общее количество Обработанных труб'];
////                                    console.log(m);
////                                }
//
//                            }
//                        }
//                    }
//                }
//                console.log(listOfFactory);
            })

		    .catch((err) => {
		        console.log(err);
		    })
	}

	function initDate(inputDate) {
		function formatDate(date) {
			var d = new Date(date),
				month = '' + (d.getMonth() + 1),
				day = '' + d.getDate(),
				year = d.getFullYear();

			if (month.length < 2)
				month = '0' + month;
			if (day.length < 2)
				day = '0' + day;

			return [year, month, day].join('-');
		}
		const defaultDate = formatDate(new Date()); // Текущая дата 2021-12-10
		inputDate.value = defaultDate;
		var event = new Event('change');
		inputDate.dispatchEvent(event);

	}

	const inputDate = document.querySelector("#id_date");
	inputDate.addEventListener("change", function (event) {
		const date = event.target.value; // 2021-12-10
		loadDataByDate(date);
//		console.log(date);
	});


	initDate(inputDate)

})();
