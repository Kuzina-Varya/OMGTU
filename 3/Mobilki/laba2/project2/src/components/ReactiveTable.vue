<template>
  <table>
    <thead>
      <tr>
        <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(row, index) in data" :key="index">
        <td v-for="col in columns" :key="col.key">
          {{ row[col.key] }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
defineProps({
  data: {
    type: Array,
    required: true
  },
  columns: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
/* Скопируем стили из styles.css, но только для таблицы */
table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border: 1px solid var(--bord);
  border-radius: 12px;
  overflow: hidden;
}
thead th {
  text-align: left;
  background: #eef2ff;
  border-bottom: 1px solid var(--bord);
  padding: 12px 14px;
  font-weight: 600;
}
tbody td {
  border-bottom: 1px solid var(--bord);
  padding: 12px 14px;
  vertical-align: top;
}
tbody tr:nth-child(even) { background: var(--zebra2); }
tbody tr:nth-child(odd) { background: var(--zebra); }
</style>