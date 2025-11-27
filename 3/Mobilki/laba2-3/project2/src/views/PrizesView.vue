<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import ReactiveTable from '@/components/ReactiveTable.vue';
import { PrizesService, NobelPrize } from '@/services/prizes.service';

const page = ref(1);
const searchQuery = ref('');
const prizes = ref<NobelPrize[]>([]);
const loading = ref(false);
const totalPages = ref(1);

const columns = [
  { key: 'year', label: 'Год' },
  { key: 'category', label: 'Категория' },
  { key: 'laureatesCount', label: 'Число лауреатов' }
];

const tableData = computed(() => {
  return prizes.value.map(p => ({
    year: p.year,
    category: p.category,
    laureatesCount: p.laureates ? p.laureates.length : 0
  }));
});

const loadPrizes = async () => {
  loading.value = true;
  try {
    if (searchQuery.value.trim()) {
      const results = await PrizesService.searchByCategory(searchQuery.value.trim());
      prizes.value = results.slice(0, 10);
      totalPages.value = 1;
    } else {
      prizes.value = await PrizesService.getAll(page.value, 10);
      // Получаем общее число премий для пагинации
      const allPrizes = await PrizesService.getAll(1, 1000);
      totalPages.value = Math.ceil(allPrizes.length / 10);
    }
  } catch (e) {
    console.error('Ошибка загрузки премий:', e);
    prizes.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadPrizes();
});

watch([page, searchQuery], () => {
  page.value = 1; // при поиске — сброс на первую страницу
  loadPrizes();
});
</script>

<template>
  <header>
    <h1>Нобелевские премии</h1>
    <div style="margin: 1rem 0">
      <input
        v-model="searchQuery"
        placeholder="Фильтр по категории (например: Физика, Мир и т.д.)"
        style="padding: 8px; width: 350px"
      />
    </div>
  </header>

  <div v-if="loading">Загрузка премий...</div>
  <ReactiveTable v-else :data="tableData" :columns="columns" />

  <div v-if="!searchQuery.trim()" style="margin-top: 1rem; display: flex; gap: 0.5rem; align-items: center">
    <button :disabled="page <= 1" @click="page--">Назад</button>
    <span>Страница {{ page }} из {{ totalPages }}</span>
    <button :disabled="page >= totalPages" @click="page++">Вперёд</button>
  </div>
</template>