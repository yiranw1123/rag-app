import React, { useEffect, useState } from 'react';
import { Container, Grid, Paper, Typography } from '@mui/material';
import styled from '@mui/system/styled';
import ChatNavBar from '../components/chat/navBar.jsx';
import QuestionForm from '../components/chat/newquestion.jsx';
import DetailsAccordion from '../components/chat/kbdetailsaccordin.jsx';
import { useDispatch, useSelector } from 'react-redux';
import { websocketConnecting, websocketDisconnect } from '../features/webSocketState.js';
import ChatDisplay from '../components/chat/chatdisplay.jsx';
import { fetchTags } from '../features/tagState.js';
import{ fetchQuestions } from '../features/questionState.js';
import QuestionPanel from '../components/chat/questionpanel.jsx';
import TagPanel from '../components/chat/tagpanel.jsx';

const Chat = () =>{
  const chatId = useSelector(state => state.chat.chatId);
  const [showQuestionInputForm, setShowQuestionInputForm] = useState(false);
  const dispatch = useDispatch();

  const toggleQuestionForm = () => {
    setShowQuestionInputForm(prev => !prev);
  }

  useEffect(() => {
    dispatch(fetchQuestions({chatId}));
    dispatch(fetchTags({chatId}));
  }, [chatId]);

  useEffect(() => {
    if(showQuestionInputForm) {
      dispatch(websocketConnecting({chatId}));
    } else{
      dispatch(websocketDisconnect());
    }

    return () => {
        dispatch(websocketDisconnect());
    }; 
  }, [showQuestionInputForm, dispatch, chatId]);

  const Item = styled('div')(({ theme }) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
    border: '1px solid',
    borderColor: theme.palette.mode === 'dark' ? '#444d58' : '#ced7e0',
    padding: theme.spacing(1),
    borderRadius: '4px',
    textAlign: 'center',
    height: '100%', 
  }));

  return(
    <>
      <ChatNavBar onToggleQuestionForm = {toggleQuestionForm}/>
      <Container maxWidth={false} style={{ height: '100vh', padding: 0 }}>
      <Grid container spacing={2} style={{ height: '100%' }}>
        {/* Left Column */}
        <Grid item xs={6} style={{ display: 'flex', flexDirection: 'column' }}>
          <Grid item style={{ flex: 1 }}>
            <DetailsAccordion/>
          </Grid>
          <Grid item style={{ flex: 3 }}>
            <Typography variant="h3">Tags</Typography>
            <TagPanel/>
            <Typography variant="h3">Questions</Typography>
            <QuestionPanel/>
          </Grid>
        </Grid>

        {/* Right Column */}
        <Grid item xs={6} style={{ display: 'flex', flexDirection: 'column' }}>
          <Grid container direction="column" style={{ height: '100%' }}>
            <Paper style={{ height: showQuestionInputForm ? '25%' : '0', overflow: 'hidden' }}>
              {showQuestionInputForm && <Item><QuestionForm/></Item>}
            </Paper>
          </Grid>
          <Grid item style={{ flex: 1 }}>
            <Paper style={{ height: '100%', margin: '8px', padding: '16px' }}>
              <ChatDisplay />
            </Paper>
          </Grid>
        </Grid>
      </Grid>
    </Container>
    </>
  );
};

export default Chat;