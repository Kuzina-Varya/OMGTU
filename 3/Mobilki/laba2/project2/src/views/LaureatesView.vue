<!-- src/views/LaureatesView.vue -->
<script setup lang="ts">
import ReactiveTable from '@/components/ReactiveTable.vue';
import { laureates } from '@/data/laureates';
import type { Laureate } from '@/data/laureates';

const columns = [
  { key: 'name', label: 'Имя / Название' },
  { key: 'birth', label: 'Дата рождения / основания' },
  { key: 'prizes', label: 'Число премий' }
] as const;
</script>

<template>
  <header>
    <h1>Нобелевские лауреаты</h1>
    <p>Имя/название, дата рождения/основания и число премий</p>
  </header>
  <ReactiveTable :data="laureates" :columns="columns" />
</template>