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
                <!-- <video src="../assets/Videostream/HorrusStream.mp4" style="width: 840px; height: 560px;" controls autoplay></video> -->
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
export default {
    data() {
        return {
            currentDate: '',
            currentTime: '',
            valueTemp: '31',
            windSpeed: '2',
            windDirec: 'n',
            humidity: '23',

        }
    },

    async mounted() {
        this.updateDateTime();
        setInterval(this.updateDateTime, 1000);
        this.startVideo();

        // Make a GET request to your server's endpoint
        try {
            const response = await axios.get('http://localhost:5000/portable_weather_station_read');
            this.weatherData = response.data; // Ensure this is correct
            console.log('Weather data:', this.weatherData);
        } catch (error) {
            console.error(error);
        }
    },

    methods: {
        //time
        updateDateTime() {
            const now = new Date();
            this.currentDate = now.toLocaleDateString();
            this.currentTime = now.toLocaleTimeString();
            console.log('Updated date and time:', this.currentDate, this.currentTime);
        }
    }
}

</script>

<style>
.overview {

    display: flex;
    flex-direction: column;
    margin-left: 64px;
    /* width: 1257px;
    height: 720px; */

    .top_content {
        height: 80px;
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
                gap: 5px;
                align-items: center;
            }

        }
    }

    .main_content {
        display: flex;
        flex-direction: row;
        margin: 20px;

        .vidoStream {
            width: 1240px;
            height: 780px;
            background-color: var(--light);
        }

        .weatherBar {
            margin-left: 20px;


            .card {
                display: flex;
                background-color: var(--light);
                width: 340px;
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