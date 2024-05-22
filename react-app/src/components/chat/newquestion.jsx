import { React, useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { useDispatch } from 'react-redux';
import { sendMessage } from '../../features/webSocketState';
import {v4 as uuid} from "uuid";

export default function QuestionForm() {
  const dispatch = useDispatch();
  const [message, setMessage] = useState('');

  const handleSendMessage =  async () => {
    const newMessage = {
      id: Date.now().toString(),
      question: message
    };
    dispatch(sendMessage(newMessage));
    setMessage('');
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
