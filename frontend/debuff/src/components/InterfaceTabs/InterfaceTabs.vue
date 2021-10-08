<template>
  <div>
    <v-tabs
        v-model="tab"
        background-color="deep-purple accent-4"
        centered
        dark
        icons-and-text
    >
      <v-tabs-slider></v-tabs-slider>

      <v-tab
          v-for="(item,i) in interfaces"
          :key="i"
          :href=item.name>
        {{ item.name }}
        <v-icon :color=item.color>fas fa-ethernet</v-icon>
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item
          v-for="(item, i) in interfaces"
          :key="i"
          :value=item.name
      >
        <v-card flat>
          <v-card-text>Rock!!!</v-card-text>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "InterfaceTabs",
  data () {
    return {
      tab: null,
      interfaces: [{}]
    }
  },

  created() {
    axios.get('http://localhost:8002/api/interfaces/names')
        .then(res => {
          const interfaces = []
          for (const x of res.data) {
            const interface_data = {
              'name':"",
              'color':""
            }
            axios.get('http://localhost:8002/api/interfaces/details?interface=' + x)
                .then(res => {
                  interface_data.name = x
                  switch(res.data[x]['operstate']) {
                    case "UP": {
                      interface_data.color = 'green';
                      break;
                    }
                    case "DOWN": {
                      interface_data.color = 'red';
                      break;
                    }
                    default: {
                      interface_data.color = 'gray';
                      break;
                    }
                  }
                  interfaces.push(interface_data)
                })
            this.interfaces = interfaces
            console.log(interfaces)

          }
        })
        .catch(error => console.log(error))
  }
}
</script>


<style scoped>

</style>