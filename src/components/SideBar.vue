<template>
    <aside>
    <div class="logo">
        <img :src="logo">
        <h2>AIRFIRE</h2>
    </div>

    <div class="menu">
	    <router-link to="/" class="button">
            <img :src="droneIcon" class="icons" />
			<p class="text">Overview</p>
		</router-link>
		<router-link to="/fire-Analysis" class="button">
			<img :src="fireIcon" class="icons"/>
			<p class="text">Fire Ananlysis</p>
		</router-link>
	</div>
</aside>

</template>

<script setup>
import { ref } from 'vue'
import logo from '../assets/AirfireLogo.png'
import droneIcon from '../assets/Icon/Drone.svg'
import fireIcon from '../assets/Icon/Fire.svg'


</script>

<style>
aside {
	position: absolute;
	display: flex;
	flex-direction: column;
    background-image: url("../assets/bg_nav.png");
	color: var(--light);
	width: 220px;
	min-height: 100vh;


    .logo {
        padding: 20px;
        display: flex;
        align-items: center;
        gap: 1rem;
		margin-top: 0.15rem;

		img {
			width: 2rem;
		}
	}


	.menu {
		margin: 10px;
    
		.button {
			display: flex;
			align-items: center;
			text-decoration: none;
            margin-bottom: 10px;
			transition: 0.2s ease-in-out;
			padding: 0.5rem 1rem 0.5rem 0.5rem;

			.icons {
				font-size: 1rem;
				transition: 0.2s ease-in-out;
			}
			.text {
                margin-left: 10px;
				color: var(--light);
				transition: 0.2s ease-in-out;
			}

			&:hover {
				background-color: var(--dark-alt);
                border-radius: 10px;

			}

			&.router-link-exact-active {
				background-color: var(--dark-alt);
				border-radius: 10px;
            
			}
		}
	}

    @media (max-width: 1024px) {
		z-index: 99;
	}

    
}

</style>