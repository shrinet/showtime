<template>
  <div class="card">
    <img
      class="card-img-top"
      :src="'http://127.0.0.1:8080' + props.data.image"
      alt="image"
      style="object-fit: cover;height: 15rem;"
    />
    <div class="card-body">
      <h6 class="card-title">{{ props.data.name }}</h6>
      <p class="card-text">
        
      </p>
      <RouterLink
        @click="selectMovie(props.data.id, props.data.name, props.data.price)"
        to="/hall"
        class="btn btn-primary"
        ><i class="fa-solid fa-bag-shopping"></i> &nbsp;Book Now</RouterLink
      >
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from "vue";

const props = defineProps({
  data: Object,
});

function selectMovie(id, name, price) {
  let userdata = ref(JSON.parse(localStorage.getItem("user")));
  userdata.value.order = {
    id: id,
    movie: name,
    price: price
  } ;
  console.log(userdata)
  localStorage.setItem("user", JSON.stringify(userdata.value));
}

</script>

<style scoped>
.card-img-top {
  width: 100%;
  object-position: top;
  object-fit: cover;
  height: 100%;
}
</style>