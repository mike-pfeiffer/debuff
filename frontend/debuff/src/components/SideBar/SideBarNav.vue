<template>
  <div class="sidebar">
    <v-navigation-drawer
        app
        clipped
        permanent
        expand-on-hover
        absolute
        color="#202327"
    >
      <v-list
          nav
          dense
      >
        <v-list-item link to="/home">
          <v-list-item-icon>
            <v-icon style="color: white">fas fa-home</v-icon>
          </v-list-item-icon>
          <v-list-item-title style="color: white" >Home</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/settings">
          <v-list-item-icon>
            <v-icon style="color: white">fas fa-cog</v-icon>
          </v-list-item-icon>
          <v-list-item-title style="color: white">Settings</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/networking">
          <v-list-item-icon>
            <v-icon style="color: white">fas fa-network-wired</v-icon>
          </v-list-item-icon>
          <v-list-item-title style="color: white">Networking</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<style scoped>
.sidebar {
  color: white;
  float: left;
  /*position: fixed;*/
  z-index: 1;
  /*top: 64px;*/
  left: 0;
  bottom: 0;
}

</style>