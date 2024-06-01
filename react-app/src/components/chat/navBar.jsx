import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import HomeIcon from '@mui/icons-material/Home';
import AddCommentIcon from '@mui/icons-material/AddComment';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { selectedKbName } from '../../features/chatState';

export default function ChatNavBar({onToggleQuestionForm}) {
  const navigate = useNavigate();
  const kbName = useSelector(selectedKbName)
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" sx={{ backgroundColor: 'rgb(136,179,234)'}}>
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={()=>{navigate('/')}}
          >
            <HomeIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontSize: '32px' }}>
            {kbName}
          </Typography>
          <IconButton color="inherit" onClick={onToggleQuestionForm}><AddCommentIcon/></IconButton>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
