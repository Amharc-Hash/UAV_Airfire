<template>
	<div class="app">
		<SideBar />
		<router-view />
	</div>
</template>

<script setup>
import SideBar from './components/sidebar.vue';
</script>
<style>
:root {
	--primary: #FF8202;
	--primary-alt: #FF8202;
	--grey: #BFBFBF;
	--dark: #1E1E1E;
	--dark-alt: #0E0E0E;
	--light: #f1f5f9;
}

* {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
	font-family: 'Fira sans', sans-serif;
}

body {
	background-color: var(--grey);
}

button {
	cursor: pointer;
	appearance: none;
	border: none;
	outline: none;
	background: none;
}

.app {
	display: flex;

	main {
		flex: 1 1 0;
		padding: 2rem;

		@media (max-width: 1024px) {
			padding-left: 6rem;
		}
	}
}
</style>