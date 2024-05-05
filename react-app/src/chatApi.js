import { clientDb } from '../src/db/clientDb.js';


export const addChatSessionToDB = async (sessionData) => {
  const id = await clientDb.chatSessions.add(sessionData);
  return {...sessionData, id};
};

export const deleteChatSessionFromDB = async (sessionId) => {
  await clientDb.chatSessions.delete(sessionId);
};

export const addChatHistoryToDB = async (historyData) => {
  const id = await clientDb.chatHistories.add(historyData);
  return {...historyData, id};
};

export const deleteChatHistoryFromDB = async (historyId) => {
  await clientDb.chatHistories.delete(historyId);
};