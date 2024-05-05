import ChatList from '../components/chat/chatlist.jsx';
import ChatWindow from '../components/chat/chatwindow.jsx';
import styles from "./Chat.module.css";
import { useSelector, useDispatch } from 'react-redux';
import React, { useEffect } from 'react';
import {useParams} from 'react-router-dom';
import { fetchActiveChat } from "../features/chatState";
import ButtonAppBar from '../components/chat/navBar.jsx';
import { Container, Grid } from '@mui/material';
import styled from '@mui/system/styled';



const Chat = () =>{
  const dispatch = useDispatch();
  const {id} = useParams();
  const activeChat = useSelector(state => state.chat.activeChat);
  const isLoading = useSelector(state => state.chat.isLoading);

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
  }));

  return(
    <>
      <ButtonAppBar/>
      <Container style={{ height: 'calc(100vh - 64px)' }} maxWidth={false}>
        <Grid container spacing={1}>
          <Grid item xs={4}>
            <Item>1</Item>
          </Grid>
          <Grid item xs={8}>
            <Item>2</Item>
          </Grid>
          <Grid item xs={4}>
            <Item>3</Item>
          </Grid>
          <Grid item xs={8}>
            <Item>4</Item>
          </Grid>
        </Grid>
      </Container>
    </>
  );
};

export default Chat;