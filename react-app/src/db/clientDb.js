import Dexie from 'dexie';

export const clientDb = new Dexie('questionsDb');

clientDb.version(1).stores({
  chatSessions: '++id, knowledgeBaseId, attachedMessagesCnt',
  questionHistory: '++id, chatId, &questionId, [chatId+questionId], question, answer, sources, *tags',
});

clientDb.open().catch(function (err) {
  console.error('Failed to open db:', err.stack);
});

export const getQuestionByQuestionId = async (questionId) =>{
  try {
    const question = await db.questionHistory.get({ questionId });
    console.log("Fetched question:", question);
    return question;
  } catch (error) {
    console.error("Failed to fetch question:", error);
  }
}
