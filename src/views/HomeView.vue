<script lang="ts" setup>
  import { computed, ref, reactive, onMounted, getCurrentInstance } from 'vue'
  import axios from 'axios'
  import { ElButton, ElMessage, ElMessageBox } from 'element-plus';
  import type {ElTable, FormInstance, TableInstance} from 'element-plus'

  const dialogFormVisible = ref(false)
  const editFormVisible = ref(false)
  const admin = ref(false)
  if (sessionStorage.getItem("access")=== "1") {
    admin.value = true
  }
  const formLabelWidth = '140px'
  const tableLayout = ref<TableInstance['tableLayout']>('auto')
  const FormRef = ref<FormInstance>()
  const editFormRef = ref<FormInstance>()
  const form = reactive({
    course_name: '',
    credit: '',
    hours: '',
    open: '',
  })
  const editform = reactive({
    id: '',
    course_name: '',
    credit: '',
    hours: '',
    open: '',
  })

  const course = reactive<Course[]>([])
  interface Course {
    課程ID: number;
    課程名稱: string;
    學分數: number;
    時數: number;
    開課單位: string;
    課程類型: string;
    學分學程名稱?: string; // 新增的臨時字段
    學分學程必修?: number;
    學分學程年度?: number;
    開課年級?: string;
    學分學程群組?: number; 
    主修班級?: string;
    主修必修?: number;
    主修開課年級?: string;
    雙主修?: boolean;
    輔系?: boolean;
    主修群組?: number;
    主修年度?: number;
  }

  const major = [
  { value: '教育系', label: '教育學系' },
  { value: '社發系', label: '社會與區域發展學系' },
  { value: '特教系', label: '特殊教育學系' },
  { value: '幼教系', label: '幼兒與家庭教育學系' },
  { value: '心諮系', label: '心理與諮商學系' },
  { value: '教經系', label: '教育經營與管理學系' },
  { value: '語創系師資組', label: '語文與創作學系師資組' },
  { value: '語創系創作組', label: '語文與創作學系創作組' },
  { value: '音樂系', label: '音樂學系' },
  { value: '兒英系', label: '兒童英語教育學系' },
  { value: '藝設系藝術組', label: '藝術與造型設計學系藝術組' },
  { value: '藝設系設計組', label: '藝術與造型設計學系設計組' },
  { value: '文創系', label: '文化創意產業經營學系' },
  { value: '體育系', label: '體育學系' },
  { value: '自然系', label: '自然科學教育學系' },
  { value: '數資系AI組', label: '數學暨資訊教育學系AI資教組' },
  { value: '數資系數學組', label: '數學暨資訊教育學系數學組' },
  { value: '資科系', label: '資訊科學系' },
  { value: '數位系', label: '數位科技設計學系' }
]

  const getCourses = () => {
    axios.get('http://127.0.0.1:9527/api/course',).then((response) => {
      course.splice(0, course.length)
      course.push(...response.data.results)
      console.log('更新課程清單')
    })
  }

  // 頁面渲染後更新課程清單
  onMounted(() => {
    getCourses()
  })

  // 刪除課程
  const handleDelete = (index: number, scope: any) => {
    ElMessageBox.confirm('確定要刪除課程嗎？','警告', {confirmButtonText: '確定', cancelButtonText: '取消', type: 'warning',})
    .then(() => { 
      console.log(index, scope)
      axios.delete(`http://127.0.0.1:9527/api/course/${scope.課程ID}`).then((response) => {
        getCourses()
        ElMessage({
          type: 'success',
          message: '刪除成功',
        })
      })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '刪除已取消',
      })
    })
  }

  const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
      if (valid) {
        axios.post('http://127.0.0.1:9527/api/course', form).then((response) => {
          console.log('新增課程成功')
          dialogFormVisible.value = false
          formEl.resetFields()
          getCourses()
          ElMessage({
            type: 'success',
            message: '新增成功',
          })
        })
      } else {
        console.log('error submit!', fields)
      }
    })
  }
  // 顯示編輯課程表單
  const handleEdit = (index: number, scope: any) => {
    // 將 scope 的屬性複製到 editform
    editform.id = scope.課程ID
    editform.course_name = scope.課程名稱
    editform.credit = scope.學分數
    editform.hours = scope.時數
    editform.open = scope.開課單位
    editFormVisible.value = true
    console.log(editform)
  }
  // 編輯課程表單提交
  const submitEditForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
      if (valid) {
        axios.put('http://127.0.0.1:9527/api/course', editform).then((response) => {
          console.log('編輯課程成功')
          editFormVisible.value = false
          formEl.resetFields()
          getCourses()
          ElMessage({
            type: 'success',
            message: '編輯成功',
          })
        })
      } else {
        console.log('error submit!', fields)
      }
    })
  }

  const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
  }

  const multipleTableRef = ref<InstanceType<typeof ElTable>>()
  const selectedForms = ref<Course[]>([])
  const groupCourseVisible = ref(false)
  const handleSelectionChange = () => {
    selectedForms.value = multipleTableRef.value!.getSelectionRows()
    console.log(selectedForms)
    groupCourseVisible.value = true
  }
  const refList = ref<FormInstance[]>([])
  const setItemRef = el => {
    if (el) {
      refList.value.push(el)
    }
  }

  const groupCourse = async () => {
    let allValid = true;

    for (const formRef of refList.value) {
      if (!allValid){
        break;
      }
      if (formRef) {
        await formRef.validate((valid) => {
          if (!valid) {
            allValid = false;
            console.log('error submit!');
            return;
          }else {
            console.log('valid submit!');
          }
        });
      }
    }

    if (allValid) {
      selectedForms.value.forEach((course) => {
        if (course.課程類型 === '學分學程') {
          axios.post('http://127.0.0.1:9527/api/module', {
            course_id: course.課程ID,
            name: course.學分學程名稱,
            required: course.學分學程必修,
            year: course.學分學程年度,
            open_grade: course.開課年級,
            course_group: course.學分學程群組,
          }).then((response) => {
            console.log('學分學程更新成功', course)
          }).catch((error) => {
            console.error('學分學程更新失敗', error)
          })
        }else if (course.課程類型 === '主修課程') {
          axios.post('http://127.0.0.1:9527/api/major_course', {
            course_id: course.課程ID,
            class: course.主修班級,
            required: course.主修必修,
            open_grade: course.主修開課年級,
            course_group: course.主修群組,
            year: course.主修年度,
            second: course.雙主修,
            minor: course.輔系,
          }).then((response) => {
            console.log('主修課程更新成功', course)
          }).catch((error) => {
            console.error('主修課程更新失敗', error, course)
          })
        }
      })
      groupCourseVisible.value = false
      ElMessage({
        type: 'success',
        message: '課程歸類成功',
      })
      getCourses()
    }
  }
</script>

<template>
  <div style="margin: 0 auto; width: 60%;">
    <!-- 標題 -->
    <h1 style="text-align: center">學分管理系統</h1>
    <!--新增課程-->
    <el-button plain @click="dialogFormVisible = true" v-if = "admin">
    新增課程
    </el-button>
    <el-button plain @click="handleSelectionChange" v-if = "admin">
    歸類課程
    </el-button>
    <!-- 新增課程表單 -->
    <el-dialog v-model="dialogFormVisible" title="新增課程" width="500" >
      <el-form :model="form" ref="FormRef"> <!-- 表單內容綁定到FormRef -->
        <el-form-item label="課程名稱" :label-width="formLabelWidth" prop = "course_name" :rules="[
          { required: true, message: '請輸入課程名稱' },]">
          <el-input v-model="form.course_name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="學分" :label-width="formLabelWidth" prop = "credit" :rules="[
          { required: true, message: '請輸入學分' },
          { type: 'number', message: '請輸入數字' },
        ]">
          <el-input v-model.number="form.credit" autocomplete="off" />
        </el-form-item>
        <el-form-item label="時數" :label-width="formLabelWidth" prop = "hours" :rules="[
          { required: true, message: '請輸入時數' },
          { type: 'number', message: '請輸入數字' },
        ]">
          <el-input v-model.number="form.hours" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="開課單位" :label-width="formLabelWidth" :rules="[
          { required: true, message: '請選擇開課單位' },]" autocomplete="off">
          <el-select v-model="form.open" placeholder="請選擇一個開課單位">
            <el-option label="校共同必修" value="校共同必修" />
            <el-option label="大一、二體育" value="大一、二體育" />
            <el-option label="通識課" value="通識課" />
            <el-option label="藝設系" value="藝設系" />
            <el-option label="藝設系設計組" value="藝設系設計組" />
            <el-option label="藝設系藝術組" value="藝設系藝術組" />
            <el-option label="資科系" value="資科系" />
          </el-select>
        </el-form-item>
      </el-form>
      <!-- 表單取消確認按鈕 -->
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="resetForm(FormRef)">清除</el-button>
          <el-button type="primary" @click="submitForm(FormRef)">
            新增
          </el-button>
        </div>
      </template>
    </el-dialog>
    <!-- 資料表格 -->
    <el-table :data="course" style="width: 100%; font-size: 16px" :table-layout="tableLayout" 
     ref="multipleTableRef">
      <el-table-column type="selection" width="55" v-if = "admin" />
      <el-table-column label="課程ID" prop="課程ID" />
      <el-table-column label="課程名稱" prop="課程名稱" />
      <el-table-column label="學分數" prop="學分數" />
      <el-table-column label="時數" prop="時數" />
      <el-table-column label="開課單位" prop="開課單位" />
      <el-table-column align="right">
        <!-- 搜尋
        <template #header>
          <el-input v-model="search" size="small" placeholder="Type to search" />
        </template>-->
        <template #default="scope"> 
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)" v-if = "admin">
            編輯
          </el-button>
          <el-button
            size="small"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)" v-if = "admin">
            刪除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 編輯課程表單 -->
    <el-dialog v-model="editFormVisible" title="編輯課程" width="500" >
      <el-form :model="editform" ref="editFormRef"> <!-- 表單內容綁定到FormRef -->
        <el-form-item label="課程ID" :label-width="formLabelWidth" prop = "id" :rules="[
          { required: true, message: '請輸入課程ID' },
          { type: 'number', message: '請輸入數字' },
        ]">
          <el-input v-model.number="editform.id" autocomplete="off" disabled/>
        </el-form-item>
        <el-form-item label="課程名稱" :label-width="formLabelWidth" prop = "course_name" :rules="[
          { required: true, message: '請輸入課程名稱' },]">
          <el-input v-model="editform.course_name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="學分" :label-width="formLabelWidth" prop = "credit" :rules="[
          { required: true, message: '請輸入學分' },
          { type: 'number', message: '請輸入數字' },
        ]">
          <el-input v-model.number="editform.credit" autocomplete="off" />
        </el-form-item>
        <el-form-item label="時數" :label-width="formLabelWidth" prop = "hours" :rules="[
          { required: true, message: '請輸入時數' },
          { type: 'number', message: '請輸入數字' },
        ]">
          <el-input v-model.number="editform.hours" autocomplete="off" />
        </el-form-item>
        <el-form-item label="開課單位" :label-width="formLabelWidth" :rules="[
          { required: true, message: '請選擇開課單位' },]">
          <el-select v-model="editform.open" placeholder="請選擇一個開課單位">
            <el-option label="校共同必修" value="校共同必修" />
            <el-option label="大一、二體育" value="大一、二體育" />
            <el-option label="通識課" value="通識課" />
            <el-option label="藝設系" value="藝設系" />
            <el-option label="藝設系設計組" value="藝設系設計組" />
            <el-option label="藝設系藝術組" value="藝設系藝術組" />
          </el-select>
        </el-form-item>
      </el-form>
      <!-- 表單取消確認按鈕 -->
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="resetForm(FormRef)">清除</el-button>
          <el-button type="primary" @click="submitEditForm(editFormRef)">
            確認
          </el-button>
        </div>
      </template>
    </el-dialog>
    <!-- 歸類課程表單 -->
    <el-dialog v-model="groupCourseVisible" title="歸類課程" width="500" >
      <!-- 多個表單 -->
      <div >
        <el-form :model="oneCourse" v-for="(oneCourse, index) in selectedForms" :key="oneCourse.課程ID" :ref="setItemRef"> 
          <el-form-item label="課程ID" :label-width="formLabelWidth" prop="課程ID">
            <el-input v-model.number="oneCourse.課程ID" autocomplete="off" disabled />
          </el-form-item>
          <el-form-item label="課程名稱" :label-width="formLabelWidth" prop="課程名稱">
            <el-input v-model="oneCourse.課程名稱" autocomplete="off" disabled/>
          </el-form-item>
          <el-form-item label="學分數" :label-width="formLabelWidth" prop="學分數">
            <el-input v-model.number="oneCourse.學分數" autocomplete="off" disabled/>
          </el-form-item>
          <el-form-item label="時數" :label-width="formLabelWidth" prop = "時數" >
            <el-input v-model.number="oneCourse.時數" autocomplete="off" disabled/>
          </el-form-item>
          <el-form-item label="開課單位" :label-width="formLabelWidth" prop="開課單位">
            <el-select v-model="oneCourse.開課單位" placeholder="請選擇一個開課單位" disabled>
            </el-select>
          </el-form-item>
          <el-form-item label="課程類型" :label-width="formLabelWidth" prop="課程類型">
            <el-select v-model="oneCourse.課程類型" placeholder="請選擇一個課程類型" >
              <el-option label="主修課程" value="主修課程" />
              <el-option label="校共同必修" value="校共同必修" />
              <el-option label="大一、二體育" value="大一、二體育" />
              <el-option label="通識課" value="通識課" />
              <el-option label="學分學程" value="學分學程" />
            </el-select>
          </el-form-item>
          <el-form-item v-if="oneCourse.課程類型 === '學分學程'" label="學分學程名稱" prop="學分學程名稱" :label-width="formLabelWidth" :rules="[
            { required: true, message: '請輸入學分學程名稱' },
          ]">
            <el-input v-model="oneCourse.學分學程名稱" autocomplete="off" />
          </el-form-item>
          <el-form-item v-if="oneCourse.課程類型 === '學分學程'" label="學分學程年度" prop="學分學程年度" :label-width="formLabelWidth" :rules="[
            { required: true, message: '請輸入年度' },
            { type: 'number', message: '請輸入數字' },
          ]">
            <el-input v-model.number="oneCourse.學分學程年度" autocomplete="off" />
          </el-form-item>
          <el-form-item v-if="oneCourse.課程類型 === '學分學程'" label="必修/選修" prop="學分學程必修" :label-width="formLabelWidth" >
            <el-switch v-model="oneCourse.學分學程必修" 
            active-text="必修"
            inactive-text="選修"
            active-value="1"
            inactive-value="0" />     
          </el-form-item>
          <el-form-item v-if="oneCourse.課程類型 === '學分學程'" label="學分學程群組" prop="學分學程群組" :label-width="formLabelWidth" :rules="[
            { required: true, message: '請輸入課程群組' },
            { type: 'number', message: '請輸入數字' },
          ]">
            <el-input v-model.number="oneCourse.學分學程群組" autocomplete="off" />
          </el-form-item>
          <el-form-item v-if="oneCourse.課程類型 === '學分學程'" label="開課年級" prop="開課年級" :label-width="formLabelWidth" :rules="[
            { required: true, message: '請輸入開課年級' },
          ]">
            <el-input v-model="oneCourse.開課年級" autocomplete="off" />
          </el-form-item>
          <el-form-item v-if="oneCourse.課程類型 === '主修課程'" label="主修班級" prop="主修班級" :label-width="formLabelWidth" >
            <el-select v-model="oneCourse.主修班級" placeholder="選擇主修班級" style="width: 240px" :rules="[
              { required: true, message: '請選擇主修' },]">
                    <el-option
                        v-for="item in major"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
            </el-select>
          </el-form-item>
          <el-form-item v-if="oneCourse.課程類型 === '主修課程'" label="主修年度" prop="主修年度" :label-width="formLabelWidth" :rules="[
            { required: true, message: '請輸入主修年度' },
            { type: 'number', message: '請輸入數字' },
          ]">
            <el-input v-model.number="oneCourse.主修年度" autocomplete="off" />
          </el-form-item>
          <el-form-item v-if="oneCourse.課程類型 === '主修課程'" label="必修/選修" prop="主修必修" :label-width="formLabelWidth">
            <el-switch v-model="oneCourse.主修必修"
              active-text="必修"
              inactive-text="選修"
              active-value="1"
              inactive-value="0" />     
          </el-form-item>
          <el-form-item v-if="oneCourse.課程類型 === '主修課程'" label="主修群組" prop="主修群組" :label-width="formLabelWidth" :rules="[
            { required: true, message: '請輸入主修群組' },
            { type: 'number', message: '請輸入數字' },
          ]">
            <el-input v-model.number="oneCourse.主修群組" autocomplete="off" />
          </el-form-item>
          <el-form-item v-if="oneCourse.課程類型 === '主修課程'" label="開課年級" prop="主修開課年級" :label-width="formLabelWidth" :rules="[
            { required: true, message: '請輸入開課年級' },
          ]">
            <el-input v-model="oneCourse.主修開課年級" autocomplete="off" />
          </el-form-item>
          <el-form-item v-if="oneCourse.課程類型 === '主修課程'" label="雙主修課程" prop="雙主修" :label-width="formLabelWidth">
            <el-switch v-model="oneCourse.雙主修"
              active-text="是"
              inactive-text="否"
              active-value="1"
              inactive-value="0" />
          </el-form-item>
          <el-form-item v-if="oneCourse.課程類型 === '主修課程'" label="輔系課程" prop="輔系" :label-width="formLabelWidth">
            <el-switch v-model="oneCourse.輔系"
              active-text="是"
              inactive-text="否"
              active-value="1"
              inactive-value="0" />
          </el-form-item>
          <el-divider />
        </el-form>
        
      </div>
      <!-- 表單確認按鈕 -->
      <template #footer>
        <el-button type="primary" @click="groupCourse()">
          確認
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>