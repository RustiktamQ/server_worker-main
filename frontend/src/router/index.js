import { createRouter, createWebHistory } from "vue-router";
import ImportPage from "@/components/ImportPage.vue";
import ExportPage from "@/components/ExportPage.vue";
import ProcessPage from "@/components/ProcessPage.vue";

const routes = [
    { path: '/', redirect: '/process'},
    { path: '/process', component: ProcessPage},
    { path: '/export', component: ExportPage},
    { path: '/import', component: ImportPage}
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;