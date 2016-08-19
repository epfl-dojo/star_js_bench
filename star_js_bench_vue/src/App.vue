<template>
  <div id="app">
    <img src="./assets/logo.png">
    <h1>{{ msg }}</h1>
    <input id="searchInput" type="text" @keyup="updateSearchResults"/>
    <ul>
      <li v-for="el in results">
        <pre>{{ el }}</pre>
      </li>
    </ul>
  </div>
</template>

<script>

window.searchResults = function searchResults(p, query, maxCount) {
  if (maxCount === undefined) {
    maxCount = 100;
  }
    var result = [];
     for(var i = 0, imax = p.length; i < imax; i++){
       var elt = p[i];
       if(matches(elt, query)){
         result.push(elt);
         if(result.length >= maxCount){
           return result;
         }
       }
     }
     return result;
  }
  function matches(elt, query) {
    return elt.filename.includes(query);
  }

  function isCtrlIsh(event) {
    var os = navigator.platform;
    if (os.startsWith("Mac")) {
      return event.metaKey;
    } else {
      return event.ctrlKey;

    }
  }
  export default {
    data () {
      return {
        msg: 'Hello Vue!',
        results: []
      }
    },
    created (){
      document.onkeydown = function(e) {

        /// for IE
        e = e || event;
        var keyCode = (window.event) ? e.which : e.keyCode;

        /// check ctrl + f key
        if (isCtrlIsh(e) && keyCode === 70) {
          e.preventDefault();
          $("input").focus();
          console.log('Ctrl(ish) + f was hit...');

          return false;
        }
      };
    },
    methods: {
      updateSearchResults () {
        console.log("Updating search results");
        var results = searchResults(p, $("input").val());
        this.results = results;
      }
    }
  }

</script>

<style>
body {
  font-family: Helvetica, sans-serif;
}
</style>
