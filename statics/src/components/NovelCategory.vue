<template>
  <div class="mbody">
    <div>{{title}}</div>
    <div style="margin-top:10px;text-align:left" v-html="description"></div>
    <div style="margin:10px;">
      <div style="float:left;display:inline">
        <a v-bind:href=getUrl(1)>首页</a>
      </div>
      <div style="float:right;display:inline">
        <a v-if="isDesc" v-on:click=setDesc(2) v-bind:href=getCurUrl(2)>正序</a>
        <a v-else>正序</a>
        <a style="margin-left:10px;margin-right:10px;">|</a>
        <a v-if="!isDesc" v-on:click=setDesc(3) v-bind:href=getCurUrl(3)>倒序</a>
        <a v-else>倒序</a>
      </div>
    </div>
    <div style="margin:auto;text-align:left;margin-top:50px;" >
    <mt-cell v-for="novel in SortNovelList" is-link v-bind:to=getUrl(novel.url) v-bind:title=novel.name></mt-cell>
    </div>
  </div>
</template>
<script>
import Vue from 'vue'
import axios from 'axios'
import { Cell, Indicator } from 'mint-ui'
Vue.component(Cell.name, Cell)
const apiPrefix = 'http://120.79.242.99:8090'
export default {
  name: 'NovelCategory',
  data () {
    return {
      title: '',
      description: '',
      novelList: [],
      isDesc: false
    }
  },
  created: function () {
    Indicator.open('加载中...')
    //this.$http.get('/api/getnovelcategory/' + this.$route.params.category + '/' + this.$route.params.guid).then(response => {
    //  var result = response.body
    //  this.novelList = result.categoryList
    //  this.title = result.title
    //  this.description = result.description
    //  document.title = 'wireboy免费小说 - ' + this.title
    //  Indicator.close()
    //})
    const that = this
    if(that.$route.params.sort == 2)
        axios.post(`${apiPrefix}/get_novel_chapter`,{novel_url:that.$route.params.url,sort:2})
        .then(function (res) {
       if (res.data.status === 'True') {
          that.novelList = res.data.data
          Indicator.close()
          that.isDesc = that.$route.params.sort == 2? true : false
          }
       })

    else if(that.$route.params.sort == 3)
        axios.post(`${apiPrefix}/get_novel_chapter`,{novel_url:that.$route.params.url,sort:3})
        .then(function (res) {
       if (res.data.status === 'True') {
          that.novelList = res.data.data
          Indicator.close()
          that.isDesc = that.$route.params.sort == 2? true : false
          }
       })
    else
    axios.post(`${apiPrefix}/get_novel_chapter`,{novel_url:that.$route.params.url})
    .then(function (res) {
    if (res.data.status === 'True') {
          that.novelList = res.data.data
          Indicator.close()
          that.isDesc = that.$route.params.sort == 2? true : false
          }     
       })
  },
  //mounted: function(){this.gettest()},
  methods: {
    getUrl: function (novel) {
      if(novel == 1)
        return '/'
      return ('/readnovel/' + this.$route.params.url + '/' + novel)
    },
    getCurUrl: function (novel) {
      if(novel == 2)
          return ('/#/novelcategory/' + this.$route.params.url + '/' +'2')
      else if(novel == 3)
          return ('/#/novelcategory/' + this.$route.params.url + '/' +'3')
      else
          return ('/#/novelcategory/' + novel)
    },
    setDesc: function (flag) {
      if(novel == 2) 
          return ('/#/novelcategory/' + this.$route.params.url + '/' +'2')
      else if(novel == 3)
          return ('/#/novelcategory/' + this.$route.params.url + '/' +'3')
      else
          this.isDesc = flag == 1? true : false
    },
    gettest: function(){
    console.log('45631')
     }
  },
  computed:{
     SortNovelList: function () {
       var _this = this;
       var sortFunc = function (a, b) {
          return _this.isDesc? (b.orderNo - a.orderNo) : (a.orderNo - b.orderNo)
       }
       return _this.novelList.sort(sortFunc)
     }
   }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
