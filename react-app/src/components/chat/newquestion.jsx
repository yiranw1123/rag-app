import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

export default function QuestionForm() {
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
          defaultValue="Type your question here..."
        />
      </div>
      <Button variant="contained">Submit</Button>
    </Box>
  );
}
