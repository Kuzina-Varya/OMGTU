<script setup>
import ReactiveTable from '@/components/ReactiveTable.vue'
import { prizes } from '@/data/prizes.js'

const columns = [
  { key: 'category', label: 'Категория' },
  { key: 'date', label: 'Дата вручения (пример)' },
  { key: 'grant', label: 'Стоимость гранта (пример)' }
]
</script>

<template>
  <header>
    <h1>Нобелевские премии</h1>
    <p>Категории, дата вручения и стоимость гранта</p>
  </header>
  <ReactiveTable :data="prizes" :columns="columns" />
</template>