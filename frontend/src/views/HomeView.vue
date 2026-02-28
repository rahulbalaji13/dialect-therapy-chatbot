<template>
  <v-container>
    <v-row>
      <!-- Controls & Status -->
      <v-col cols="12" md="4">
        <v-card class="pa-4 elevator-3 mb-4 rounded-xl" theme="dark">
          <v-card-title>Therapy Session</v-card-title>
          <v-select
            v-model="dialect"
            :items="dialects"
            label="Select Dialect"
            variant="outlined"
            class="mt-4"
          ></v-select>

          <v-row class="mt-2 text-center" justify="center">
            <v-btn
              :color="isRecording ? 'error' : 'success'"
              size="x-large"
              icon
              @click="toggleRecording"
            >
              <v-icon>{{ isRecording ? 'mdi-stop' : 'mdi-microphone' }}</v-icon>
            </v-btn>
          </v-row>
          <div class="text-caption text-center mt-2">
            {{ isRecording ? 'Listening...' : 'Ready to record' }}
          </div>

          <!-- Waveform placeholder -->
          <div v-if="isRecording" class="waveform-container mt-6">
            <div class="bar" v-for="n in 10" :key="n" :style="{ animationDelay: n * 0.1 + 's' }"></div>
          </div>
        </v-card>

        <!-- Metric Details -->
        <v-card v-if="liveScore" class="pa-4 elevator-3 rounded-xl mt-4" theme="dark">
           <v-card-title>Session Metrics</v-card-title>
           <div class="text-subtitle-1">Severity: 
              <v-chip :color="severityColor" text-color="white">{{ liveScore.severity.toUpperCase() }}</v-chip>
           </div>
           
           <!-- Impediment Gauge representation -->
           <v-progress-circular
              :model-value="liveScore.fluency_score * 100"
              :color="gaugeColor"
              size="120"
              width="15"
              class="mt-4 mb-2 mx-auto d-flex"
            >
              <span class="text-h5 font-weight-bold">{{ Math.round(liveScore.fluency_score * 100) }}</span>
            </v-progress-circular>
            <div class="text-center text-caption mb-4">Fluency Score</div>

            <v-divider class="mb-2"></v-divider>
            <div v-for="(pat, i) in liveScore.detected_patterns" :key="i" class="text-body-2 mb-1">
              <v-icon color="warning" size="small" class="mr-1">mdi-alert-circle</v-icon> {{ pat }}
            </div>
        </v-card>
      </v-col>

      <!-- Main Activity Area -->
      <v-col cols="12" md="8">
        <!-- Live Transcript -->
        <v-card class="pa-4 rounded-xl mb-4" height="200" theme="dark">
           <v-card-title>Live Transcript</v-card-title>
           <v-card-text class="text-body-1 transcript-box">
             {{ liveTranscript || 'Transcription will appear here...' }}
           </v-card-text>
        </v-card>

        <!-- Therapy Plan Generated -->
        <v-card v-if="liveTherapy" class="pa-4 rounded-xl" theme="dark">
           <v-card-title class="text-primary d-flex align-center">
             <v-icon class="mr-2">mdi-human-greeting-proximity</v-icon> Therapy Plan
             <v-spacer></v-spacer>
             <v-btn icon color="primary" variant="tonal" @click="playFeedback" :loading="isAudioPlaying">
               <v-icon>mdi-volume-high</v-icon>
             </v-btn>
           </v-card-title>
           
           <v-card-text>
             <div class="text-body-1 bg-grey-darken-3 pa-3 rounded mb-4">
               <em>"{{ liveTherapy.feedback }}"</em>
             </div>

             <v-row>
               <v-col cols="12" v-for="(ex, i) in liveTherapy.exercises" :key="i">
                 <v-card variant="outlined" class="pa-3 border-primary" theme="dark">
                   <div class="d-flex align-center">
                     <v-chip size="small" color="secondary" class="mr-3">{{ ex.type.replace('_', ' ').toUpperCase() }}</v-chip>
                     <span class="text-body-1">{{ ex.content }}</span>
                   </div>
                 </v-card>
               </v-col>
             </v-row>
           </v-card-text>
        </v-card>
        
        <v-card v-else-if="!isRecording && !liveScore" class="pa-8 text-center rounded-xl d-flex align-center justify-center flex-column" height="300" theme="dark">
            <v-icon size="64" color="grey-darken-1">mdi-microphone-outline</v-icon>
            <div class="text-h6 text-grey mt-4">Start recording to generate your personalized dialect therapy</div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useSessionStore } from '../store/session'
import { io, Socket } from 'socket.io-client'

const store = useSessionStore()

const dialect = computed({
  get: () => store.dialect,
  set: (val) => store.setDialect(val)
})
const dialects = store.dialects

const isRecording = ref(false)
const liveTranscript = computed(() => store.liveTranscript)
const liveScore = computed(() => store.liveScore)
const liveTherapy = computed(() => store.liveTherapy)
const isAudioPlaying = ref(false)

const gaugeColor = computed(() => {
  if (!liveScore.value) return 'grey'
  const sc = liveScore.value.fluency_score
  if (sc > 0.8) return 'success'
  if (sc > 0.5) return 'warning'
  return 'error'
})

const severityColor = computed(() => {
  if (!liveScore.value) return 'grey'
  const sev = liveScore.value.severity
  if (sev === 'mild') return 'success'
  if (sev === 'moderate') return 'warning'
  return 'error'
})

let mediaRecorder: MediaRecorder | null = null
let socket: Socket | null = null
let audioChunks: Blob[] = []
let lastFeedbackAudioB64 = ''

onMounted(() => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'
  socket = io(`${backendUrl}/live-session`)

  socket.on('connect', () => {
    console.log('Connected to AI back-end')
  })

  socket.on('transcript_live', (data) => {
    store.updateLiveTranscript(data.text)
  })

  socket.on('score_live', (data) => {
    store.updateLiveScore(data.score)
  })

  socket.on('therapy_live', (data) => {
    store.updateLiveTherapy(data.therapy)
  })
  
  socket.on('audio_feedback', (data) => {
    lastFeedbackAudioB64 = data.audio_b64
    playFeedback()
  })

  socket.on('status_update', (data) => {
    console.log('Server status:', data.step)
  })
})

onUnmounted(() => {
  if (socket) socket.disconnect()
})

async function toggleRecording() {
  if (isRecording.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []

    mediaRecorder.ondataavailable = (e) => {
      audioChunks.push(e.data)
    }

    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
      store.updateLiveTranscript('Processing...')
      store.updateLiveScore(null)
      store.updateLiveTherapy(null)
      
      if (socket) {
        socket.emit('audio_chunk', {
          dialect: dialect.value,
          audio: audioBlob
        })
      }
      
      // Stop traces
      stream.getTracks().forEach(track => track.stop())
    }

    mediaRecorder.start()
    isRecording.value = true
  } catch (err) {
    console.error('Mic access denied:', err)
  }
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
  }
  isRecording.value = false
}

function playFeedback() {
  if (!lastFeedbackAudioB64) return
  isAudioPlaying.value = true
  const audio = new Audio("data:audio/mp3;base64," + lastFeedbackAudioB64)
  audio.play()
  audio.onended = () => {
    isAudioPlaying.value = false
  }
}
</script>

<style scoped>
.transcript-box {
  max-height: 120px;
  overflow-y: auto;
  scrollbar-width: thin;
}

.waveform-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 40px;
  gap: 4px;
}

.bar {
  width: 6px;
  height: 100%;
  background: #5CBBF6;
  border-radius: 4px;
  animation: equalize 1s ease-in-out infinite;
}

@keyframes equalize {
  0% { height: 10px; }
  50% { height: 40px; }
  100% { height: 10px; }
}

.rounded-xl {
  border-radius: 16px !important;
}

.border-primary {
  border-color: rgba(24, 103, 192, 0.4) !important;
}
</style>
