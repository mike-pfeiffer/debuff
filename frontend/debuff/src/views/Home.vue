<template>
  <InterfacePanel />
<!--  <InterfaceTabs />-->
</template>

<script lang="ts">
import Vue from "vue";
import InterfacePanel from "@/components/InterfacePanels/InterfacePanel.vue";
// import InterfaceTabs from "@/components/InterfaceTabs/InterfaceTabs.vue";

export default Vue.extend({
  components: {InterfacePanel}
});
</script>
