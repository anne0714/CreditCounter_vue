<script lang="ts" setup>
import axios from 'axios';
import { ElMessage, type FormInstance } from 'element-plus';
import type { pa } from 'element-plus/es/locales.mjs';
import { reactive, ref } from 'vue'

const loginForm = reactive({
    account: '',
    password: '',
})
const loginFormRef = ref<FormInstance>()

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

const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
      if (valid) {
        axios.post('http://127.0.0.1:9527/api/login', loginForm).then((response) => {
          if (response.data.status === 'success') {
            console.log('登入成功')
            sessionStorage.setItem("account", loginForm.account); //存入sessionStorage
            sessionStorage.setItem("major", response.data.major); //存入主修系別到session
            sessionStorage.setItem("access", response.data.access); //存入姓名到session
            formEl.resetFields()
            ElMessage({
                type: 'success',
                message: '登入成功',
            })
            window.location.href = '/myclass'
          } else {
            console.log('登入失敗')
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

const signup = () => {
  window.location.href = '/signup'
}
</script>

<template>
    <el-col style="margin: 0 auto; width: 20%; margin:0 auto;" align="center">
        <!-- 標題 -->
        <h1 style="text-align: center">登入</h1>
        <!-- 表單 -->
        <el-form :model="loginForm" ref="loginFormRef" label-width="auto" 
        hide-required-asterisk="true" > <!-- 表單內容綁定到loginFormRef -->
            <!-- 帳號 -->
            <el-form-item label="學號" prop = "account" :rules="[
            { validator: checkAccount, trigger: 'blur' },
            ]">
                <el-input v-model.number="loginForm.account" autocomplete="off" />
            </el-form-item>
            <!-- 密碼 -->
            <el-form-item label="密碼" prop = "password" :rules="[
            { required: true, message: '請輸入密碼' },
            { min: 6, message: '密碼長度最少6碼' },]">
                <el-input v-model="loginForm.password" autocomplete="off" />
            </el-form-item>
            
        </el-form>
        <el-button type="primary" @click="signup">沒有帳號？立即註冊</el-button>
        <el-button type="primary" @click="submitForm(loginFormRef)">登入</el-button>
    </el-col>
</template>