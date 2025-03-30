<template>
  <div class="search-container">
    <h1>Busca de Operadoras</h1>
    <input type="text" v-model="query" placeholder="Digite sua busca" />
    <button @click="search">Buscar</button>

    <ul v-if="results.length" class="result-list">
      <li v-for="(item, index) in results" :key="index">
        {{ item }}
      </li>
    </ul>
    <p v-else class="no-result">Sem resultados.</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: '',
      results: []
    }
  },
  methods: {
    async search() {
      try {
        const response = await fetch(`http://localhost:5000/search?query=${this.query}`);
        const data = await response.json();
        this.results = data;
      } catch (error) {
        console.error('Erro ao buscar dados:', error);
      }
    }
  }
}
</script>

<style scoped>

</style>
