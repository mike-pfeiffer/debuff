<template>
  <v-app>
    <TopBar />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import TopBar from "@/components/TopBar/TopBar.vue";

export default Vue.extend({
  name: "App",
  components: {TopBar},
  data: () => ({
    //
  }),
});
</script>
