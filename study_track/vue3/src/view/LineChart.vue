<template>
  <div class="line-chart-container">
    <canvas ref="chartCanvas"></canvas>
    <div v-if="loading" class="loading-message">加载中...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
import { onMounted, ref } from 'vue';

export default {
  name: 'LineChart',
  setup() {
    const chartCanvas = ref(null);
    const loading = ref(true);
    const error = ref(null);
    const studentNo = ref('');
    let chartInstance = null;

    const fetchGpaData = async () => {
      try {
        // 从sessionStorage获取用户信息
        const userInfo = JSON.parse(sessionStorage.getItem("userInfo"));
        studentNo.value = userInfo?.student_no || '';
        
        if (!studentNo.value) {
          throw new Error('未获取到学号信息');
        }

        loading.value = true;
        error.value = null;
        
        // 构建API请求URL
        const apiUrl = `http://127.0.0.1:8000/semester_gpa/${studentNo.value}`;
        const response = await fetch(apiUrl);
        
        if (!response.ok) {
          throw new Error('获取数据失败');
        }
        
        const data = await response.json();
        return data;
      } catch (err) {
        error.value = err.message || '获取绩点数据时出错';
        return null;
      } finally {
        loading.value = false;
      }
    };

    const renderChart = (gpaData) => {
      // 确保数据存在且不为空
      if (!gpaData || gpaData.length === 0) {
        error.value = '没有可用的绩点数据';
        return;
      }
      
      // 处理数据
      const labels = gpaData.map(item => item.semester);
      const dataPoints = gpaData.map(item => item.semester_gpa);
      
      // 计算Y轴范围，留出一些空间
      const minValue = Math.min(...dataPoints) - 0.2;
      const maxValue = Math.max(...dataPoints) + 0.2;
      
      // 如果已有图表实例，先销毁
      if (chartInstance) {
        chartInstance.destroy();
      }
      
      // 创建新图表
      if (chartCanvas.value) {
        const ctx = chartCanvas.value.getContext('2d');
        
        chartInstance = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: '绩点趋势',
              data: dataPoints,
              borderColor: '#4CAF50',
              backgroundColor: 'rgba(76, 175, 80, 0.1)',
              borderWidth: 2,
              tension: 0.4,
              fill: true,
              pointBackgroundColor: '#fff',
              pointBorderColor: '#4CAF50',
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                mode: 'index',
                intersect: false
              }
            },
            scales: {
              y: {
                min: minValue,
                max: maxValue,
                ticks: {
                  stepSize: 0.1,
                  callback: function(value) {
                    return value.toFixed(2);
                  }
                },
                grid: {
                  color: 'rgba(0, 0, 0, 0.05)'
                }
              },
              x: {
                grid: {
                  display: false
                }
              }
            },
            interaction: {
              mode: 'nearest',
              axis: 'x',
              intersect: false
            }
          }
        });
      }
    };

    onMounted(async () => {
      // 注册所有Chart.js组件
      Chart.register(...registerables);
      
      // 获取数据并渲染图表
      const gpaData = await fetchGpaData();
      if (gpaData) {
        renderChart(gpaData);
      }
    });

    return { chartCanvas, loading, error };
  }
};
</script>

<style scoped>
.line-chart-container {
  position: relative;
  height: 300px;
  width: 100%;
  margin: 20px 0;
}

.loading-message, .error-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  text-align: center;
}

.error-message {
  color: #f44336;
}
</style>