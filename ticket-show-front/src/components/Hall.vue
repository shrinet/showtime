<template>
  <div class="container-fluid">
    <div class="row m-3 p-3">
      <h1 class="title text-center py-3 bg-warning">
        {{ userdata.order.movie }}
      </h1>
      
        <template v-for="(data, index) in state.movie.s" :key="index">
          <div class="col-12 box">
          <div class="first mx-2">{{ index }}</div>
          <div class="second">
            
            <template v-for="(time, ti) in data" :key="ti">
              <RouterLink
                to="/book"
                @click="selectDate(time)"
                class="btn btn-outline-primary"
              >
                {{ time }}
              </RouterLink>
            </template>
          
          </div></div>
        </template>
        
      
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive } from "vue";
import axios from "axios";

let userdata = ref(JSON.parse(localStorage.getItem("user")));
console.log(userdata.value.order)
const BASE_URL = "http://127.0.0.1:8080/api";
const MOVIEAPI = BASE_URL + "/movie/"+ userdata.value.order.id ;

let state = reactive({
  movie: [],
});

function selectDate(time) {
  userdata.value.order.time = time;
  userdata.value.order.hall =
    event.target.parentNode.previousElementSibling.innerText;
  localStorage.setItem("user", JSON.stringify(userdata.value));
}
async function getMovie() {
  try {
    state.movie = await axios.get(MOVIEAPI).then((d) => d.data);
    console.log(state.movie)
    //state.movie = JSON.parse(JSON.stringify(state.movies));
  } catch (err) {
    console.error("Error in fetching data:" + err);
  }
}

onMounted(() => {
  getMovie();
});
</script>
<style scoped>
.row {
  box-shadow: rgba(50, 50, 93, 0.25) 0px 50px 100px -20px,
    rgba(0, 0, 0, 0.3) 0px 30px 60px -30px,
    rgba(10, 37, 64, 0.35) 0px -2px 6px 0px inset;
  border-radius: 10px;
  gap: 20px;
}
.box {
  display: flex;
  padding: 10px;
  box-shadow: rgba(0, 0, 0, 0.05) 0px 6px 24px 0px,
    rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
  gap: 40px;
  border-radius: 5px;
  align-items: center;
}

.box .first {
  width: 300px;
}

.box .second {
  width: 100%;
  display: flex;
  gap: 35px;
}
</style>