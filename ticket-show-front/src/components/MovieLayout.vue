<template>
  <div class="container-fluid py-3">
    <template v-for="(data, index) in state.movies" :key="index">
      <MovieCard :data="data" />
    </template>
  </div>
</template>

<script setup>
import { onMounted, reactive } from "vue";
import axios from "axios";
import MovieCard from "./MovieCard.vue";

const BASE_URL = "http://127.0.0.1:8080/api";
const MOVIESAPI = BASE_URL + "/movies";


let state = reactive({
  movies: [],
});

async function getMovies() {
  try {
    state.movies = await axios.get(MOVIESAPI).then((d) => d.data);
    state.movies = JSON.parse(JSON.stringify(state.movies));
  } catch (err) {
    console.error("Error in fetching data:" + err);
  }
}

onMounted(() => {
  getMovies();
});
</script>

<style scoped>
.container-fluid {
  display: grid;
  justify-content: space-around;
  justify-items: center;
  column-gap: 30px;
  row-gap: 15px;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  grid-auto-rows: 350px;
}

.container-fluid > * {
  display: flex;
  justify-content: center;
  border: 1px solid black;
}
</style>