<template>
  <div class="grade-management">
    <h1>成绩管理</h1>

    <!-- 显示提示信息 -->
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
    <p v-if="successMessage" style="color: green;">{{ successMessage }}</p>

    <div class="controls">
      <button class="add-course-btn" @click="showAddCourseDialog = true">
        添加课程
      </button>

      <div class="sort-option">
        <span>排序方式:</span>
        <select v-model="sortBy">
          <option value="id">ID</option>
          <option value="name">课程名称</option>
          <option value="grade">成绩</option>
          <option value="credit">学分</option>
        </select>
      </div>
    </div>

    <div class="course-list-container">
      <CourseList 
        :courses="sortedCourses" 
      />
    </div>

    <AddCourseDialog 
      v-if="showAddCourseDialog"
      @close="showAddCourseDialog = false"
      @add-course="addCourse"
    />
  </div>
</template>

<script>
import CourseList from './CourseList.vue';
import AddCourseDialog from './AddCourseDialog.vue';
import axios from "axios";

export default {
  name: 'GradeManagement',
  components: {
    CourseList,
    AddCourseDialog
  },
  data() {
    return {
      student_no: "", // 初始为空，将从sessionStorage获取
      sortBy: 'id',
      showAddCourseDialog: false,
      courses: [],
      errorMessage: "",
      successMessage: ""
    };
  },
  computed: {
    sortedCourses() {
      return [...this.courses].sort((a, b) => {
        if (this.sortBy === 'id') return a.id - b.id;
        if (this.sortBy === 'name') return a.course_name.localeCompare(b.course_name);
        if (this.sortBy === 'grade') return b.score - a.score;
        if (this.sortBy === 'credit') return b.credit - a.credit;
        return 0;
      });
    }
  },
  async mounted() {
    try {
      const userInfo = JSON.parse(sessionStorage.getItem("userInfo"));
      this.student_no = userInfo?.student_no || '';
      
      if (!this.student_no) {
        console.warn("未从 sessionStorage 获取到 student_no");
        this.errorMessage = "无法获取学生信息";
        return;
      }

      const res = await axios.get(`http://127.0.0.1:8000/grades/${this.student_no}`);
      this.courses = res.data.map((c, index) => ({
        id: c.course_code,  
        course_name: c.course_name,
        semester: c.semester,
        score: c.score,
        credit: c.credit
      }));
    } catch (error) {
      this.errorMessage = "无法加载成绩数据";
    }
  },
  methods: {
    translateError(detail) {
      const errorMap = {
        "Grade already exists for this student, course, and semester": "该课程在本学期已有成绩记录",
        "Course not found": "课程不存在"
      };
      return errorMap[detail] || detail;
    },
    
    async addCourse(newCourse) {
      try {
        this.errorMessage = "";
        this.successMessage = "";
        
        const payload = {
          student_no: this.student_no,
          course_name: newCourse.course_name,  // 统一使用 course_name
          semester: newCourse.semester,
          score: Number(newCourse.score)       // 统一使用 score 并确保是数字
        };

        const res = await axios.post("http://127.0.0.1:8000/insert_grade", payload);

        if (res.data.msg === "success") {
          this.successMessage = "课程添加成功！";
          this.showAddCourseDialog = false;
          
          // 重新加载课程列表以确保数据最新
          const refreshRes = await axios.get(`http://127.0.0.1:8000/grades/${this.student_no}`);
          this.courses = refreshRes.data.map(c => ({
            id: c.course_code,
            course_name: c.course_name,
            semester: c.semester,
            score: c.score,
            credit: c.credit
          }));
        } else if (res.data.detail) {
          throw new Error(res.data.detail);
        }
      } catch (error) {
        this.successMessage = "";
        if (error.response?.data?.detail) {
          this.errorMessage = this.translateError(error.response.data.detail);
        } else if (error.message) {
          this.errorMessage = this.translateError(error.message);
        } else {
          this.errorMessage = "添加失败: 请检查网络或后端服务";
        }
      }
    }
  }
};
</script>

<style scoped>
.grade-management {
  padding: 20px;
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
}

.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 20px;
}

.add-course-btn {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.add-course-btn:hover {
  background-color: #45a049;
}

.sort-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-option select {
  padding: 6px 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.course-list-container {
  display: flex;
  justify-content: center;
  width: 100%;
}
</style>
