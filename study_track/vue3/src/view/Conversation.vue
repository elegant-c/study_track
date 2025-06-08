<template>
  <div class="trend-analysis">
    <h1>趋势分析</h1>
    
    <div class="gpa-trend-section">
      <h2>绩点趋势图</h2>
      
      <!-- 这里使用现有的LineChart组件 -->
      <LineChart :chartData="chartData" :options="chartOptions" />
      <div class="current-gpa">
		  <h1>预测绩点</h1>
        <span class="gpa-value">4.2</span>
      </div>
      <div class="trend-prediction">
        <h3>趋势预测：</h3>
        <p>如果您能继续保持现在的学习节奏，并稍微注意一下课程难度的调整，我预计您的绩点有望在未来两周内稳定在 4.2 左右。</p>
        <p>这可是相当不错的表现哦！</p>
      </div>
    </div>
    
    <div class="divider"></div>
    
    <div class="semester-info">
      <div class="semester-header">
        <span>2024-2025春季学期</span>
        <a href="#" class="view-details">查看具体成绩</a>
      </div>
      
      <table class="course-table">
        <thead>
          <tr>
            <th>课程名称</th>
            <th>学分</th>
            <th>成绩</th>
            <th>学期</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>计算机网络</td>
            <td>2</td>
            <td>90</td>
            <td>2024-2025春季学期</td>
          </tr>
          <tr>
            <td>数据结构</td>
            <td>4</td>
            <td>85</td>
            <td>2024-2025春季学期</td>
          </tr>
          <tr>
            <td>工科数学</td>
            <td>3</td>
            <td>88</td>
            <td>2024-2025春季学期</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import LineChart from './LineChart.vue';

export default {
  name: 'TrendAnalysis',
  components: {
    LineChart
  },
  data() {
    return {
      chartData: {
        // 这里应该根据实际数据填充
        labels: ['第1周', '第2周', '第3周', '第4周', '第5周', '第6周'],
        datasets: [
          {
            label: '绩点趋势',
            data: [3.8, 3.9, 4.0, 4.1, 4.15, 4.2],
            borderColor: '#4CAF50',
            backgroundColor: 'rgba(76, 175, 80, 0.1)',
            tension: 0.4,
            fill: true
          }
        ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            min: 3.5,
            max: 4.5,
            ticks: {
              stepSize: 0.2
            }
          }
        }
      }
    };
  }
};
</script>

<style scoped>
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

.trend-options {
  display: flex;
  margin-bottom: 20px;
}

.trend-options span {
  padding: 8px 15px;
  margin-right: 10px;
  cursor: pointer;
  border-radius: 4px;
}

.trend-options span.active {
  background-color: #f0f7ff;
  color: #1890ff;
  font-weight: bold;
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

/* 图表容器样式 */
.line-chart-container {
  height: 300px;
  margin: 20px 0;
}
</style>