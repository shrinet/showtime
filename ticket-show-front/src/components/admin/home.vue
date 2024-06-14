<template>
 <div>
     <router-view></router-view>
 </div>
  
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

onMounted( () => {
    if (sessionStorage.getItem("adminpanel") != undefined) router.push('admin') ;
}) 

</script>
