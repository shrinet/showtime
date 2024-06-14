<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6 offset-md-3">
        <h2 class="text-center text-dark mt-5">Login</h2>
        <h1 class="text-center  mb-5 text-dark">Admin Panel</h1>
        <div class="card my-5">
          <form class="card-body cardbody-color p-lg-5" @submit.prevent="login">
            <div class="mb-3">
              <input
                type="email"
                class="form-control"
                id="email"
                aria-describedby="emailHelp"
                placeholder="email"
                v-model="state.form.email"
              />
            </div>
            <div class="mb-3">
              <input
                type="password"
                class="form-control"
                id="password"
                placeholder="password"
                v-model="state.form.pwd"
              />
            </div>
            <span class="text-danger">{{state.form.error}}</span>
            <div class="text-center">
              <button type="submit" class="btn btn-color px-5 w-100">
                Login
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.btn-color {
  background-color: #0e1c36;
  color: #fff;
}

.profile-image-pic {
  height: 200px;
  width: 200px;
  object-fit: cover;
}

.cardbody-color {
  background-color: #ebf2fa;
}

a {
  text-decoration: none;
}
</style>

<script setup>
import { reactive } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const state = reactive({
  form: {
    email: "",
    pwd: "",
    error: "",
  },
});

function login() {

  const olddb = JSON.parse(localStorage.getItem("registerdb")) || [];

  const index = olddb.findIndex(
    (d) => d.email == state.form.email && d.password == state.form.pwd
  );

  if (index == -1) return (state.form.error = "Invalid Credentails");
  console.log(state.form)
  sessionStorage.setItem("admin_panel", [JSON.stringify(olddb[index])]);
  router.push("dashboard");
}
</script>
