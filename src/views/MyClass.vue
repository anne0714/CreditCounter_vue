<script lang="ts" setup>
  import { computed, ref, reactive, onMounted } from 'vue'
  import axios from 'axios'
  import { ElMessageBox, type TableInstance } from 'element-plus';

  const tableLayout = ref<TableInstance['tableLayout']>('auto')
  const course = reactive<Course[]>([]) // course為響應式陣列

  // 從後端拿取課程資料
  const getCourses = () => {
    if (sessionStorage.getItem("account")) {
      const account = sessionStorage.getItem("account")
      axios.get(`http://127.0.0.1:9527/api/study/${account}`,).then((response) => {
        course.splice(0, course.length) // 清空原本的課程清單
        // 如果沒有課程資料，就新增該學生的主修課程
        if (response.data.results.length === 0) {
          const major = sessionStorage.getItem("major")
          axios.post(`http://127.0.0.1:9527/api/study/${account}`, { class_name: major }).then((response) => {
            console.log('更新課程清單')
          })
          getCourses()
        }else{
          course.push(...response.data.results)
          console.log('獲取課程清單')
        }
      })
    } else {
      ElMessageBox.alert('請先登入', '提示', {
        confirmButtonText: '確定',
        callback: () => {
          window.location.href = '/login'
        }
      })
    }
  }

  // 頁面渲染後更新課程清單
  onMounted(() => {
    getCourses()
  })

  interface Course {
    課程ID: number;
    課程名稱: string;
    學分數: number;
    開課年級: string;
    先修課程名稱: string[];
    修課狀態: string;
    課程類型: string;
  }

  const tableRowClassName = ({
    row,
  }: {
    row: Course
  }) => {
    if (row.修課狀態 === '已修畢') {
    return 'completed-row'
    } else if (row.修課狀態 === '正在修') {
        return 'in-progress-row'
    } else if (row.修課狀態 === '未通過') {
        return 'failed-row'
    } else if (row.修課狀態 === '已停修') {
        return 'stopped-row'
    } else {
    return ''
    }
  }

const handleCommand = (command: string , scope: any) => {
  const account = sessionStorage.getItem("account")
  axios.put(`http://127.0.0.1:9527/api/study/${account}`,
  {"course_id": course[scope.$index].課程ID,"status": command}).then((response) => {
    console.log("編輯課程成功")
    getCourses()
  })
}
</script>

<template>
  <div style="margin: 0 auto; width: 60%;">
    <!-- 標題 -->
    <h1 style="text-align: center">我的課程</h1>

    <!-- 資料表格 -->
    <el-table :data="course" style="width: 100%; font-size: 16px" :row-class-name="tableRowClassName" 
    :table-layout="tableLayout">
      <el-table-column label="課程ID" prop="課程ID" />
      <el-table-column label="課程名稱" prop="課程名稱" />
      <el-table-column label="學分數" prop="學分數" />
      <el-table-column label="開課年級" prop="開課年級" />
      <el-table-column label="先修課程名稱" prop="先修課程名稱" />
      <el-table-column label="修課狀態" prop="修課狀態" >
        <template #default="scope">
          <el-dropdown v-model="course[scope.$index].修課狀態">
            <span class="el-dropdown-link">
              {{ course[scope.$index].修課狀態 }}
              <el-icon color="#303133">
                <arrow-down/>
              </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu >
                <el-dropdown-item @click="handleCommand('已修畢', scope)">已修畢</el-dropdown-item>
                <el-dropdown-item @click="handleCommand('正在修', scope)">正在修</el-dropdown-item>
                <el-dropdown-item @click="handleCommand('未通過', scope)">未通過</el-dropdown-item>
                <el-dropdown-item @click="handleCommand('已停修', scope)">已停修</el-dropdown-item>
                <el-dropdown-item @click="handleCommand('未修課', scope)">未修課</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </el-table-column>
      <el-table-column label="課程類型" prop="課程類型" >
        <template #default="scope">
          <el-tag
            :type="scope.row.課程類型 === '主修' ? '' : 'success'"
            disable-transitions
            >{{ scope.row.課程類型 }}</el-tag
          >
        </template>
      </el-table-column>
      <!--
      <el-table-column align="right">
        資料表格 <template #header>
          <el-input v-model="search" size="small" placeholder="Type to search" />
        </template>
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
            Edit
          </el-button>
          
        </template>
      </el-table-column>
      -->
    </el-table>
  </div>
  <!-- 進度條 
  <div class="demo-progress">
    <el-progress type="dashboard" :percentage="80">
      <template #default="{ percentage }">
        <span class="percentage-value">{{ percentage }}%</span>
        <span class="percentage-label">系必修課程</span>
      </template>
    </el-progress>
    
  </div>
  -->
</template>

<style>
.el-table .completed-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
.el-table .in-progress-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}
.el-table .failed-row {
  --el-table-tr-bg-color: var(--el-color-danger-light-9);
}
.el-table .stopped-row {
  --el-table-tr-bg-color: var(--el-color-gray-light-9);
}

.percentage-value {
  display: block;
  margin-top: 10px;
  font-size: 28px;
}
.percentage-label {
  display: block;
  margin-top: 10px;
  font-size: 16px;
}

.el-table .warning-row {
  --el-table-tr-bg-color: var(--el-color-danger-light-9);
}
.el-table .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>

<style scoped>
.example-showcase .el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}
</style>
