import { defineStore } from 'pinia'

// Types
export interface Exercise {
    type: string
    content: string
}

export interface TherapyPlan {
    exercises: Exercise[]
    feedback: string
}

export interface SessionData {
    id?: number
    user_id: string
    dialect: string
    transcript: string
    fluency_score: number
    severity: string
    therapy_plan: TherapyPlan
    created_at?: string
}

export const useSessionStore = defineStore('session', {
    state: () => ({
        userId: 'guest',
        dialect: 'Madurai',
        dialects: ['Kongu', 'Madurai', 'Tirunelveli', 'Chennai'],
        isRecording: false,
        liveTranscript: '',
        liveScore: null as any,
        liveTherapy: null as TherapyPlan | null,
        history: [] as SessionData[],
        audioPlaying: false
    }),
    actions: {
        setDialect(d: string) {
            this.dialect = d
        },
        updateLiveTranscript(t: string) {
            this.liveTranscript = t
        },
        updateLiveScore(s: any) {
            this.liveScore = s
        },
        updateLiveTherapy(th: TherapyPlan | null) {
            this.liveTherapy = th
        },
        setHistory(h: SessionData[]) {
            this.history = h
        }
    }
})
