<template>
  <v-app style="background-color: #f0f0f0">
    <TopBar />
    <SideBarNav />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import TopBar from "@/components/TopBar/TopBar.vue";
import SideBarNav from "@/components/SideBar/SideBarNav.vue";

export default Vue.extend({
  name: "App",
  components: {TopBar, SideBarNav},
  data: () => ({
    //
  }),
});
</script>
