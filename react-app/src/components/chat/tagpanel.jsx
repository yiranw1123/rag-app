import { useSelector } from "react-redux";
import { selectTags } from "../../features/tagState";
import { Grid, Paper } from '@mui/material';
import TagCard from './tagcard';

const TagPanel = () => {
  const tags = useSelector(selectTags);  // Assuming you're fetching tags like this
  return (
    <Paper>
      <div style={{ maxHeight: '50vh', overflowY: 'auto', padding:'2px' }}>
        <Grid container spacing={2}>
        {tags.map((tag, index) => (
          <Grid item key={index}>
            <TagCard tag={tag} />
          </Grid>
        ))}
        </Grid>
      </div>
    </Paper>
  );
};

export default TagPanel;