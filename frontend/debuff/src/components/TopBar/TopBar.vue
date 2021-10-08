<template>
  <v-app-bar
      app
      color="#CDCDCD"
      dark
  >
    <v-img
        class="mx-2"
        :src="require('@/assets/debuff icon.png')"
        max-height="200"
        max-width="175"
        contain
    ></v-img>
  </v-app-bar>
</template>

<script>
export default {
  name: "TopBar"
}
</script>

<style scoped>

</style>