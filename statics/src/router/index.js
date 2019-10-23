import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import MyFirstPage from '@/components/MyFirstPage'
import NovelCategory from '@/components/NovelCategory'
import ReadNovel from '@/components/ReadNovel'

Vue.use(Router)

export default new Router({
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  },
  // mode: 'history',
  routes: [
    {
      path: '/',
      component: MyFirstPage
    },
    {
      path: '/about',
      component: HelloWorld
    },
    {
      path: '/novelcategory/:url/:sort',
      name: 'novelcategory',
      component: NovelCategory
    },
    {
      path: '/readnovel/:category/:url',
      //path: '/readnovel/:category/:guid/:page',
      name: 'readnovel',
      component: ReadNovel
    }
  ]
})
