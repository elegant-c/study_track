<template>
  <div class="course-list">
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>课程名称</th>
          <th>学期</th>
          <th>成绩</th>
          <th>学分</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in courses" :key="course.id">
          <td>{{ course.id }}</td>
          <td>{{ course.course_name }}</td>
          <td>{{ course.semester }}</td>
          <td>{{ course.score }}</td>
          <td>{{ course.credit }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'CourseList',
  props: {
    courses: {
      type: Array,
      required: true
    }
  }
}
</script>

<style scoped>
.course-list {
  width: 90%;
  max-width: 1000px;
}

table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

th, td {
  border: 1px solid #ddd;
  padding: 12px 15px;
  text-align: center;
}

th {
  background-color: #f2f2f2;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
}



</style>