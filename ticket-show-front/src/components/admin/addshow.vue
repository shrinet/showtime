<template>
  <section className="my-4 py-2">
    <div className="container mt-7">
      <h1 className="mb-4 text-center">Add Movie</h1>
      <div className="bg-white shadow rounded-lg d-block d-sm-flex">
        <div className="tab-content p-4 p-md-5" id="v-pills-tabContent">
          <div
            className="tab-pane  active"
            id="account"
            role="tabpanel"
            aria-labelledby="account-tab"
          >
            <h3 className="mb-4">Movie Details</h3>
            <div className="row">
              <div className="col-md-6 mt-2">
                <div className="form-group">
                  <label> Enter Movie Name</label>
                  <input
                    required
                    minlength="5"
                    type="text"
                    className="form-control"
                    name="name"
                    v-model="state.movie.name"
                  />
                </div>
              </div>

              <div className="col-md-6 mt-2">
                <div className="form-group">
                  <label>Enter Movie Description</label>
                  <input
                    required
                    type="desc"
                    className="form-control"
                    v-model="state.movie.description"
                  />
                </div>
              </div>
              <div className="col-md-6 mt-2">
                <div className="form-group">
                  <label>Enter Movie Venue</label>
                  <select class="form-select" id="mySelect" v-model="state.movie.venue">
                    <option value="Miraj cinma">Miraj cinma</option>
                    <option value="AMB cinema">AMB cinema</option>
                    <option value="fast moj cinema">fast moj cinema</option>
                  </select>
                </div>
              </div>
              <div className="col-md-6 mt-2">
                <div className="form-group">
                  <label for="formFileSm" class="form-label"
                    >Upload Movie Image</label
                  >
                  <input
                    required
                    @change="handleFileChange"
                    class="form-control form-control-sm"
                    id="formFileSm"
                    type="file"
                  />
                </div>
              </div>

              <div class="date">
                <div
                  class="row d-flex justify-content-between"
                  id="dateDisplay"
                ></div>
              </div>
            </div>
            <div>
              <button @click="upload" className="blue btn btn-primary mt-4">
                Upload Movie
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, reactive } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

const state = reactive({
  movie: {
    name: "",
    description: "",
    venue: "",
    file: "",
    timings: [],
    id: Date.now(),
  },
});

const handleFileChange = (event) => {
  const selectedFile = event.target.files[0];
  if (selectedFile) {
    const blobImage = new Blob([selectedFile], { type: selectedFile.type });

    const blobImageURL = window.URL.createObjectURL(blobImage);

    state.movie.file = blobImageURL;
  }
};

let new_movie_db = JSON.parse(localStorage.getItem("new_movie_db") || "[]");

function upload() {
  if (route.params.id) {
    localStorage.setItem("new_movie_db", JSON.stringify(new_movie_db));
    router.push("/admin/dashboard");
    return;
  }

  new_movie_db.push(state.movie);
  localStorage.setItem("new_movie_db", JSON.stringify(new_movie_db));
  router.push("/admin/dashboard");
}

function formatDate(date) {
  const options = { weekday: "long", day: "numeric", month: "long" };
  return new Intl.DateTimeFormat("en-US", options).format(date);
}

function createColumn(date) {
  const column = document.createElement("div");
  column.classList.add("col-md-2");

  const formattedDate = formatDate(date);

  const buttons = document.createElement("div");
  buttons.classList.add("timings");

  const timeSlots = ["9-12 AM", "12-3 PM", "3-6 PM", "6-9 PM"];
  timeSlots.forEach((slot) => {
    const button = document.createElement("button");
    button.classList.add("btn", "btn-primary", "my-1");
    button.textContent = slot;
    button.addEventListener("click", (e) => {
      const button = e.target;
      const timingId =
        slot + " : " + button.parentElement.previousElementSibling.textContent;
      if (button.classList.contains("btn-primary")) {
        // Remove 'btn-primary' and add 'btn-success'
        button.classList.remove("btn-primary");
        button.classList.add("btn-success");
        state.movie.timings.push(timingId);
      } else {
        // Remove 'btn-success' and add 'btn-primary'
        state.movie.timings = state.movie.timings.filter(
          (currentdata) => currentdata !== timingId
        );
        button.classList.remove("btn-success");
        button.classList.add("btn-primary");
      }
    });
    buttons.appendChild(button);
  });

  // Add date and buttons to the column
  column.innerHTML = `<p>${formattedDate}</p>`;
  column.appendChild(buttons);

  return column;
}

const currentDate = new Date();

onMounted(() => {
  const dateContainer = document.getElementById("dateDisplay");
  const answer = new_movie_db.find((data) => data.id == route.params.id);

  for (let i = 0; i < 5; i++) {
    const column = createColumn(currentDate);
    dateContainer.appendChild(column);
    currentDate.setDate(currentDate.getDate() + 1);
  }

  if (answer) {
    const buttons = document.getElementsByTagName("button");
    state.movie = answer;
    Array.from(buttons).forEach((current_btn) => {
      const slot = current_btn.textContent;
      const timingId =
        slot +
        ":" +
        current_btn.parentElement.previousElementSibling.textContent;

      state.movie.timings.forEach((timing) => {
        if (timing == timingId) {
          current_btn.classList.remove("btn-primary");
          current_btn.classList.add("btn-success");
        }
      });
    });
  }
});
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

/* input:invalid {
  border: 2px solid red;
  box-shadow: none;
  outline: none;
} */

@media screen and (max-width: 500px) {
  .error {
    font-size: 11.5px;
  }
}
</style>