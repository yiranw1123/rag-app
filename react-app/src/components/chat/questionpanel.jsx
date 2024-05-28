import { useSelector } from "react-redux";
import { selectQuestions } from "../../features/questionState";
import { Grid, List, ListItem, ListItemText, Paper } from '@mui/material';

const QuestionPanel = () =>{
  const questions = useSelector(selectQuestions);

  return(
    <Paper>
      <Grid item xs={12} sm={8} style={{ maxHeight: '90vh', overflowY: 'auto' }}>
        <List>
          {questions.map((item, index) => (
            <ListItem key={index}>
              <ListItemText primary={item.question} />
            </ListItem>
          ))}
        </List>
      </Grid>
    </Paper>
  );
};
export default QuestionPanel;