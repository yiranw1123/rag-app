import Dexie from 'dexie';

export const clientDb = new Dexie('chatDb');

clientDb.version(1).stores({
  chatSessions: '++id, updateTime, knowledgeBaseId, attachedMessagesCnt',
  chatHistories: '++id, sessionId, role, message, timestamp',
});