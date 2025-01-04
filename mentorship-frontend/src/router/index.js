import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AskQuestion from "../components/AskQuestion.vue";
import RecommendResources from "../components/RecommendResources.vue";
import TestComp from "../components/TestComp.vue";
import ReviewComp from "../components/ReviewComp.vue";

const routes = [
  { path: "/", name: "HomeView", component: HomeView },
  { path: "/ask", name: "AskQuestion", component: AskQuestion },
  {
    path: "/recommend-resources",
    name: "RecommendResources",
    component: RecommendResources,
  },
  { path: "/test", name: "TestComp", component: TestComp },
  { path: "/review", name: "ReviewComp", component: ReviewComp },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;      