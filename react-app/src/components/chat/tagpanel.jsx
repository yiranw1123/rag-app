import { useSelector } from "react-redux";
import { selectTags } from "../../features/tagState";
import { Grid, Paper } from '@mui/material';
import TagCard from './tagcard';

const TagPanel = () =>{
  const tags = useSelector(selectTags);

  return(
    <Paper>
      <Grid item xs={12} sm={4}>
        {tags.map(tag => (
          <TagCard
            key={tag}
            tag={tag}
          />
        ))}
      </Grid>
    </Paper>
  );
};
export default TagPanel;