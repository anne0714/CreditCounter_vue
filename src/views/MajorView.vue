<script lang="ts" setup>
  import { computed, ref, reactive, onMounted } from 'vue'
  import axios from 'axios'
  import { ElMessageBox, type TableInstance } from 'element-plus';

  const art_course = reactive<any>([]) // course為響應式陣列
  const cs_course = reactive<any>([])
  const tableLayout = ref<TableInstance['tableLayout']>('auto')
  // 從後端拿取課程資料
  const getCourses = () => {
    axios.get('http://127.0.0.1:9527/api/major_course/藝設系設計組',).then((response) => {
      art_course.splice(0, art_course.length) // 清空原本的課程清單
      art_course.push(...response.data.results)
      console.log('更新課程清單')
    })
    axios.get('http://127.0.0.1:9527/api/major_course/資科系',).then((response) => {
      cs_course.splice(0, cs_course.length) // 清空原本的課程清單
      cs_course.push(...response.data.results)
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
    <h1 style="text-align: center">藝設系設計組專門課程</h1>
    <!-- 資料表格 -->
    <el-table :data="art_course" style="width: 100%; font-size: 16px" :table-layout="tableLayout">
      <el-table-column label="課程ID" prop="課程ID" />
      <el-table-column label="課程名稱" prop="課程名稱" />
      <el-table-column label="學分數" prop="學分數" />
      <el-table-column label="時數" prop="時數" />
      <el-table-column label="必修/選修" prop="必修/選修" />
      <el-table-column label="開課年級" prop="開課年級" />
      <el-table-column align="right">
        <template #default="scope">
          <!--<el-button size="small" @click="handleEdit(scope.$index, scope.row)">
            Edit
          </el-button>-->
          
        </template>
      </el-table-column>
    </el-table>
    <!-- 標題 -->
    <h1 style="text-align: center">資科系專門課程</h1>
    <!-- 資料表格 -->
    <el-table :data="cs_course" style="width: 100%; font-size: 16px":table-layout="tableLayout">
      <el-table-column label="課程ID" prop="課程ID" />
      <el-table-column label="課程名稱" prop="課程名稱" />
      <el-table-column label="學分數" prop="學分數" />
      <el-table-column label="時數" prop="時數" />
      <el-table-column label="必修/選修" prop="必修/選修" />
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