<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { ElMessage, type FormInstance } from 'element-plus';
import axios from 'axios';
import { el } from 'element-plus/es/locales.mjs';

const signupFormRef = ref<FormInstance>()
const signupForm = reactive({
    account: '',
    password: '',
    major: '',
    second_major: '',
    minor: '',
    education: '',
    access: 0,
})

const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid) => {
      if (valid) {
        axios.post('http://127.0.0.1:9527/api/signup', signupForm).then((response) => {
          if (response.data.status === 'success') {
            console.log('註冊成功')
            formEl.resetFields()
            window.location.href = '/login'
            ElMessage({
                type: 'success',
                message: '註冊成功',
            })
          } else {
            console.log('註冊失敗')
            ElMessage({
                type: 'error',
                message: '帳號或密碼錯誤',
            })
            } 
        })
      }else {
        console.log('請輸入正確格式')
        ElMessage({
            type: 'error',
            message: '請輸入正確格式',
        })
      }
  })
}

const checkAccount = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('請輸入學號'))
  }
  setTimeout(() => {
    if (!Number.isInteger(value)) {
      callback(new Error('請輸入數字'))
    } else {
      if (value.toString().length!== 9) {
        callback(new Error('學號需為9位數'))
      } else {
        callback()
      }
    }
  }, 100)
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
const education = [
    { value: '國小教程', label: '國民小學教育學程' },
    { value: '特教教程身障組', label: '特殊教育學程-國小身障組' },
    { value: '特教教程資優組', label: '特殊教育學程-國小資優組' },
    { value: '特教教程幼教組', label: '特殊教育學程-幼兒園身障組' },
    { value: '幼教教程', label: '幼兒園教育學程' },
]
const 無 = '無'
</script>

<template>
    <el-col style="margin: 0 auto; width: 20%; margin:0 auto;" align="center">
        <!-- 標題 -->
        <h1 style="text-align: center">註冊</h1>
        <!-- 表單 -->
        <el-form :model="signupForm" ref="signupFormRef" label-width="auto" 
        hide-required-asterisk="true" > <!-- 表單內容綁定到signupFormRef -->
            <!-- 帳號 -->
            <el-form-item label="學號" prop = "account" :rules="[
            { validator: checkAccount, trigger: 'blur' },
            ]">
                <el-input v-model.number="signupForm.account" autocomplete="off" />
            </el-form-item>
            <!-- 密碼 -->
            <el-form-item label="密碼" prop = "password" :rules="[
            { required: true, message: '請輸入密碼' },
            { min: 6, message: '密碼長度最少6碼' },]">
                <el-input v-model="signupForm.password" autocomplete="off" />
            </el-form-item>
            <el-form-item label="主修" prop = "major" >
                <el-select v-model="signupForm.major" placeholder="選擇主修" style="width: 240px" :rules="[
                { required: true, message: '請選擇主修' },]">
                    <el-option
                        v-for="item in major"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>
            <el-form-item label="雙主修" prop = "second_major" >
                <el-select v-model="signupForm.second_major" placeholder="選擇雙主修" style="width: 240px":rules="[
                { required: true, message: '請選擇雙主修' },]">
                    <template #header>
                        <el-option
                        :label="無"
                        :value="無"
                        />  
                    </template>
                    <el-option
                        v-for="item in major"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>
            <el-form-item label="輔系" prop = "minor" >
                <el-select v-model="signupForm.minor" placeholder="選擇輔系" style="width: 240px" :rules="[
                { required: true, message: '請選擇輔系' },]">
                    <template #header>
                        <el-option
                        :label="無"
                        :value="無"
                        />  
                    </template>
                    <el-option
                        v-for="item in major"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>
            <el-form-item label="教育學程" prop = "education" >
                <el-select v-model="signupForm.education" placeholder="選擇教育學程" style="width: 240px":rules="[
                { required: true, message: '請選擇教育學程' },]">
                    <template #header>
                        <el-option
                        :label="無"
                        :value="無"
                        />  
                    </template>
                    <el-option
                        v-for="item in education"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>
        </el-form>
        <el-button type="primary" @click="submitForm(signupFormRef)">註冊</el-button>
    </el-col>
</template>