<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'; // ← Добавь computed!
import ReactiveTable from '@/components/ReactiveTable.vue';
import { LaureatesService, NobelLaureate } from '@/services/laureates.service';

const page = ref(1);
const searchQuery = ref('');
const laureates = ref<NobelLaureate[]>([]);
const totalPages = ref(1);
const loading = ref(false);

const columns = [
  { key: 'name', label: 'Имя / Фамилия' },
  { key: 'born', label: 'Родился' },
  { key: 'prizesCount', label: 'Число премий' }
];

// Вычисляемое поле для таблицы
const tableData = computed(() => {
  return laureates.value.map(l => ({
    name: `${l.firstname || ''} ${l.surname || l.firstname || '-'}`.trim(),
    born: l.born || '-',
    prizesCount: l.prizes?.length || 0
  }));
});

const loadLaureates = async () => {
  loading.value = true;
  try {
    if (searchQuery.value) {
      const results = await LaureatesService.searchByName(searchQuery.value);
      laureates.value = results.slice(0, 10); // показываем первые 10
      totalPages.value = 1;
    } else {
      laureates.value = await LaureatesService.getAll(page.value, 10);
      // Получаем общее число для пагинации (примерно)
      const all = await LaureatesService.getAll(1, 1000);
      totalPages.value = Math.ceil(all.length / 10);
    }
  } catch (e) {
    console.error('Ошибка загрузки лауреатов', e);
  } finally {
    loading.value = false;
  }
};

onMounted(() => loadLaureates());

watch([page, searchQuery], () => {
  page.value = 1; // при поиске — сброс на первую страницу
  loadLaureates();
});
</script>

<template>
  <header>
    <h1>Нобелевские лауреаты</h1>
    <div style="margin: 1rem 0">
      <input v-model="searchQuery" placeholder="Поиск по имени..." style="padding: 8px; width: 300px" />
    </div>
  </header>

  <div v-if="loading">Загрузка...</div>
  <ReactiveTable v-else :data="tableData" :columns="columns" />

  <div v-if="!searchQuery" style="margin-top: 1rem; display: flex; gap: 0.5rem">
    <button :disabled="page <= 1" @click="page--">Назад</button>
    <span>Страница {{ page }} из {{ totalPages }}</span>
    <button :disabled="page >= totalPages" @click="page++">Вперёд</button>
  </div>
</template>