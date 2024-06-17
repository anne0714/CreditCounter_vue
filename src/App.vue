<script lang="ts" setup>
import { ref } from 'vue';

const isAccount = ref(false)
if (sessionStorage.getItem("account")) {
  isAccount.value = true
}

const logout = () => {
  sessionStorage.clear()
  isAccount.value = false
  window.location.href = '/'
}
</script>

<template>
  <p>
    <strong>Current route path:</strong> {{ $route.fullPath }}
  </p>
  <nav>
    <el-button type="primary" 
    plain round
    @click="$router.push('/')">
      所有課程
    </el-button>
    <el-button type="primary" 
    plain round
    @click="$router.push('/major')">
      專門課程
    </el-button>
    <el-button type="primary" 
    plain round
    @click="$router.push('/module')">
      其他學程
    </el-button>
    <el-button type="primary" 
    plain round
    @click="$router.push('/myclass')">
      我的課程
    </el-button>
    <el-button type="primary" 
    plain round
    @click="$router.push('/login')"
    v-if="!isAccount">
      登入
    </el-button>
    <el-button type="primary" 
    plain round
    @click="logout"
    v-if="isAccount">
      登出
    </el-button>
  </nav>
  <main>
    <RouterView />
  </main>
</template>

<style scoped lang="scss">
  body {font-family: Inter, 'Helvetica Neue', Helvetica, 'PingFang SC',
  'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;}
</style>