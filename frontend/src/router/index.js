/*
 * @Description: Copyright © 1999 - 2020 Winter. All Rights Reserved. 
 * @Author: Winter
 * @Email: 837950571@qq.com
 * @Date: 2021-03-29 16:39:31
 * @LastEditTime: 2021-04-26 19:35:55
 */
import VueRouter from "vue-router"
import Vue from "vue"

import Login from "../views/Login"
import Home from "../views/Home"
import Record from "../components/Record"
import New from "../components/New"
import Introduction from "../components/Introduction"
import User from "../components/User"
import Detail from "../views/Detail"
Vue.use(VueRouter)

const routes = [
    { path: "/", redirect: "/login" },
    {
        path: "/login",
        name: "Login",
        component: Login,
    }, {
        path: "/home",
        name: "Home",
        component: Home,
        redirect: "/home/record",
        children: [{
            name: "Record",
            path: "/home/record",
            component: Record
        },
        {
            name: "New",
            path: "/home/new",
            component: New
        },
        {
            name: "Introduction",
            path: "/home/introduction",
            component: Introduction
        },
        {
            name: "User",
            path: "/home/user",
            component: User
        }
        ]
    },
    {
        path: "/detail",
        name: "Detail",
        component: Detail
    }
]
const router = new VueRouter({
    routes
})

export default router