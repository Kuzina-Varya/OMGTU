<!-- src/views/PrizesView.vue -->
<script setup lang="ts">
import ReactiveTable from '@/components/ReactiveTable.vue';
import { prizes } from '@/data/prizes';
import type { Prize } from '@/data/prizes';

const columns = [
  { key: 'category', label: 'Категория' },
  { key: 'date', label: 'Дата вручения (пример)' },
  { key: 'grant', label: 'Стоимость гранта (пример)' }
] as const;
</script>

<template>
  <header>
    <h1>Нобелевские премии</h1>
    <p>Категории, дата вручения и стоимость гранта</p>
  </header>
  <ReactiveTable :data="prizes" :columns="columns" />
</template>