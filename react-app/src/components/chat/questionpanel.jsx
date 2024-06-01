import { useSelector } from "react-redux";
import { selectQuestions, setSelectedQuestion } from "../../features/questionState";
import { Grid, List, ListItem, ListItemText, Paper } from '@mui/material';
import { useDispatch } from "react-redux";

const QuestionPanel = () =>{
  const questions = useSelector(selectQuestions);

  const dispatch = useDispatch();
  const options = {
    weekday: 'short', // "Thu"
    year: 'numeric', // "2024"
    month: 'short', // "May"
    day: 'numeric', // "30"
    hour: '2-digit', // "16"
    minute: '2-digit', // "53"
    second: '2-digit', // "06"
    hour12: false // Use 24-hour time without AM/PM
  };

  const handleOnClick = (item) =>{
    dispatch(setSelectedQuestion(item));
  };

  return(
    <Paper>
      <div style={{ maxHeight: '50vh', minHeight:'30vh', overflowY: 'auto' }}>
        <Grid item xs={12} sm={8}>
          <List>
            {questions.map((item, index) => (
              <ListItem key={index} onClick={() => handleOnClick(item)}>
                <ListItemText primary={item.question} secondary={new Date(Number(item.timestamp)).toLocaleString('en-US', options)} />
              </ListItem>
            ))}
          </List>
        </Grid>
      </div>
    </Paper>
  );
};
export default QuestionPanel;