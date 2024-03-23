<template>
    <div class="fireAnalysis">
        <!-- Top content -->
        <div class="top_content">
            <h2>fireAnalysis</h2>
            <div class="date_time">
                <div class="date">
                    <img src="../assets/Icon/Date.svg" class="icons" />
                    <p>{{ currentDate }}</p>
                </div>
                <div class="time">
                    <img src="../assets/Icon/time.svg" class="icons" />
                    <p>{{ currentTime }}</p>
                </div>
            </div>
        </div>
        <!-- Main content -->
        <div class="main_content">
            <!--detectiont -->
            <div class="detection">
                <div class="detecCard">
                    <h2>RGB Detection</h2>
                    <div class="result">
                        <!-- <img src="../assets/result/rgb_Detection.jpg" style="width: 640px; height: 420px;"> -->
                        <img style="-webkit-user-select: none;" src="http://localhost:5000/rgb_feed" width="760"
                            height="430">
                    </div>
                </div>
                <div class="velueTopredic">
                    <div class="inputLaLong">
                        <div class="title">
                            <h2>Location</h2>
                        </div>
                        <div class="buttonLaLong">
                            <p>Latitude:</p>
                            <input class="latitude" ref="latitudeInput" @change="updateMarkerPosition"
                                style="height: 32px;" />
                            <p>Longtitude:</p>
                            <input class="longtitude" ref="longitudeInput" @change="updateMarkerPosition"
                                style="height: 32px;" />
                            <div class="getLocation">
                                <button @click="goToLocation">Go Location</button>
                            </div>
                        </div>
                    </div>
                    <div class="inputWildTime">
                        <div class="wildbutton">
                            <p>Type of Wild</p>
                            <select v-model="selectedWildOption" style="width: 350px; height: 35px;">
                                <option v-for="option in wildOptions" :key="option.value" :value="option.value">
                                    {{ option.text }}
                                </option>
                            </select>
                        </div>
                        <div class="timebutton">
                            <p>Time to Prediction</p>
                            <!-- <select v-model="selectedTimeOption" @change="handleChangeWild" style="width: 350px;
				        height: 35px;">
                                <option v-for="option in timeOptions" :key="option.value" :value="option.value">
                                    {{ option.text }}
                                </option>
                            </select> -->
                            <select v-model="selectedTimeOption" style="width: 350px; height: 35px;">
                                <option v-for="option in timeOptions" :key="option.value" :value="option.value">
                                    {{ option.text }}
                                </option>
                            </select>
                        </div>
                        <div class="buttonPredic">
                            <button @click="handlePredictionButtonClick">Prediction</button>
                        </div>
                    </div>

                </div>
            </div>

            <div class="predicFire">
                <div class="title">
                    <h2>Fire Prediction</h2>
                </div>
                <div class="showResult">
                    <div class="predicResult">
                        <!-- <img src="../assets/result/Figure_1.png" style="width: 700px; height: 540px;"> -->
                        <div ref="map" style="height: 430px;"></div>
                    </div>
                    <div class="paraPredic">
                        <div class="fireDenger">
                            <p>Fire Danger Lavel</p>
                            <div class="level">
                                <div class="box-container">
                                    <div class="box" style="background-color: #1FA45C;"></div>
                                    <div class="text">Low</div>
                                </div>
                                <div class="box-container">
                                    <div class="box" style="background-color: #85EE1D;"></div>
                                    <div class="text">Moderate</div>
                                </div>
                                <div class="box-container">
                                    <div class="box" style="background-color: #FFD809;"></div>
                                    <div class="text">High</div>
                                </div>
                                <div class="box-container">
                                    <div class="box" style="background-color: #FB8800;"></div>
                                    <div class="text">Very High</div>
                                </div>
                                <div class="box-container">
                                    <div class="box" style="background-color: #EE1D42;"></div>
                                    <div class="text">Extreme</div>
                                </div>
                            </div>
                        </div>
                        <div class="forPrediction">
                            <p>Fire Danger Lavel In map</p>
                            <img src="http://localhost:5000/fire_analysis_feed" style="width: 380px; height: 260px;">
                        </div>
                    </div>

                </div>

            </div>
        </div>

    </div>
</template>
<script>
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
export default {
    name: 'LeafletMap',
    data() {
        return {
            currentDate: '',
            currentTime: '',
            selectedTime: '',
            selectedWildOption: "", // Initially selected option for wild type
            selectedTimeOption: "", // Initially selected option for time
            wildOptions: [
                { text: "Deciduous forest", value: "deciduous_forest" },
                { text: "Pine forest", value: "pine_forest" },
                { text: "Meadow", value: "meadow" },
                { text: "Forest garden", value: "forest_garden" }
            ],
            timeOptions: [
                { text: "5 min", value: "5_min" },
                { text: "10 min", value: "10_min" },
                { text: "15 min", value: "15_min" },
                { text: "20 min", value: "20_min" }
            ],

        }
    },

    created() {
        setInterval(this.getNow, 1000);
    },

    methods: {
        getNow: function () {
            const today = new Date();
            const date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
            const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            const currentDate = date;
            const currentTime = time;
            this.currentDate = currentDate;
            this.currentTime = currentTime;
        },


        handleChange(event) {
            console.log("Selected option:", event.target.value);
        },
        handlePredictionButtonClick() {
            // Send HTTP request to server.py for prediction
            fetch('/perform-prediction', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    selectedWildOption: this.selectedWildOption,
                    selectedTimeOption: this.selectedTimeOption
                })
            })
                .then(response => {
                    if (response.ok) {
                        console.log('Prediction request sent to server successfully');
                    } else {
                        console.error('Failed to send prediction request to server');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        },

        updateMarkerPosition() {
            const latitude = parseFloat(this.$refs.latitudeInput.value);
            const longitude = parseFloat(this.$refs.longitudeInput.value);
            if (!isNaN(latitude) && !isNaN(longitude)) {
                this.marker.setLatLng([latitude, longitude]);
                this.circleL.setLatLng([latitude, longitude]);
                this.map.setView([latitude, longitude]);
            }
        },


        sendSelectedValue() {
            // Send HTTP request to server.py with selected value 
            fetch('/update-time', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ selectedTime: this.selectedTime })
            })
                .then(response => {
                    if (response.ok) {
                        console.log('Value sent to server successfully');
                    }
                    else {
                        console.error('Failed to send value to server');
                    }
                }).catch(error => { console.error('Error:', error); });
        }
    },
    mounted() {
        // Create a map instance
        this.map = L.map(this.$refs.map).setView([13.7292423, 100.7754499], 13);

        // Add a tile layer to the map
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(this.map);

        // Create marker and store it in a component property
        this.marker = L.marker([13.7292423, 100.7754499]).addTo(this.map);

        this.circleL = L.circle([13.7292423, 100.7754499], {
            color: ' #EE1D42',
            fillColor: ' #EE1D42',
            fillOpacity: 0.5,
            radius: 500
        }).addTo(this.map);


        // Reverse geocode the default position (if needed)
        this.reverseGeocode(13.7292423, 100.7754499);
    }
}


</script>
<style>
.fireAnalysis {

    display: flex;
    flex-direction: column;
    margin-left: 240px;

    .top_content {
        height: 80px;
        width: 1680px;
        padding: 20px 30px 20px 20px;
        display: flex;
        flex-direction: row;
        background-color: var(--light);
        align-items: center;
        justify-content: space-between;

        .date_time {
            display: flex;
            gap: 30px;

            .date,
            .time {
                font-size: 20px;
                display: flex;
                gap: 8px;
                align-items: center;
            }

        }
    }

    .main_content {
        display: flex;
        flex-direction: row;
        margin: 20px;
        gap: 20px;

        .detection {
            display: flex;
            flex-direction: column;
            gap: 20px;

            .detecCard {
                background-color: var(--light);
                width: 800px;
                height: 500px;
                padding: 20px;
                border-radius: 12px;

                .result {
                    display: flex;
                    margin-top: 6px;
                    gap: 10px;
                    justify-content: center;
                }
            }
        }

        .velueTopredic {
            display: flex;
            gap: 20px;

            .inputWildTime {
                flex-direction: column;
                background-color: var(--light);
                width: 390px;
                height: 300px;
                border-radius: 12px;
                padding: 20px;
                font-size: 14px;

                .wildbutton {
                    margin-bottom: 20px;
                }

                select {
                    margin-top: 10px;
                    gap: 10px;
                    background-color: var(--light);
                    border-radius: 6px;
                }

                option {
                    font-size: 14px;
                    padding: 12px;

                }

            }

            .inputLaLong {
                width: 390px;
                height: 300px;
                background-color: var(--light);
                display: flex;
                flex-direction: column;
                border-radius: 12px;
                padding: 20px;

                .title {
                    margin-bottom: 10px;
                }

                .buttonLaLong {
                    display: flex;
                    flex-direction: column;
                    gap: 5px;
                    border-radius: 12px;

                    input {
                        height: 60px;
                    }

                }
            }

            .buttonPredic {
                display: flex;
                width: 100px;
                height: 40px;
                padding: 12px;
                border-radius: 8px;
                margin: 100px 0px 0px 240px;
                background-color: var(--grey);
                justify-content: center;

                &:hover {
                    background-color: var(--primary);
                    color: var(--light);
                }
            }

            .getLocation {
                width: 100px;
                height: 40px;
                padding: 12px;
                border-radius: 8px;
                margin: 60px 0px 0px 240px;
                background-color: var(--grey);

                &:hover {
                    background-color: var(--primary);
                    color: var(--light);
                }
            }

        }

        .predicFire {
            width: 820px;
            height: 820px;
            background-color: var(--light);
            border-radius: 12px;
            padding: 20px;

            .predicResult {
                margin-top: 20px;
            }

            .paraPredic {
                display: flex;
                justify-content: space-between;

                .fireDenger {
                    margin-top: 20px;
                    font-size: 18px;

                    .level {
                        display: flex;
                        flex-direction: column;
                        margin-top: 10px;
                        gap: 15px;
                    }

                    .box-container {
                        display: flex;
                        align-items: center;
                    }

                    .box {
                        width: 10px;
                        height: 10px;
                    }

                    .text {
                        color: var(--dark);
                        font-size: 18px;
                        margin-left: 4px;
                    }

                }

                .forPrediction {
                    margin-top: 20px;
                    gap: 20px
                }



            }

        }

    }
}
</style>
