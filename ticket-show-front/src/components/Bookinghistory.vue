<template>
  <div class="container-fluid p-3">
    <template v-if="orders">
      <div v-for="(data, index) in orders" :key="index" class="card mb-3">
        <div class="card-body">
          <h5 class="card-title">{{ data.movie }}</h5>
          <div class="card-text">
            <p>Cinema Hall : {{ data.hall }}</p>
            <p>Start timing : {{ data.time }}</p>
            <p>
              Total Amount Paid:
              {{ data.seat.length * 200 + (data.seat.length * 200 * 11) / 100 }}
              ( {{ data.seat.length }} Tickets)
            </p>
          </div>
          <div v-if="data.comment">
            Your Review:
            {{ data.comment }}
            <template
              v-for="(element, index) in Array(5).fill('f')"
              :key="index"
            >
              <i
                class="fa-solid fa-star star"
                :class="[data.star >= index + 1 ? 'color' : '']"
                @click="fill(index + 1)"
                :id="index"
              >
              </i>
            </template>
          </div>
          <div v-else>
            <button
              data-bs-toggle="modal"
              :data-bs-target="'#' + data.id"
              class="btn btn-primary"
            >
              Want To Give Review
            </button>
          </div>

          <Modal
            @update_review="update_review"
            :id="data.id"
            :name="data.movie"
          />
        </div>
      </div>
    </template>
    <template v-else>
      <div>No Booking History</div>
    </template>
  </div>
</template>
<script setup>
import { reactive, ref } from "vue";
import Modal from "./Modal.vue";

const userdata = ref(JSON.parse(sessionStorage.getItem("user")));

const orders = reactive(
  JSON.parse(localStorage.getItem(userdata.value.email))?.[0].orders  
);

function update_review(comment, id, star) {
  const index = orders.findIndex((d) => d.id == id);
  orders[index].star = star;
  orders[index].comment = comment;
  localStorage.setItem(
    userdata.value.email,
    JSON.stringify([
      {
        email: userdata.value.email,
        orders: orders,
      },
    ])
  );
}
</script>


<style scoped>
.color {
  color: blue !important;
}
</style>
