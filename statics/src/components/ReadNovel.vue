<template>
  <div class="mbody">
    <div style="text-align:left">
      <a v-bind:href=getUrl(1)>首页</a>
      <a v-bind:href=getUrl(2)>目录</a>
    </div>
    <div>
      {{title}}
    </div>
    <!--<div style="margin:auto;text-align:left;margin-top:30px;text-indent:2em;white-space:pre-wrap;" v-html="content" >
      {{content}}
    </div>-->
    <div style="margin:auto;text-align:left;margin-top:30px;text-indent:2em;white-space:pre-wrap;" >
    {{content}}</div>
    <div>
      <a v-if="prePageEnable" v-bind:href=getUrl(prePage)>上一页</a>
      <a v-else>上一页</a>
      <a style="margin-left:10px;margin-right:10px;">|</a>
      <a v-if="lastPageEnable" v-bind:href=getUrl(lastPage)>下一页</a>
      <a v-else>下一页</a>
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
  name: 'ReadNovel',
  data () {
    return {
      title: '',
      content: '',
      lastPage: '',
      prePage: '',
      lastPageEnable: false,
      prePageEnable: false
    }
  },
  created: function () {
    this.initPage()
  },
  methods: {
    getUrl: function (page) {
      var result = '/'
      if (page === 1) {
        result = '/'
      } else if (page === 2) {
        result = ('/#/novelcategory/' + this.$route.params.category)
      } else if (page) {
        result = ('/#/readnovel/' + this.$route.params.category  + '/' + page)
      }
      return result
    },
    initPage: function () {
      Indicator.open('加载中...')
     // this.$http.get('/api/readnovel/' + this.$route.params.category + '/' + this.$route.params.guid + '/' + this.$route.params.page).then(response => {
     //   this.content = response.body.content
     //   this.title = response.body.title
     //   this.prePage = response.body.prePage
     //   this.lastPage = response.body.lastPage
     //   this.prePageEnable = this.prePage.length > 0? true : false
     //   this.lastPageEnable = this.lastPage.length > 0? true : false
     //   document.title = 'wireboy免费小说 - ' + this.title
     //   Indicator.close()
     // })
      const that = this
      axios.post(`${apiPrefix}/get_novel_chapter_content`,{chapter_url:that.$route.params.url})
      .then(function (res){
        if (res.data.status === 'True'){
          that.content = res.data.data.content
          that.prePage = res.data.data.prev_url
          that.lastPage = res.data.data.next_url
          that.prePageEnable = that.prePage.length > 0? true : false
          that.lastPageEnable = that.lastPage.length > 0? true : false
          document.title = res.data.data.title
          Indicator.close()
     }
      })
    }
 },
  watch: {
    '$route' (to, from) {
      this.initPage(this.$route.path)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
