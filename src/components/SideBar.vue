<template>
	<aside :class="`${is_expanded ? 'is-expanded' : ''}`">
		<div class="logo">
			<img :src="logo" />
            <h2>AIRFIRE</h2>
            
		</div>

		<div class="menu-toggle-wrap">
			<button class="menu-toggle" @click="ToggleMenu">
				<img :src="arrow_right" class="icons" />
			</button>
		</div>
		<div class="menu">
			<router-link to="/" class="button">
                <img :src="droneIcon" class="icons" />
				<span class="text">Overview</span>
			</router-link>
			<router-link to="/fire-Analysis" class="button">
				<img :src="fireIcon" class="icons"/>
				<span class="text">Fire Ananlysis</span>
			</router-link>
		</div>

		<div class="flex"></div>
		
	</aside>
</template>

<script setup>
import { ref } from 'vue'
import logo from '../assets/AirfireLogo.png'
import droneIcon from '../assets/Icon/Drone.svg'
import fireIcon from '../assets/Icon/Fire.svg'
import arrow_right from '../assets/Icon/arrow-right.svg'


const is_expanded = ref(localStorage.getItem("is_expanded") === "true")

const ToggleMenu = () => {
	is_expanded.value = !is_expanded.value
	localStorage.setItem("is_expanded", is_expanded.value)
}

</script>

<style>
aside {
	position: absolute;
	display: flex;
	flex-direction: column;

    background-image: url("../assets/bg_nav.png");

	color: var(--light);

	width: 64px;
	overflow: hidden;
	min-height: 100vh;
	padding: 1rem;

	transition: 0.2s ease-in-out;

	.flex {
		flex: 1 1 0%;
	}

	.logo {
        display: flex;
        align-items: center;
        gap: 1rem;
		margin-top: 0.15rem;

		img {
			width: 2rem;
		}
	}

	.menu-toggle-wrap {
		display: flex;
		justify-content: flex-end;
        margin-top: 0.5rem;

		position: relative;
		top: 0;
		transition: 0.2s ease-in-out;

		.menu-toggle {
			transition: 0.2s ease-in-out;
			.icons {
				font-size: 2rem;
				fill: var(--light);
				transition: 0.2s ease-out;
			}
			
			&:hover {
				.icons {
					transform: translateX(0.5rem);
				}
			}
		}
	}

	h3, .button .text {
		opacity: 0;
		transition: opacity 0.3s ease-in-out;
	}

	h3 {
		color: var(--grey);
		font-size: 0.875rem;
		margin-bottom: 0.5rem;
		text-transform: uppercase;
	}

	.menu {
		margin: 0 -1rem;

		.button {
			display: flex;
			align-items: center;
			text-decoration: none;
            margin: 8px;
			transition: 0.2s ease-in-out;
			padding: 0.5rem 1rem 0.5rem 0.5rem;

			.icons {
				font-size: 1rem;
				transition: 0.2s ease-in-out;
			}
			.text {
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

	&.is-expanded {
		position: absolute;
		width: 220px;

		.menu-toggle-wrap {
			top: -3rem;
			
			.menu-toggle {
				transform: rotate(-180deg);
			}
		}

		h3, .button .text {
			opacity: 1;
		}

		.button {
			.icons {
				margin-right: 1rem;
			}
		}

	}

	@media (max-width: 1024px) {
		z-index: 99;
	}
}
</style>
