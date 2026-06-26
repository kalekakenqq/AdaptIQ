import { defineStore } from "pinia";

let nextId = 1;

export const useNotificationStore = defineStore("notifications", {
  state: () => ({
    items: [],
  }),

  actions: {
    push(message, type = "info") {
      const id = nextId++;
      this.items.push({ id, message, type });
      setTimeout(() => this.remove(id), 3000);
    },

    remove(id) {
      this.items = this.items.filter((item) => item.id !== id);
    },
  },
});
