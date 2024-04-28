import { createContext, useContext } from 'react';

// Define the context with a default value that has a similar structure
export const ActiveChatContext = createContext({
  activeChat: null,
  setActiveChat: () => {}  // empty function as placeholder
});


export const useActiveChat =() =>{
  const context = useContext(ActiveChatContext);

  if (context === undefined) {
    throw new Error('useActiveChat must be used with a ActiveChatContext');
  }

  return context;
}