import { createRouter, createWebHistory } from "vue-router";

import { useAuthStore } from "../stores/auth";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", name: "login", component: () => import("../views/Login.vue") },
  { path: "/register", name: "register", component: () => import("../views/Register.vue") },
  {
    path: "/dashboard",
    name: "student-dashboard",
    component: () => import("../views/StudentDashboard.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/lesson/:id",
    name: "lesson",
    component: () => import("../views/LessonView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/teacher",
    name: "teacher-dashboard",
    component: () => import("../views/TeacherDashboard.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/analytics",
    name: "analytics",
    component: () => import("../views/Analytics.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/courses/editor",
    name: "course-editor",
    component: () => import("../views/CourseEditor.vue"),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: "login" };
  }
  return true;
});

export default router;
