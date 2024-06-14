import { createApp } from 'vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
import App from './App.vue'
import Routes from './Router.js'
import axios from "axios";

axios.defaults.baseURL = 'http://localhost:8000/'
//axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('token')
//axios.defaults.withCredentials = true;

createApp(App).use(Routes).mount('#app')
