<template>
    <div class="fireAnalysis">
		<!-- Top content -->
		<div class="top_content">
            <h2>Fire Analysis</h2>
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
                <!--RGB detectiont -->
		        <div class="detecCard">
                    <h5>RGB Detection</h5>
				    <div class="result">
					    <!-- <img src="../assets/result/rgb_Detection.jpg" style="width: 340px; height: 220px;"> -->
					    <img style="-webkit-user-select: none;" src="http://localhost:5000/rgb_feed" width="340" height="220">
                        <div calss="paraDetec">
						    <div class="box-container">
              			        <div class="box" style="border: 2px solid red;"></div>
              			        <div class="text">Fire</div>
            		        </div>
					    </div>
                    </div>
                </div>

                <!--Thermal detectiont -->
		        <div class="detecCard">
                    <h5>RGB Detection</h5>
				    <div class="result">
					    <!-- <img src="../assets/result/thermal_Detection.jpg" style="width: 340px; height: 220px;"> -->
                        <img style="-webkit-user-select: none;" src="http://localhost:5000/thermal_feed" width="340" height="220">
					    <div calss="paraDetec">
						    <div class="box-container">
              			        <div class="box" style="border: 2px solid red;"></div>
              			        <div class="text">Fire</div>
            		        </div>
                            <div class="box-container">
              				    <div class="box" style="border: 2px solid rgb(13, 0, 255);"></div>
              				    <div class="text">Smoke</div>
            			    </div>
                        </div>
					</div>
                </div>
		    </div>

            <!--prediction -->
	        <div class="prediction">
                <div class="inputWildTime">
                    <div class="wildbutton">
                        <p>Type of Wild</p>
                        <select v-model="selectedWildOption" @change="handleChangeWild">
                            <option v-for="option in wildOptions" :key="option.value" :value="option.value">
                                {{ option.text }}
                            </option>
                        </select>
                    </div>
                    <div class="wildbutton">
                        <p>Time to Prediction</p>
                        <select v-model="selectedWildOption" @change="handleChangeWild">
                            <option v-for="option in wildOptions" :key="option.value" :value="option.value">
                                {{ option.text }}
                            </option>
                        </select>
                    </div>
                </div>
                
                <div class="predicFire">
			        <div class="title">
				        <h5>Fire Prediction</h5>
			        </div>
			        <div class="showResult">
				        <div class="compass">
				            <img src="../assets/Vector.png" style="width: 20px; height: 20px;">
				            <img src="../assets/compass.png" style="width: 80px; height: 80px;">
			            </div>
			            <div class="predicResult">
                            <img src="http://localhost:5000/fire_analysis_feed" style="width: 350px; height: 240px;">
                            <meta http-equiv="refresh" content="30">
			            </div>
			            <div class="fireDenger">
                            <div class="title">
				                <p>Fire Danger Lavel</p>
			                </div>
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

      }
    },

    mounted() {
       //--time---//
      this.updateDateTime();
      setInterval(this.updateDateTime, 1000);

      //--video---//
      this.startVideo();

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
.fireAnalysis {
  
    display: flex;
    flex-direction: column;
    margin-left: 64px;

    .top_content {
        height: 80px;
        padding: 20px 30px 20px 20px;
        display: flex;
        flex-direction: row;
        background-color: var(--light);
        align-items:center;
        justify-content:space-between;

        .date_time{
            display: flex;
            gap:30px;

            .date , .time{
              font-size: 20px;
              display: flex;
              gap: 5px;
              align-items: center;
            }

        }
    }

	.main_content {
        display: flex;
	    flex-direction: column;
        margin: 20px;

        .detection{
		display: flex;
		gap: 20px;

		    .detecCard{
			    background-color: var(--light);
			    width: 578px;
			    height: 280px;
			    padding: 20px;
			    border-radius: 12px;
                

                .result{
                    display: flex;
                    margin-top: 6px;
                    gap:10px;
                    justify-content: center;
                }


		    }
			
		}


        .prediction {
		    display: flex;
		    margin-top: 20px;
            gap: 20px;

		    .inputWildTime{
			    display:flex;
			    flex-direction: column;
			    background-color: var(--light);
			    width: 332px;
			    height: 300px;
			    border-radius: 12px;
			    padding: 20px;
			    font-size: 14px;

			    select {
                    margin: 10px 0px 26px 0px;
				    background-color: var(--grey);
				    width: 286px;
				    height: 40px;
				    border-radius: 12px;
			    }
            }

            .predicFire {
			    width: 820px;
			    height: 300px;
			    background-color: var(--light);
			    border-radius: 12px;
			    padding: 20px;

                .showResult {
				    display: flex;
				    margin-top: 5px;
                    
                    .compass{
					    display: flex;
					    flex-direction: column;
					    margin: 50px;
					    gap:5px;
					    align-items: center;
					    justify-content: center;
				    }


                    .fireDenger{
                        .title{
                            margin-bottom: 10px;
                        }
					    font-size: 14px;
                        margin-left: 50px;
                        
                    }
                }

            }
        }

	}

    .box-container {
        margin-bottom: 10px;
      	display: flex;
      	align-items: center;
    }
  
    .box {
        width: 20px;
        height: 20px;
    }
  
    .text {
        color: var(--dark);
      	font-size: 12px; 
      	margin-left: 4px; 
    }
		
}

</style>