<template>
  <div class="sidebar">
    <v-navigation-drawer
        app
        clipped
        :mini-variant.sync="mini"
        permanent
        expand-on-hover
        absolute
        color="#202327"
    >
      <v-list
          nav
          dense
      >
        <v-list-item link to="/">
          <v-list-item-icon>
            <v-icon style="color: white">fas fa-arrow-alt-circle-down</v-icon>
          </v-list-item-icon>
          <v-list-item-title style="color: white">Impairments</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
export default {
  name: "SideNav",
  data() {
    return {
      mini: true
    }
  }
};
</script>

<style scoped>
.sidebar {
  color: white;
  float: left;
  /*position: static;*/
  z-index: 1;
  left: 0;
  bottom: 0;
}

</style>
