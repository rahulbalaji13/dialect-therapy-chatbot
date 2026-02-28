<template>
  <v-app>
    <v-app-bar color="primary" app>
      <v-toolbar-title>Dialect Therapy Chatbot</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text to="/" exact>Therapy</v-btn>
      <v-btn text to="/history">History</v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>


<style>
/* Global styles */
body {
  font-family: 'Inter', sans-serif;
  background-color: #121212;
  color: #fff;
}
</style>
