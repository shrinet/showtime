<template>
  <div class="cont">
    <h1 class="title text-center py-3 bg-warning">
      {{ userdata.order.movie }}
    </h1>
    <div class="mt-4 p-3 seats">
      <template v-for="(element, index) in Array(260).fill('f')" :key="index">
        
        <i class="fa-solid fa-chair seat" @click="setSeats(index)" :id="index">
        </i>
      </template>
    </div>

    <p class="text-center text-3xl" v-if="state.book.error">
      {{ state.book.error }}
    </p>
    <div class="text-center">
      <div @click="book" class="btn btn-success price m-4">
        <span>Pay</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, watch } from "vue";
import {  useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

const userdata = ref(JSON.parse(localStorage.getItem("user")));
const BASE_URL = "http://127.0.0.1:8080/api";
const SEATAPI = BASE_URL + "/hall/"+ userdata.value.order.id + "/"+userdata.value.order.time ;

if (!userdata.value) router.push("/login");


const state = reactive({
  book: {
    cinema: "",
    cseat: [],
    booked: [],
    seats:
      JSON.parse(
        localStorage.getItem(
          "seatdb" +
            userdata.value.order.movie.slice(0, 5) +
            userdata.value.order.time.slice(0, 2) +
            userdata.value.order.hall.slice(0, 5)
        )
      ) || [],
    error: "",
  },
});

function setSeats(id) {
  if (
    JSON.parse(
      localStorage.getItem(
        "seatdb" +
          userdata.value.order.movie.slice(0, 5) +
          userdata.value.order.time.slice(0, 2) +
          userdata.value.order.hall.slice(0, 5)
      )
    )
  ) {
    if (
      JSON.parse(
        localStorage.getItem(
          "seatdb" +
            userdata.value.order.movie.slice(0, 5) +
            userdata.value.order.time.slice(0, 2) +
            userdata.value.order.hall.slice(0, 5)
        )
      ).includes(id)
    )
      return;
  }
  event.target.classList.toggle("choose");
  if (state.book.cseat.includes(id))
    return state.book.cseat.splice(state.book.cseat.indexOf(id), 1);

  state.book.cseat.push(id);
}

function book() {
  if (!state.book.cseat.length) {
    state.book.error = "Please Choose Seats for Booking";
    return false;
  }
  console.log(state.book.cseat)
  userdata.value.order.seat = state.book.cseat;
  localStorage.setItem("user", JSON.stringify(userdata.value));
  return router.push('/payment')
}

async function getSeats() {
  try {
    let sts = await axios.get(SEATAPI).then((d) => d.data);
    sts.booked.map(function(value) {
      state.book.booked.push(value);
   });
  } catch (err) {
    console.error("Error in fetching data:" + err);
  }
}

onMounted(() => {
  getSeats();
  
});

watch(() => state.book.booked.length, () => {
  const temp = document.getElementsByClassName("seat");
  state.book.booked.forEach((item) => {
      temp[item].style.opacity = "0.3";
      temp[item].className += " disabled";
    })
  })
</script>


<style scoped>
.movie {
  display: flex;
  flex-wrap: wrap;
  list-style: none;
  padding: 10px;
  gap: 15px;
}

button {
  all: unset;
  padding: 7px 20px;
  border: 1px solid rgb(0, 0, 0);
  border-radius: 900px;
  cursor: pointer;
  font-weight: 900;
}

.green {
  background: rgb(32, 219, 32);
  color: white;
}

.seats {
  border: 1px solid rgb(0, 0, 0);
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin: 15px;
  border-radius: 15px;
}

.seat.disabled {
  pointer-events: none;
}

.fa-solid {
  font-size: 30px;
  cursor: pointer;
}
.choose {
  color: rgb(111, 182, 4);
}

.price {
  display: inline-flex;
  gap: 8px;
  align-items: center;
}
.price {
  font-size: 25px;
  width: 90%;
  margin: auto;
  justify-content: center;
}
.text-3xl {
  font-size: 25px;
}
</style>