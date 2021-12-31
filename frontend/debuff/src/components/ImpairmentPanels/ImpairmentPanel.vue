<template>
  <div class="rows">
    <v-row justify="center">
      <v-expansion-panels popout>
        <v-expansion-panel
            v-for="(item,i) in interfaces"
            :key="i"
        >
          <v-expansion-panel-header>
            <div>
              <v-icon :color=item.color>fas fa-ethernet</v-icon>
              {{ item.name }}
            </div>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <InterfaceImpairmentForm :interface_name=item.name />
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-row>
  </div>
</template>

<script>
import axios from "axios";
import InterfaceImpairmentForm from "@/components/ImpairmentPanels/InterfaceImpairmentForm";

export default {
  name: "ImpairmentPanel",
  components: {InterfaceImpairmentForm},
  data () {
    return {
      interfaces: [{}]
    }
  },

  created() {
    console.log("Yay!")
    axios.get('http://192.168.5.2:8002/api/interfaces/names')
        .then(res => {
          const interfaces = []
          for (const x of res.data) {
            const interface_data = {
              'name':"",
              'color':""
            }
            axios.get('http://192.168.5.2:8002/api/interfaces/state?interface=' + x)
                .then(res => {
                  interface_data.name = x
                  switch(res.data) {
                    case "UP": {
                      interface_data.color = 'green';
                      break;
                    }
                    case "DOWN": {
                      interface_data.color = 'red';
                      break;
                    }
                    case "UNKNOWN": {
                      interface_data.color = 'grey';
                      break;
                    }
                    case "IMPAIRED": {
                      interface_data.color = 'yellow';
                      break;
                    }
                    default: {
                      interface_data.color = 'black';
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
.rows {
  padding: 2em;
}
/*.test {*/
/*  align-items: flex-start;*/
/*  justify-content: left;*/
/*  left: 1px;*/
/*  text-align: right;*/
/*}*/
</style>
