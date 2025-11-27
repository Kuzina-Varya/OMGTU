<template>
  <div id="app">
    <nav>
      <router-link to="/laureats">Лауреаты</router-link> |
      <router-link to="/prizes">Премии</router-link>
    </nav>
    <main>
      <router-view />
    </main>
    <footer>
      © Лабораторная работа — реактивные таблицы
    </footer>
  </div>
</template>

<style>
:root {
  --bg: #f7f7f8;
  --ink: #1f2328;
  --accent: #5b7fff;
  --bord: #d0d7de;
  --zebra: #ffffff;
  --zebra2: #f2f4f7;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  color: var(--ink);
  background: var(--bg);
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  padding: 16px 20px;
  background: var(--accent);
  color: white;
}

nav {
  background: #111827;
  color: #e5e7eb;
  display: flex;
  gap: 16px;
  padding: 10px 20px;
}
nav a {
  color: #e5e7eb;
  text-decoration: none;
  padding: 6px 10px;
  border-radius: 8px;
}
nav a:hover,
nav a.router-link-active {
  background: rgba(255, 255, 255, 0.12);
}

main {
  max-width: 980px;
  margin: 18px auto;
  padding: 0 16px 40px;
  flex: 1;
}

footer {
  border-top: 1px solid var(--bord);
  color: #6b7280;
  text-align: center;
  padding: 14px 8px;
}
</style>