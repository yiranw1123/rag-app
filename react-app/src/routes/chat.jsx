import { useSelector, useDispatch } from 'react-redux';
import React, { useEffect, useState } from 'react';
import {useParams} from 'react-router-dom';
import { fetchActiveChat } from "../features/chatState";
import { Container, Grid } from '@mui/material';
import styled from '@mui/system/styled';
import ChatNavBar from '../components/chat/navBar.jsx';
import QuestionForm from '../components/chat/newquestion.jsx';
import DetailsAccordion from '../components/chat/kbdetailsaccordin.jsx';

const Chat = () =>{
  const [showQuestionInputForm, setShowQuestionInputForm] = useState(false);
  const dispatch = useDispatch();
  const {id} = useParams();
  const activeChat = useSelector(state => state.chat.activeChat);
  const isLoading = useSelector(state => state.chat.isLoading);
  const questionFormHeight = showQuestionInputForm ? '35%' : '0%'; // Adjust percentage as necessary
  const item4Height = showQuestionInputForm ? '65%' : '100%'; // Adjust so total is always 100%

  const toggleQuestionForm = () => {
    setShowQuestionInputForm(prev => !prev);
  }

  useEffect(() => {
    const loadChat = async () =>{
      if(id) {
        dispatch(fetchActiveChat(id));
      }
    };
    loadChat();
  }, [id, dispatch]);

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
      <Container style={{ height: 'calc(100vh - 64px)'}} maxWidth={false}>
      <Grid container spacing={1} style={{ height: '100vh' }}> {/* Full viewport height */}
        {/* Column for details + prev questions */}
        <Grid item xs={4}>  {/* Takes up 4 out of 12 columns */}
          <Item>
            <DetailsAccordion />
          </Item>
        </Grid>

        {/* Column for new question + chat display */}
        <Grid item xs={8}>  {/* Takes up 8 out of 12 columns */}
          <Grid container direction="column" style={{ height: '100%' }}>
            <Grid item style={{ height: questionFormHeight }}>
              {showQuestionInputForm && <Item><QuestionForm/></Item>}
            </Grid>
            <Grid item style={{ flexGrow: 1 }}>
              <Item>Chat Display Area</Item>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
      </Container>

    </>
  );
};

export default Chat;