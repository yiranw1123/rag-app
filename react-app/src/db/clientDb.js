import Dexie from 'dexie';

export const clientDb = new Dexie('questionsDb');

clientDb.version(1).stores({
  chatSessions: '++id, knowledgeBaseId, attachedMessagesCnt',
  questionHistory: '++id, [chatId+questionId], question, answer, sources, *tags',
});

clientDb.open().catch(function (err) {
  console.error('Failed to open db:', err.stack);
});
