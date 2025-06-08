<template>
  <div class="trend-analysis">
    <h1>趋势分析</h1>
    
    <div class="gpa-trend-section">
      <h2>绩点趋势图</h2>
      
      <LineChart :chartData="chartData" :options="chartOptions" />
      <div class="current-gpa">
        <h1>{{ prediction.semester ? `${prediction.semester}预测绩点` : '预测绩点' }}</h1>
        <span class="gpa-value">{{ prediction.gpa || '--' }}</span>
      </div>
      <div class="trend-prediction">
        <h3>趋势预测：</h3>
        <template v-if="prediction.trend_analysis">
          <p v-for="(paragraph, index) in formattedAnalysis" :key="index">{{ paragraph }}</p>
        </template>
        <p v-else-if="loading">数据加载中...</p>
        <p v-else>暂无趋势分析数据</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import LineChart from './LineChart.vue';

export default {
  name: 'TrendAnalysis',
  components: {
    LineChart
  },
  data() {
    return {
      student_no: '',
      loading: false,
      chartData: {
        labels: [],
        datasets: [{
          label: '绩点趋势',
          data: [],
          borderColor: '#4CAF50',
          backgroundColor: 'rgba(76, 175, 80, 0.1)',
          tension: 0.4,
          fill: true
        }]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            min: 3.0,
            max: 4.5,
            ticks: { stepSize: 0.2 }
          }
        }
      },
      prediction: {
        semester: null,
        gpa: null,
        trend_analysis: null
      }
    };
  },
  computed: {
    formattedAnalysis() {
      if (!this.prediction.trend_analysis) return [];
      // 按换行符分割分析文本为多个段落
      return this.prediction.trend_analysis.split('\n').filter(p => p.trim());
    }
  },
  async mounted() {
  const userInfo = JSON.parse(sessionStorage.getItem("userInfo"));
  this.student_no = userInfo?.student_no || '';

  if (!this.student_no) {
    console.warn("未从 sessionStorage 获取到 student_no");
    return;
  }

  await this.fetchSemesterGPA();
  await this.predictGPA();
}
,
  methods: {
    async fetchSemesterGPA() {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/semester_gpa/${this.student_no}`);
        const labels = res.data.map(item => item.semester);
        const gpaValues = res.data.map(item => item.semester_gpa);
        this.chartData.labels = labels;
        this.chartData.datasets[0].data = gpaValues;
      } catch (err) {
        console.error('获取GPA数据失败', err);
      }
    },
    async predictGPA() {
      this.loading = true;
      try {
        const res = await axios.post('http://127.0.0.1:8000/predict_gpa', {
          student_no: this.student_no
        });
        this.prediction = {
          semester: res.data.prediction.semester,
          gpa: res.data.prediction.gpa,
          trend_analysis: res.data.prediction.trend_analysis
        };
      } catch (err) {
        console.error('GPA预测失败', err);
        this.prediction.trend_analysis = '获取趋势分析失败，请稍后重试';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
/* 保持原有样式不变 */
.trend-analysis {
  font-family: 'Arial', sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  color: #333;
}

h1 {
  font-size: 24px;
  margin-bottom: 30px;
  color: #2c3e50;
}

.gpa-trend-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

h2 {
  font-size: 18px;
  margin-bottom: 15px;
  color: #2c3e50;
}

.current-gpa {
  text-align: center;
  margin: 20px 0;
}

.gpa-value {
  font-size: 36px;
  font-weight: bold;
  color: #4CAF50;
}

.trend-prediction {
  margin-top: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.trend-prediction h3 {
  font-size: 16px;
  margin-bottom: 10px;
}

.trend-prediction p {
  margin: 5px 0;
  line-height: 1.5;
}

.divider {
  height: 1px;
  background-color: #e8e8e8;
  margin: 25px 0;
}

.semester-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.view-details {
  color: #1890ff;
  text-decoration: none;
  font-size: 14px;
}

.course-table {
  width: 100%;
  border-collapse: collapse;
}

.course-table th, .course-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e8e8e8;
}

.course-table th {
  font-weight: 500;
  color: #666;
}

.course-table tr:hover {
  background-color: #f5f5f5;
}

.line-chart-container {
  height: 300px;
  margin: 20px 0;
}
</style>