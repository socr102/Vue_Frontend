<template>
  <div id="products">
    <div class="title-details">
      <ProductTabs />
    </div>
  </div>
</template>

<script>
import ProductTabs from "./ProductTabs.vue";
export default {
  name: 'Products',
  components: {
      ProductTabs
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>