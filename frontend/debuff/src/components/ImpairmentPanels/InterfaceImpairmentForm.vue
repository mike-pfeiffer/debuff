<template>
  <v-container class="my-5">
    <v-layout row wrap>

      <v-card
        class="mx-auto"
        max-width="344"
        tile
        >
        <v-card-title class="text-h5">
          Status
        </v-card-title>
          <v-card-text>
            {{ impairmentStatus }}
          </v-card-text>
          <v-card-actions>
            <v-btn
                :disabled="!valid"
                color="success"
                class="mr-4"
                @click="sendGet()"
            >
              Submit
            </v-btn>
          </v-card-actions>
      </v-card>

      <v-card
        class="mx-auto"
        max-width="344"
        tile
        >
        <v-card-title class="text-h5">
          Impairments
        </v-card-title>
        <v-form
            ref="form"
            v-model="valid"
            lazy-validation
        >
          <v-card-text>

            <v-select
                v-model="select"
                :items="items"
                :rules="[v => !!v || 'Item is required']"
                label="Direction"
                required
            ></v-select>

            <v-text-field
                v-model="delay"
                label="Delay"
                hint="Range Value: > 0 ms"
                persistent-hint
            ></v-text-field>

            <v-text-field
                v-model="jitter"
                label="Jitter"
                hint="Range Value: > 0 ms"
                persistent-hint
            ></v-text-field>

            <v-text-field
                v-model="loss"
                label="Loss"
                hint="Range Value: 100 >= x > 0 %"
                persistent-hint
            ></v-text-field>
            <v-divider class="mt-4"></v-divider>
            <v-card-actions>
              <v-btn
                  :disabled="!valid"
                  color="success"
                  class="mr-4"
                  @click="sendPost()"
              >
                Submit
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                  color="error"
                  class="mr-4"
                  @click="reset"
              >
                Reset
              </v-btn>
            </v-card-actions>
          </v-card-text>
        </v-form>
      </v-card>
    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  props: {
    interface_name: {
      type: String
    }
  },
  data: () => ({
    valid: true,
    name: "InterfaceImpairmentForm",
    delay: '',
    jitter: '',
    loss: '',
    select: null,
    items: [
      'Bidirectional',
      'Incoming',
      'Outgoing',
    ],
    impairmentStatus: ''
  }),

  methods: {
    sendPost () {
      axios
        .post(
            'http://192.168.5.2:8002/api/impairments/set' +
            '?interface=' + this.interface_name +
            '&direction=' + this.select.toLowerCase() +
            '&delay=' + this.delay +
            '&jitter=' + this.jitter +
            '&loss=' + this.loss
        )
        .then(res => {
          console.log(res.body);
        });
    },
    sendGet () {
      axios
        .get(
          'http://192.168.5.2:8002/api/impairments/show' +
          '?interface=' + this.interface_name
        )
        .then(
          response => (this.impairmentStatus = response.data)
        );
    },
    submit () {
      this.$refs.form.validate()
    },
    reset () {
      this.$refs.form.reset()
    },
  },
}
</script>


<style scoped>

</style>
