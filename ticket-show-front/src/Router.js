import { createRouter, createWebHistory } from "vue-router";
import Home from "./components/Home.vue"
import Login from "./components/Login.vue"
import Signup from "./components/Signup.vue"
import Profile from "./components/Profile.vue"
import book from "./components/book.vue"
import Hall from "./components/Hall.vue"
import MovieLayout from "./components/MovieLayout.vue"
import Payment from "./components/Payment.vue"
import Bookinghistory from "./components/Bookinghistory.vue"
import { Authentication } from "./guards";

import AdminLogin from "./components/admin/admin_login.vue"
import Dashboard from './components/admin/Dashboard.vue'
import Adminhome from "./components/admin/home.vue"
import AddShow from "./components/admin/addshow.vue"

const routes = [
    {
        path: '/',
        component: Home,
        beforeEnter: (to, from, next) => Authentication(next),
        children: [
            {
                path: "",
                component: MovieLayout
            },
            {
                path: 'hall',
                component: Hall
            },
            {
                path: 'book',
                component: book,
            },
            {
                path: 'payment',
                component: Payment,
            },
            {
                path: 'history',
                component: Bookinghistory,
            }
        ]
    },
    {
        path: "/login",
        component: Login
    },
    {
        path: "/signup",
        component: Signup
    },
    {
        path: '/profile',
        component: Profile
    },

    {
        path: '/admin',
        component : Adminhome,
        children:[
            {
                path :"login",
                component: AdminLogin
            },
            {
                path:'dashboard',
                component: Dashboard,
            },
            {
                path : 'addshow',
                component: AddShow
            },
            {
                path : 'edit/:id',
                component: AddShow
            }
       
            ,{
                path: '',
                redirect: 'admin/login'
            } , 
          
        ]
    },

]

const Router = createRouter({
    history: createWebHistory(),
    routes,
})

export default Router