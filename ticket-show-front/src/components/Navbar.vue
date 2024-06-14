<template>
  <nav class="navbar navbar-expand-lg navbar-light p-2">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">ShowTime</a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li style="display: none">
            <form class="d-flex">
              <input
                class="form-control me-2"
                type="search"
                placeholder="Search"
                aria-label="Search"
              />
              <button class="btn btn-outline-success" type="submit">
                Search
              </button>
            </form>
          </li>
        </ul>
        <template v-if="userdata">
          <button class="btn btn-primary mx-2">
            <router-link class="nav-link" to="/profile">
              <i class="fa-solid fa-user"></i>&nbsp;{{
                userdata.name
              }}</router-link
            >
          </button>
          <button class="btn btn-primary mx-2">
            <router-link class="nav-link" to="/history">
              <i class="fa-solid fa-clock-rotate-left"></i>&nbsp; Booking
              History
            </router-link>
          </button>
          <button class="btn btn-primary mx-2">
            <router-link class="nav-link" to="/"> Home </router-link>
          </button>
          <button class="btn btn-primary" @click="logout">Logout</button>
        </template>
        <template v-else>
          <button class="btn btn-primary">
            <router-link class="nav-link" to="/login">Login</router-link>
          </button>
          <button class="btn btn-primary mx-3">
            <router-link class="nav-link" to="/signup">Signup</router-link>
          </button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

let router = useRouter()
/* const udata = JSON.stringify({
  token: localStorage.getItem("token"),
  user: localStorage.getItem("user")
})

let userdata = ref(JSON.parse(udata)); */
let userdata = ref(JSON.parse(localStorage.getItem("user")));

function logout() {
  userdata.value = null;
  localStorage.clear();
  router.push('/login')
}
</script>

<style scoped>
nav {
  background-color: aquamarine;
}

.navbar-brand {
  color: purple;
  font-weight: 900;
}
</style>