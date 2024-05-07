import { React, useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { useDispatch, useSelector } from 'react-redux';
import { sendMessage, websocketConnecting } from '../../features/webSocketState';
import { addMessage } from '../../features/chatState';

export default function QuestionForm() {
  const chatId = useSelector(state => state.chat.chatId);
  const dispatch = useDispatch();
  const [message, setMessage] = useState('');
  
  useEffect(() =>{
    dispatch(websocketConnecting({chatId}));
  },[]);

  const handleSendMessage =  async () => {
    dispatch(sendMessage(message));
    dispatch(addMessage({'sender': 'me', 'text':message}));
    setMessage(''); // Clear input
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Box
      component="form"
      sx={{
        '& .MuiTextField-root': { m: 1, width: '100%' },
      }}
      noValidate
      autoComplete="off"
    >
      <div>
        <TextField
          id="outlined-multiline-static"
          label="New Question"
          multiline
          rows={4}
          placeholder="Type your question here..."
          onChange={(e) => setMessage(e.target.value)}
          value={message} 
          onKeyDown={handleKeyDown}
        />
      </div>
      <Button variant="contained" onClick={handleSendMessage}>Submit</Button>
    </Box>
  );
}
