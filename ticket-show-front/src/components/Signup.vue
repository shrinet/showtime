<template>
  <div class="container-fluid">
    <div class="form">
      <h1 class="mb-5 text-center">Create Account</h1>
      <p v-if="error">{{ error }}</p>
      <form class="md:w-10/12 md:p-4 w-full mx-auto" @submit.prevent="register">
        
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input
            minlength="5"
            required
            v-model="form.username"
            type="name"
            class="form-control"
          />
        </div>
        <div class="mb-3">
          <label for="exampleInputEmail1" class="form-label">Email address</label>
          <input
            v-model="form.email"
            type="email"
            class="form-control"
            id="exampleInputEmail1"
            aria-describedby="emailHelp"
          />
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input
            minlength="8"
            required
            v-model="form.password"
            type="password"
            class="form-control"
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Confirm Password</label>
          <input
            minlength="8"
            v-model="form.cpwd"
            type="password"
            class="form-control"
          />
        </div>
        <button
          type="submit"
          
          class="btn btn-primary px-4 mx-auto"
        >
          Signup
        </button>
      </form>
      <br />
      <router-link to="/login">Already Have account ? </router-link>
    </div>
  </div>
</template>

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
<script>
//import { reactive } from "vue";
//import { useRouter } from "vue-router";
//const router = useRouter();

export default {
  name: "register",
  data() {
    return {
      form: this.initForm()
    }
  },
  methods: {
    register(){
      //
      /* if (this.form.pwd != this.form.cpwd)
        return (this.form.error = "Password must be equal");

      this.form.error = ""; */

      fetch('http://127.0.0.1:8080/api/register', {
            method: "POST", // or 'PUT'
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(this.form),
          }).then(response => {
            localStorage.setItem('token', response.data.access_token)
            this.$store.dispatch('user', response.data)
            this.$router.push('/')
          }).catch(error => {
            console.log(error)
          }) 

      if (localStorage.getItem("registerdb")) {
        const olddb = JSON.parse(localStorage.getItem("registerdb"));

        

        localStorage.setItem(
          "registerdb",
          JSON.stringify([
            ...olddb,
            {
              email: this.form.email,
              password: this.form.cpwd,
              name: this.form.name,
            },
          ])
        );
      } else {
        localStorage.setItem(
          "registerdb",
          JSON.stringify([
            {
              email: this.form.email,
              password: this.form.cpwd,
              name: this.form.name,
            },
          ])
        );
      }
      this.form.error = "Registration Successful";
      this.$router.push("/login");
    },
    initForm() {
      return {
        email: null,
        password: null,
        username: null
      }
    }
  }
  
}


/* const state = reactive({
  form: {
    email: "",
    pwd: "",
    cpwd: "",
    error: "",
    name: "",
  },
});

function isAccountExist(olddb) {
  return olddb.findIndex((d) => d.email == state.form.email) != -1;
} */


</script>