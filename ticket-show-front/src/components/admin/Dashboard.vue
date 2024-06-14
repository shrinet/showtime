<template>
  <h1 class="my-2 mt-4 text-center">All Shows</h1>
  <div class="">
    <div class="col-md-4 mx-auto">
      <div class="cardadd">
        <p class="card-text">Add Movie or Show By Clicking here</p>

        <router-link to="/">
          <button class="btn btn-add mx-2">Check Your Listed Movies</button>
        </router-link>

        <router-link to="addshow">
          <button class="btn btn-add">Add Show</button>
        </router-link>
      </div>
    </div>
  </div>
  <div class="container mt-5">
    <div class="row">
      <h1 class="text-center" v-if="!new_movie_db.length">
        No Movie Uploaded Yet
      </h1>
      <div
        class="col-md-4 mb-4"
        v-for="(movie, index) in new_movie_db"
        :key="index"
      >
        <div class="card">
          <img :src="'http://127.0.0.1:8080' + movie.image" class="card-img" alt="Image 1" />
          <div class="card-body">
            <h5 class="card-title">{{ movie.name }}</h5>
            <p class="card-text">{{ movie.description }}</p>
            <button @click="editMovie(movie.id)" class="btn btn-primary">
              Edit
            </button>
            <button @click="deleteMovie(movie.id)" class="btn btn-danger mx-2">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const userdata = ref(JSON.parse(localStorage.getItem("user")));
let new_movie_db = ref(
  
  fetch('http://127.0.0.1:8080/api/admin/show', {
        method: "GET", // or 'PUT'
        headers: {
          'Authorization': 'Bearer ' + userdata.value.token, 
          "Content-Type": "application/json",
        },
        body: JSON.stringify(),
      }).then(response => {
        response.json().then((data) => {
          new_movie_db.value = data
          
          });
        
        
        
      }).catch(error => {
        console.error(error);
        router.push("/");

      }) 
);

function deleteMovie(id) {
  new_movie_db.value = new_movie_db.value.filter((movie) => movie.id !== id);
  localStorage.setItem("new_movie_db", JSON.stringify(new_movie_db.value));
}

function editMovie(id) {
  router.push("edit/" + id);
}

async function getDashboard() {
  
  //console.log(arrayFailed)
  fetch('http://127.0.0.1:8080/api/admin/dashboard', {
        method: "GET", // or 'PUT'
        headers: {
          'Authorization': 'Bearer ' + userdata.value.token, 
          "Content-Type": "application/json",
        },
        body: JSON.stringify(),
      }).then(response => {
        response.json().then((data) => {
          console.log(data)
          
          });
        
        
        
      }).catch(error => {
        console.error(error);
        router.push("/");

      }) 
}

onMounted(() => {
  getDashboard();
})
</script>


<style scoped>
.card-img {
  height: 200px; /* Adjust the height as needed */
  object-fit: cover; /* Maintain aspect ratio and cover the entire container */
}

.cardadd {
  background-color: #f5f5f5;
  border: none;
  border-radius: 10px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  padding: 20px;
  text-align: center;
}

/* Style the "Add" button */
.btn-add {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 18px;
  cursor: pointer;
}

/* Style the "Add" button on hover */
.btn-add:hover {
  background-color: #0056b3;
}
</style>