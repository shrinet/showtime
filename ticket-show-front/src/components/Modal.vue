<template>
  <div
    class="modal fade"
    :id="props.id"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
            {{ props.name }}
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body p-4">
          <template v-for="(element, index) in Array(5).fill('f')" :key="index">
            <i
              class="fa-solid fa-star star"
              :class="[star >= index +1 ? 'color' : '']"
              @click="fill(index + 1)"
              :id="index"
            >
            </i>
          </template>
          <textarea v-model="text" cols="30" rows="10"></textarea>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button
            type="button"
            @click="emit('update_review', text, props.id, star)"
            class="btn btn-primary"
          >
            Save changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from "vue";

const emit = defineEmits(["update_review"]);
const text = ref("");
const star = ref(0);
const props = defineProps({
  id: Number,
  name: String,
});

function fill(index) {
  star.value = index;
  console.log(star.value);
}
</script>

<style scoped>
textarea {
  resize: none;
  width: 100%;
  padding: 10px;
  outline: none;
}

.star {
  margin-bottom: 13px;
  font-size: 20px;
  margin-inline: 5px;
  cursor: pointer;
}
.color{
  color: blue;
}
</style>