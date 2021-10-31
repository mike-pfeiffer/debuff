import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Interfaces from "@/views/Interfaces.vue";
import Home from "@/views/Home.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/interfaces",
    name: "Interfaces",
    component: Interfaces,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
