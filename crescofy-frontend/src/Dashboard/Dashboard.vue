<template>
    <MainMenu />
    <TopBar title="Analytics" :author="{
    home: 'Home',
    cart: 'Analytics'
  }"
   />
    <Products />
</template>

<script>
    import { reactive } from "vue";
    import { Modal, Toast } from "bootstrap";
    import TopBar from "../Menu/TopBar.vue";
    import MainMenu from "../Menu/MainMenu.vue";
    import Products from "./components/Products.vue";

    export default {
        name: "Home",
        components: {
            TopBar,
            Products,
            MainMenu
        },
    };
</script>