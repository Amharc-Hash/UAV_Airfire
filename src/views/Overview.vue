<template>
    <div class="overview">
        <!-- Top content -->
        <div class="top_content">
            <h2>Overview</h2>
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
            <!-- real-time -->
            <div class="vidoStream">
                <img style="-webkit-user-select: none;" src="http://localhost:5000/video_feed" width="1240"
                    height="780">
                <!-- <video src="../assets/Videostream/HorrusStream.mp4" style="width: 1120px; height: 800px;" controls autoplay></video> -->
            </div>
            <!-- Weather-->
            <div class="weatherBar">
                <!-- temp -->
                <div class="card">
                    <img src="../assets/temp.png" alt="Card Image" class="card-image">
                    <div class="card-content">
                        <p class="card-title">Temperature</p>
                        <p class="card-value">{{ valueTemp }} c</p>
                    </div>
                </div>

                <!-- Humidity -->
                <div class="card">
                    <img src="../assets/humidity.png" alt="Card Image" class="card-image">
                    <div class="card-content">
                        <p class="card-title">Humidity</p>
                        <p class="card-value">{{ humidity }} %</p>
                    </div>
                </div>

                <!-- windSpeed -->
                <div class="card">
                    <img src="../assets/windSpeed.png" alt="Card Image" class="card-image">
                    <div class="card-content">
                        <p class="card-title">Wind Speed</p>
                        <p class="card-value">{{ windSpeed }} k/hr</p>
                    </div>
                </div>

                <!-- windDirec -->
                <div class="card">
                    <img src="../assets/compass.png" alt="Card Image" class="card-image">
                    <div class="card-content">
                        <p class="card-title">Wind Direction </p>
                        <p class="card-value">{{ windDirec }}</p>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            currentDate: 'N/A',
            currentTime: 'N/A',
            valueTemp: 'N/A',
            windSpeed: 'N/A',
            windDirec: 'N/A',
            humidity: 'N/A',

        }
    },

    mounted() {
        this.updateDateTime();
        setInterval(this.updateDateTime, 1000);
        // this.startVideo();
        this.fetchData(); // Fetch initial data
        setInterval(this.fetchData, 1000); // Fetch periodically

    },

    methods: {
        //time
        updateDateTime() {
            const now = new Date();
            this.currentDate = now.toLocaleDateString();
            this.currentTime = now.toLocaleTimeString();
            console.log('Updated date and time:', this.currentDate, this.currentTime);
        },
        async fetchData() {
            try {
                const response = await axios.get('http://localhost:5000/weather_data');
                this.valueTemp = response.data.valueTemp;
                this.windSpeed = response.data.windSpeed;
                this.windDirec = response.data.windDirec;
                this.humidity = response.data.humidity;
            } catch (error) {
                console.error('Error fetching data from sensor', error);
            }
        }
    }
};

</script>

<style>
.overview {

    display: flex;
    flex-direction: column;
    margin-left: 220px;

    .top_content {
        height: 80px;
        width: 1486px;
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

        .vidoStream {
            width: 1120px;
            height: 780px;
            background-color: var(--light);
        }

        .weatherBar {
            margin-left: 20px;


            .card {
                display: flex;
                background-color: var(--light);
                width: 300px;
                height: 100px;
                border-radius: 12px;
                padding: 20px;
                align-items: center;
                margin-bottom: 20px;
            }

            .card-image {
                width: 60px;
                height: 60px;
            }

            .card-content {
                flex: 1;
                text-align: right;
            }

            .card-title {
                margin: 0 0 5px;
                font-size: 20px;
            }

            .card-value {
                margin: 0;
                font-size: 32px;
            }
        }
    }

}
</style>