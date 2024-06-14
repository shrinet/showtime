<template>
  <div class="container-fluid">
    <div class="form">
      <h1 class="mb-5 text-center">Login Account</h1>
      <p v-if="error">{{ error }}</p>
      <form class="md:w-10/12 md:p-4 w-full mx-auto" @submit.prevent="login">
      <div class="mb-3">
        <label for="exampleInputEmail1" class="form-label">Username</label>
        <input
          type="text"
          class="form-control"
          v-model="form.username"
          id="exampleInputEmail1"
          aria-describedby="emailHelp"
        />
      </div>
      <div class="mb-3">
        <label for="exampleInputPassword1" class="form-label">Password</label>
        <input
          type="password"
          class="form-control"
          v-model="form.password"
          id="exampleInputPassword1"
        />
      </div>

      <button type="submit" class="btn btn-primary px-4 mx-auto">
        Login
      </button>
    </form>
      <br />
      <router-link to="/signup">Don't have Account Create now</router-link>
    </div>
  </div>
</template>

<script >
//import axios from "axios";

export default {
  name: "Login",
  data() {
    return {
      form: this.initForm()
    }
  },

  methods: {
    login() {
     
  fetch('http://127.0.0.1:8080/api/login', {
        method: "POST", // or 'PUT'
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.form),
      }).then(response => {
        response.json().then((data) => {
          console.log(data)
          localStorage.setItem('token', data.token)
          let udata = JSON.stringify({
            token: data.token,
            user: data.username
          })
          localStorage.setItem('user', udata)
          this.$router.push('/')
          });
        
        
        
      }).catch(error => {
        console.log(error)
      }) 
    },

    initForm() {
      return {
        username: null,
        password: null
      }
    }
  }
}


</script>

<style scoped>
.container-fluid {
  display: flex;
  min-height: 100vh;
  align-items: center;
  background-color: rgb(143, 0, 209);
}

.form {
  width: 30%;
  display: block;
  margin: auto;
  color: white;
  font-weight: 900;
  font-size: 20px;
}
</style>


