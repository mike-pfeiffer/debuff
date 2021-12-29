import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Impairments from "@/views/Impairments.vue";
import Home from "@/views/Home.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/impairments",
    name: "Impairments",
    component: Impairments,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
