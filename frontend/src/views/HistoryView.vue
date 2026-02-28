<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="pa-4 elevator-3 rounded-xl mb-4" theme="dark">
          <v-card-title>Weekly Summary</v-card-title>
          <div class="d-flex justify-space-between text-caption text-grey">
            <span>Sessions</span>
            <span class="font-weight-bold ml-2 text-white">{{ history.length }}</span>
          </div>
          <div class="d-flex justify-space-between text-caption text-grey mt-2">
            <span>Overall Fluency Delta</span>
            <span class="font-weight-bold ml-2 text-success">+14%</span>
          </div>
          <div class="d-flex justify-space-between text-caption text-grey mt-2">
            <span>Streak</span>
            <span class="font-weight-bold ml-2 text-warning"><v-icon size="small" color="warning">mdi-fire</v-icon> 5 Days</span>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" md="8">
         <v-card class="pa-4 elevator-3 rounded-xl" theme="dark">
            <v-card-title>Fluency Progress</v-card-title>
            <div style="height: 250px" class="pa-2">
                <LineChart :data="chartData" :options="chartOptions" />
            </div>
         </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <v-card theme="dark" class="rounded-xl elevator-3">
          <v-card-title class="d-flex align-center">
            Session History
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              variant="tonal"
              prepend-icon="mdi-file-pdf-box"
              @click="exportPdf"
            >
              Export PDF
            </v-btn>
          </v-card-title>
          <v-table>
            <thead>
              <tr>
                <th class="text-left">Date</th>
                <th class="text-left">Dialect</th>
                <th class="text-left">Fluency Score</th>
                <th class="text-left">Severity</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="session in mockHistory" :key="session.id">
                <td>{{ session.date }}</td>
                <td>{{ session.dialect }}</td>
                <td>
                  <v-progress-linear
                    :model-value="session.score * 100"
                    color="primary"
                    height="12"
                    rounded
                  ></v-progress-linear>
                  <span class="text-caption">{{ Math.round(session.score * 100) }}%</span>
                </td>
                <td>
                  <v-chip :color="session.severity === 'mild' ? 'success' : 'warning'" size="small">
                    {{ session.severity.toUpperCase() }}
                  </v-chip>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Line as LineChart } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

// Mock Data for UI since DB isn't hydrated natively without starting supabase edge
const mockHistory = ref([
 { id: 1, date: '2026-02-23', dialect: 'Madurai', score: 0.55, severity: 'moderate' },
 { id: 2, date: '2026-02-24', dialect: 'Kongu', score: 0.62, severity: 'moderate' },
 { id: 3, date: '2026-02-25', dialect: 'Tirunelveli', score: 0.68, severity: 'mild' },
 { id: 4, date: '2026-02-26', dialect: 'Madurai', score: 0.74, severity: 'mild' },
 { id: 5, date: '2026-02-27', dialect: 'Kongu', score: 0.81, severity: 'mild' }
])

const history = computed(() => mockHistory.value)

const chartData = computed(() => ({
  labels: history.value.map(h => h.date),
  datasets: [
    {
      label: 'Fluency Score',
      backgroundColor: '#5CBBF6',
      borderColor: '#1867C0',
      data: history.value.map(h => h.score * 100),
      tension: 0.4,
      fill: true
    }
  ]
}))

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      max: 100
    }
  }
})

function exportPdf() {
  alert('Export PDF stub: Logic requires jsPDF or similar.')
}
</script>
