import { create } from 'zustand';

export type Enclave = {
  name: string;
  status: string;
  nodes: number;
  type: string;
  lastActive: string;
};

export type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  status?: 'loading' | 'done';
  loadingText?: string;
  attachments?: { name: string; type: string }[];
};

export type Session = {
  id: string;
  title: string;
  status: string;
  time: string;
  messages: Message[];
};

interface AppState {
  enclaves: Enclave[];
  addEnclave: (enclave: Enclave) => void;
  removeEnclave: (index: number) => void;
  updateEnclaveType: (index: number, type: string) => void;

  workloadTypes: string[];
  addWorkloadType: (type: string) => void;
  removeWorkloadType: (type: string) => void;
  
  sessions: Session[];
  createNewSession: (initialMessage: Message) => string;
  addMessageToSession: (sessionId: string, message: Message) => void;
  updateMessageInSession: (sessionId: string, messageId: string, updates: Partial<Message>) => void;
}

export const useAppStore = create<AppState>((set) => ({
  enclaves: [
    { name: "Core Intelligence", status: "active", nodes: 24, type: "Production", lastActive: "Just now" },
    { name: "Threat Analysis V2", status: "processing", nodes: 8, type: "Research", lastActive: "2 hrs ago" },
    { name: "Legacy DB Migration", status: "offline", nodes: 0, type: "Archived", lastActive: "3 weeks ago" },
    { name: "Neural Network Training", status: "active", nodes: 128, type: "Cluster", lastActive: "1 min ago" },
    { name: "Web Server Fleet", status: "active", nodes: 6, type: "Production", lastActive: "10 mins ago" },
  ],
  addEnclave: (enclave) => set((state) => ({ enclaves: [enclave, ...state.enclaves] })),
  removeEnclave: (index) => set((state) => {
    const newEnclaves = [...state.enclaves];
    newEnclaves.splice(index, 1);
    return { enclaves: newEnclaves };
  }),
  updateEnclaveType: (index, type) => set((state) => {
    const newEnclaves = [...state.enclaves];
    newEnclaves[index] = { ...newEnclaves[index], type };
    return { enclaves: newEnclaves };
  }),

  workloadTypes: ["Research & Analysis", "Production Server", "Compute Cluster", "Cold Storage"],
  addWorkloadType: (type) => set((state) => ({ workloadTypes: [...state.workloadTypes, type] })),
  removeWorkloadType: (type) => set((state) => ({
    workloadTypes: state.workloadTypes.filter((t) => t !== type),
    enclaves: state.enclaves.map((e) => e.type === type ? { ...e, type: "Requires Update" } : e)
  })),

  sessions: [
    {
      id: "1",
      title: "Analyze telemetry logs",
      status: "done",
      time: "Today",
      messages: [
        {
          id: "1", role: "user", content: "Can you scan the attached syslog for any unauthorized egress attempts?", attachments: []
        },
        {
          id: "2", role: "assistant", content: "I have analyzed the `syslog_export.txt`. The enclave is secure. There were 14 blocked outbound attempts from a quarantined container, but the hypervisor rules prevented any actual egress.", status: "done"
        }
      ]
    },
    { id: "2", title: "Compile NPU drivers", status: "active", time: "Today", messages: [] },
    { id: "3", title: "Scan local network", status: "progress", time: "Yesterday", messages: [] },
  ],
  
  createNewSession: (initialMessage) => {
    const sessionId = Date.now().toString();
    const newSession: Session = {
      id: sessionId,
      title: initialMessage.content.slice(0, 30) + (initialMessage.content.length > 30 ? "..." : "") || "New Chat",
      status: "active",
      time: "Today",
      messages: [initialMessage]
    };
    
    set((state) => ({
      sessions: [newSession, ...state.sessions]
    }));
    
    return sessionId;
  },
  
  addMessageToSession: (sessionId, message) => set((state) => ({
    sessions: state.sessions.map((session) => 
      session.id === sessionId 
        ? { ...session, messages: [...session.messages, message] }
        : session
    )
  })),
  
  updateMessageInSession: (sessionId, messageId, updates) => set((state) => ({
    sessions: state.sessions.map((session) => 
      session.id === sessionId 
        ? { 
            ...session, 
            messages: session.messages.map(msg => 
              msg.id === messageId ? { ...msg, ...updates } : msg
            ) 
          }
        : session
    )
  })),
}));
