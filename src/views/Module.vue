<script lang="ts" setup>
  import { computed, ref, reactive, onMounted } from 'vue'
  import axios from 'axios'
  import { ElMessageBox } from 'element-plus';

  const course = reactive<any>([]) // course為響應式陣列
  // 從後端拿取課程資料
  const getCourses = () => {
    axios.get('http://127.0.0.1:9527/api/module',).then((response) => {
      course.splice(0, course.length) // 清空原本的課程清單
      course.push(...response.data.results)
      console.log('更新課程清單')
    })
  }

  // 頁面渲染後更新課程清單
  onMounted(() => {
    getCourses()
  })
</script>

<template>
    <div style="margin: 0 auto; width: 60%;">
      <!-- 標題 -->
      <h1 style="text-align: center">其他學程課程清單</h1>
  
      <!-- 資料表格 -->
      <el-table :data="course" style="width: 100%; font-size: 16px">
        <el-table-column label="學程名稱" prop="學程名稱" />
        <el-table-column label="適用年度" prop="適用年度" />
        <el-table-column label="課程名稱" prop="課程名稱" />
        <el-table-column label="學分數" prop="學分數" />
        <el-table-column label="時數" prop="時數" />
        <el-table-column label="必修/選修" prop="必修/選修" />
        <el-table-column label="必選修子群組" prop="必選修子群組" />
        <el-table-column label="開課年級" prop="開課年級" />
        <el-table-column align="right">
          <template #default="scope">
            <!--<el-button size="small" @click="handleEdit(scope.$index, scope.row)">
              Edit
            </el-button>-->
            
          </template>
        </el-table-column>
      </el-table>
    </div>
  </template>