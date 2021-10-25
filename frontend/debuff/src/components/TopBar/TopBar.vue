<template>
  <v-app-bar
      app
      color="#202327"
      dark
      clipped-left
  >
    <v-img
        class="mx-2"
        :src="require('@/assets/debuff icon(white).png')"
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