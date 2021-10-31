<template>
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
            hint="Current Values: Incoming: 10 | Outgoing: 10"
            persistent-hint
        ></v-text-field>

        <v-text-field
            v-model="jitter"
            label="Jitter"
            hint="Current Value: 10"
            persistent-hint
        ></v-text-field>

        <v-text-field
            v-model="loss"
            label="Loss"
            hint="Current Value: 10"
            persistent-hint
        ></v-text-field>
        <v-divider class="mt-4"></v-divider>
        <v-card-actions>
          <v-btn
              :disabled="!valid"
              color="success"
              class="mr-4"
              @click="submit"
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
</template>

<script>
export default {
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
    ]
  }),

  methods: {
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