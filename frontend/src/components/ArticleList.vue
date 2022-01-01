<template>
  <div>
    <div v-for="article in info.results" v-bind:key="article.url" id="articles">
      <router-link
        :to="{ name: 'ArticleDetail', params: { id: article.id } }"
        class="article-title"
      >
        {{ article.title }}
      </router-link>
      <div>
        {{ formatted_time(article.created) }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data: function () {
    return {
      info: "",
    };
  },
  mounted() {
    axios.get("/api/article").then((response) => (this.info = response.data));
  },
  methods: {
    formatted_time: function (iso_date_string) {
      const date = new Date(iso_date_string);
      return date.toLocaleDateString();
    },
  },
};
</script>

<style>
#articles {
  padding: 10px;
}

.article-title {
  font-size: large;
  font-weight: bolder;
  color: black;
  text-decoration: none;
  padding: 5px 0 5px 0;
}
</style>