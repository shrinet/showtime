<template>
  <section className="my-4 py-2">
    <div className="container mt-7">
      <h1 className="mb-4 text-center">My Account</h1>
      <div className="bg-white shadow rounded-lg d-block d-sm-flex">
        <div className="tab-content p-4 p-md-5" id="v-pills-tabContent">
          <div
            className="tab-pane  active"
            id="account"
            role="tabpanel"
            aria-labelledby="account-tab"
          >
            <h3 className="mb-4">Account Settings</h3>
            <div className="row">
              <div className="col-md-6 mt-2">
                <div className="form-group">
                  <label> Name</label>
                  <input
                    minlength="5"
                    type="text"
                    className="form-control"
                    name="name"
                    v-model="formname"
                  />
                </div>
              </div>

              <div className="col-md-6 mt-2">
                <div className="form-group">
                  <label>Email</label>
                  <input
                    disabled
                    type="email"
                    className="form-control"
                    name="email"
                    v-model="userdata.email"
                  />
                </div>
              </div>
            </div>
            <div>
              <button @click="update" className="blue btn btn-primary mt-4">
                Update
              </button>
              <!-- <span className="error">{{error}}</span> -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();
const userdata = ref(JSON.parse(sessionStorage.getItem("user")));
if (!userdata.value) router.push("/login");

const formname = ref(userdata.value.name);

function update() {
  const olddb = JSON.parse(localStorage.getItem("registerdb"));

  const index = olddb.findIndex((d) => d.email == userdata.value.email);

  olddb[index].name = formname.value;

  localStorage.setItem("registerdb", JSON.stringify(olddb));
  sessionStorage.setItem("user", [JSON.stringify(olddb[index])]);
}
</script>


<style scoped>
.error {
  display: inline-block;
  text-align: center;
  height: 20px;
  color: red;
  margin-left: 10px;
}

.name {
  width: 90%;
  margin: auto;
}

.shadow {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
}

.profile-tab-nav {
  min-width: 250px;
}

.tab-content {
  flex: 1;
}

.form-group {
  margin-bottom: 1.5rem;
}

.nav-pills a.nav-link {
  padding: 15px 20px;
  border-bottom: 1px solid #ddd;
  border-radius: 0;
  color: #333;
}

.nav-pills a.nav-link i {
  width: 20px;
}

.nav-pills a.nav-link.active-tab {
  color: white;
  background-color: blue;
}

h1 {
  font-size: 2.5rem;
  font-weight: bold;
}

input:invalid {
  border: 2px solid red;
  box-shadow: none;
  outline: none;
}

@media screen and (max-width: 500px) {
  .error {
    font-size: 11.5px;
  }
}
</style>