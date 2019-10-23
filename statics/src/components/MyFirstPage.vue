<template>
  <div class="mbody">
    <div>
      <h1>{{ msg }}</h1>
      <!--<input style="width:400px;" v-model="text"><button v-on:click="getData">查询</button>-->
      <mt-field placeholder="请输入小说名称" v-model="name"><mt-button @click.native="getData">查询</mt-button></mt-field>
    </div>
    <div style="margin:auto;text-align:left;margin-top:30px;" >
    <mt-cell v-for="novel in novelList" is-link v-bind:to=getUrl(novel.url) v-bind:title=novel.book_name>
    </mt-cell>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import { Cell, Search, Indicator } from 'mint-ui'
Vue.component(Cell.name, Cell)
Vue.component(Search.name, Search)
const apiPrefix = 'http://120.79.242.99:8090'
export default {
  name: 'MyFirstPage',
  data () {
    return {
      msg: '小说搜索',
      novelList: [],
      text: '',
      hisKey: '',
      nextPage: 1
    }
  },
  methods: {
    getData: function () {
      Indicator.open('加载中...')
      //this.$http.post('/api/SearchNovel/' + this.text).then(response => {
      //  var result = response.body
      //  this.hisKey = result.key
      //  this.novelList = result.itemList
        // this.nextPage = 1 + result.pageIndex
      //  Indicator.close()
      //})
      const that = this
      axios.post(`${apiPrefix}/search_novel`, { novel: this.name })
      .then(function (res){
       console.log(res.data.status)
      if (res.data.status === 'True')
          console.log('123')
          that.novelList = res.data.data
          Indicator.close()
      })
      
    },
    getUrl: function (novel) {
      return ('/novelcategory/' + novel + '/' + 4)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
