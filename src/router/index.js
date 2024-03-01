import { createRouter, createWebHistory } from "vue-router";
import Overview from "../views/Overview.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: Overview,
    },
    {
      path: "/fire-Analysis",
      component: () => import("../views/FireAnalysis.vue"),
    },
  ],
});

export default router;
