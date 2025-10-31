<!-- src/views/LaureatesView.vue -->
<script setup>
import ReactiveTable from '@/components/ReactiveTable.vue'
import { laureates } from '@/data/laureates.js'

const columns = [
  { key: 'name', label: 'Имя / Название' },
  { key: 'birth', label: 'Дата рождения / основания' },
  { key: 'prizes', label: 'Число премий' }
]
</script>

<template>
  <header>
    <h1>Нобелевские лауреаты</h1>
    <p>Имя/название, дата рождения/основания и число премий</p>
  </header>
  <ReactiveTable :data="laureates" :columns="columns" />
</template>